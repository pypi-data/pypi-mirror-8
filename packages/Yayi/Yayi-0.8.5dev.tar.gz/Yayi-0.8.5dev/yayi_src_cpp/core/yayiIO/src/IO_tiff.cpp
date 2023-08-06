#include "yayi_IO.hpp"
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>


#include <math.h>
#include "tiffio.h"
#include <boost/tuple/tuple.hpp>


BOOST_STATIC_ASSERT(sizeof(TIFF_INT64_T) == 8);
BOOST_STATIC_ASSERT(sizeof(TIFF_UINT64_T) == 8);

namespace yayi {

  namespace IO {

    void TIFFError(thandle_t client_data, const char* module, const char* fmt, va_list argptr)
    {
      char msg[10240];  
      vsprintf (msg, fmt, argptr);
      yayi::errors::yayi_error_stream() << "TIFF error: " << module << " / " << msg << "\n";
    }

    struct init_tiff
    {
      init_tiff()
      {
        previous = TIFFSetErrorHandler(0);
        previous_ext = TIFFSetErrorHandlerExt(TIFFError);

      }
      ~init_tiff()
      {
        // needed ?
        TIFFSetErrorHandler(previous);
        TIFFSetErrorHandlerExt(previous_ext);
      }

      TIFFErrorHandler previous;
      TIFFErrorHandlerExt previous_ext;
    };

    static const init_tiff g_init_tiff = init_tiff();


    struct s_auto_release
    {
      tdata_t &buf;
      s_auto_release(tdata_t& b) : buf(b){}
      ~s_auto_release()
      {
        _TIFFfree(buf);
      }
    };



    template <class T>
    struct s_tiff_to_yayi_pixel
    {
      void operator()(T const *buffer, T* p) const
      {
        *p = *buffer;
      }
      void operator()(T const *buffer, T* p, int /*plane*/) const
      {
        *p = *buffer;
      }
    };

    template <class T, class U>
    struct s_tiff_to_yayi_pixel< s_compound_pixel_t<T, U> >
    {
      typedef s_compound_pixel_t<T, U> pixel_t;
      static const int dimension = s_get_pixel_dimension<pixel_t>::dimension;

      void operator()(T const *buffer, pixel_t* p) const
      {
        for(int i = 0; i < dimension; i++)
          (*p)[i] = buffer[i];
      }
      void operator()(T const *buffer, pixel_t* p, int plane) const
      {
        (*p)[plane] = *buffer;
      }
    };


    template <class pixel_type>
    yaRC readTIFFHelperTile(TIFF *tif, int config, Image<pixel_type>& im)
    {
      typedef typename s_get_pixel_scalar_type<pixel_type>::type scalar_type;

      // should match the types used in
      yaUINT32 tile_width, tile_height;
      TIFFGetField(tif, TIFFTAG_TILEWIDTH, &tile_width);
      TIFFGetField(tif, TIFFTAG_TILELENGTH, &tile_height);

      uint64 tile_size = TIFFTileSize64(tif);
      uint64 scanline = TIFFTileRowSize64(tif);
      assert(scanline % sizeof(scalar_type) == 0);
      uint32 nb_tiles = TIFFNumberOfTiles(tif);

      tdata_t buf = _TIFFmalloc(tile_size);
      s_auto_release obj_release(buf);

      s_tiff_to_yayi_pixel<pixel_type> copy_tiff;

      if(config == PLANARCONFIG_CONTIG)
      {
        // reading strips in the strip order
        std::map<ttile_t, std::pair<int, int> > map_tile_to_xy;
        for (int y = 0; y < im.Size()[1]; y += tile_height)
        {
          for (int x = 0; x < im.Size()[0]; x += tile_width)
          {
            ttile_t tile = TIFFComputeTile(tif, x, y, 0, 0);
            map_tile_to_xy[tile] = std::make_pair(x, y);
          }
        }

        for (ttile_t tile = 0; tile < nb_tiles; tile++)
        {
          // this is for raw strip reading

          if(TIFFReadEncodedTile(tif, tile, buf, std::numeric_limits<tsize_t>::max()) < 0)
          {
            return yaRC_E_file_io_error;
          }

          assert(map_tile_to_xy.count(tile) > 0);
          std::pair<int, int> current_tile_position = map_tile_to_xy[tile];


          scalar_type const * decoded_byte = static_cast<scalar_type const *>(buf);

          for(int y = 0, ycount = std::min<uint32>(tile_height, im.Size()[1] - current_tile_position.second); y < ycount; y++)
          {
            pixel_type *p = &im.pixel(c2D(current_tile_position.first, current_tile_position.second + y));
            int const xcount = std::min<uint32>(tile_width, im.Size()[0] - current_tile_position.first);
            for(int x = 0, v = 0;
                x < xcount;
                x++, v+= s_get_pixel_dimension<pixel_type>::dimension)
            {
              copy_tiff(decoded_byte + v, p + x);
            }
            decoded_byte += /*xcount */scanline/ sizeof(scalar_type);

          }
        }
      }
      else if(config == PLANARCONFIG_SEPARATE)
      {

      #ifndef NDEBUG
        if(type_support<pixel_type>::compound == type::c_scalar)
        {
          yaUINT16 nsamples;
          TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &nsamples);
          assert(nsamples == s_get_pixel_dimension<pixel_type>::dimension); // compilera
        }
      #endif

        // reading strips in the strip order
        std::map<ttile_t, std::vector< boost::tuples::tuple<int, int, int> > > map_tile_to_xy;
        for (int y = 0; y < im.Size()[1]; y += tile_height)
        {
          for (int x = 0; x < im.Size()[0]; x += tile_width)
          {
            for(int s = 0; s < s_get_pixel_dimension<pixel_type>::dimension; s++ )
            {
              ttile_t tile = TIFFComputeTile(tif, x, y, 0, s);
              map_tile_to_xy[tile].push_back(boost::tuples::make_tuple(s, x, y));
            }
          }
        }

        for (ttile_t tile = 0; tile < nb_tiles; tile++)
        {
          if(TIFFReadEncodedTile(tif, tile, buf, std::numeric_limits<tsize_t>::max()) < 0)
          {
            return yaRC_E_file_io_error;
          }

          assert(map_tile_to_xy.count(tile) > 0);
          std::vector< boost::tuples::tuple<int, int, int> > const &v_strips = map_tile_to_xy[tile];

          for(size_t i = 0; i < v_strips.size(); i++)
          {
            int current_column = boost::get<1>(v_strips[i]);
            int current_line   = boost::get<2>(v_strips[i]);
            int current_channel= boost::get<0>(v_strips[i]);

            scalar_type const * bc = static_cast<scalar_type const *>(buf);

            for(int y = 0, ycount = std::min<uint32>(tile_height, im.Size()[1] - current_line); y < ycount; y++)
            {
              pixel_type *p = &im.pixel(c2D(current_column, current_line + y));
              int const xcount = std::min<uint32>(tile_width, im.Size()[0] - current_column);
              for(int x = 0, v = 0;
                  x < xcount;
                  x++, /*v+= s_get_pixel_dimension<pixel_type>::dimension*/v++)
              {
                copy_tiff(bc + v, p + x, current_channel);
              }
              bc += /*xcount */scanline / sizeof(scalar_type);
            }
          }
        }

      }

      return yaRC_ok;

    }



    // note:there should be an additional transformation from the void* to the correct type, and this includes the
    // msb <-> lsb transformation.
    template <class pixel_type>
    yaRC readTIFFHelperStrip(TIFF *tif, int config, Image<pixel_type>& im)
    {
      typedef typename s_get_pixel_scalar_type<pixel_type>::type scalar_type;


      const uint32 nb_strips = TIFFNumberOfStrips(tif);
      uint32 rowsperstrip = std::numeric_limits<uint32>::max();
      if(TIFFGetField(tif, TIFFTAG_ROWSPERSTRIP, &rowsperstrip) < 0)
      {
        return yaRC_E_unknown;
      }
      tsize_t scanline = TIFFScanlineSize(tif);
      assert(scanline % sizeof(scalar_type) == 0);
      tmsize_t stripsize = TIFFStripSize(tif);//bc[0];
      tdata_t buf = _TIFFmalloc(stripsize);
      s_auto_release obj_release(buf);

      s_tiff_to_yayi_pixel<pixel_type> copy_tiff;

      if(config == PLANARCONFIG_CONTIG)
      {
        // reading strips in the strip order
        std::map<tstrip_t,int> map_strip_to_y;
        for (int y = 0; y < im.Size()[1]; y += rowsperstrip)
        {
          //uint32 nrow = (row+rowsperstrip > h ? h-row : rowsperstrip);
          tstrip_t strip = TIFFComputeStrip(tif, y, 0);
          map_strip_to_y[strip] = y;
        }

        for (tstrip_t strip = 0; strip < nb_strips; strip++)
        {
          if(TIFFReadEncodedStrip(tif, strip, buf, /*bc[strip]*/std::numeric_limits<tsize_t>::max()) < 0)
          {
            return yaRC_E_file_io_error;
          }

          assert(map_strip_to_y.count(strip) > 0);
          int current_line = map_strip_to_y[strip];


          scalar_type const * decoded_byte = static_cast<scalar_type const *>(buf);

          for(int y = 0, ycount = std::min<uint32>(rowsperstrip, im.Size()[1] - current_line); y < ycount; y++)
          {
            pixel_type *p = &im.pixel(c2D(0, current_line + y));
            for(int x = 0, v = 0;
                x < im.Size()[0];
                x++, v+= s_get_pixel_dimension<pixel_type>::dimension)
            {
              copy_tiff(decoded_byte + v, p + x);
            }
            decoded_byte += scanline / sizeof(scalar_type);
          }
        }

#if 0
        // todo replace by stripped oriented things...
        // this works though...
        tdata_t buf = _TIFFmalloc(TIFFScanlineSize(tif));
        if(!buf)
        {
          return yaRC_E_allocation;
        }

        s_auto_release obj_release(buf);

        // contiguous planar
        for (int current_line = 0; current_line < im.Size()[1]; current_line++)
        {
          if(TIFFReadScanline(tif, buf, current_line) < 0)
          {
            return yaRC_E_file_io_error;
          }


          // now buf contains the current line that should be developped into the image
          typedef typename s_get_pixel_scalar_type<pixel_type>::type scalar_type;
          scalar_type const * bc = static_cast<scalar_type const *>(buf);
          pixel_type *p = &im.pixel(c2D(0, current_line));
          for(int x = 0, v = 0;
              x < im.Size()[0];
              x++, v+= s_get_pixel_dimension<pixel_type>::dimension)
          {
            copy_tiff(bc + v, p + x);
          }


        }
#endif

      }
      else if(config == PLANARCONFIG_SEPARATE)
      {

      #ifndef NDEBUG
        if(type_support<pixel_type>::compound == type::c_scalar)
        {
          yaUINT16 nsamples;
          TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &nsamples);
          assert(nsamples == s_get_pixel_dimension<pixel_type>::dimension); // compilera
        }
      #endif

        // reading strips in the strip order
        std::map<tstrip_t, std::vector< std::pair<int, int> > > map_strip_to_y;
        for (int y = 0; y < im.Size()[1]; y += rowsperstrip)
        {
          //uint32 nrow = (row+rowsperstrip > h ? h-row : rowsperstrip);
          for(int s = 0; s < s_get_pixel_dimension<pixel_type>::dimension; s++ )
          {
            tstrip_t strip = TIFFComputeStrip(tif, y, s);
            map_strip_to_y[strip].push_back(std::make_pair(s, y));
          }

        }

        for (uint32 strip = 0; strip < nb_strips; strip++)
        {
          if(TIFFReadEncodedStrip(tif, strip, buf, /*bc[strip]*/std::numeric_limits<tsize_t>::max()) < 0)
          {
            return yaRC_E_file_io_error;
          }

          assert(map_strip_to_y.count(strip) > 0);
          std::vector< std::pair<int, int> > const &v_strips = map_strip_to_y[strip];

          for(size_t i = 0; i < v_strips.size(); i++)
          {
            int current_line = v_strips[i].second;
            int current_channel = v_strips[i].first;

            scalar_type const * bc = static_cast<scalar_type const *>(buf);
            pixel_type *p = &im.pixel(c2D(0, current_line));
            for(uint32 y = 0; y < rowsperstrip; y++)
            {
              for(int x = 0, v = 0;
                  x < im.Size()[0];
                  x++, /*v+= s_get_pixel_dimension<pixel_type>::dimension*/v++)
              {
                copy_tiff(bc + v, p + x, current_channel);
              }
              bc += scanline / sizeof(scalar_type);
              p  += im.Size()[0];
            }
          }
        }

      }

      return yaRC_ok;
    }

    template <type::compound_type e>
    yaRC readTIFFHelper(TIFF* tif, const type& t, int config, bool is_tiled, IImage* im)
    {
      assert(im->IsAllocated());
      switch(t.s_type)
      {
        case type::s_ui8:
        {
          typedef typename from_type<e, type::s_ui8>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t *im_t = dynamic_cast<image_t*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return (is_tiled ? readTIFFHelperTile(tif, config, *im_t) : readTIFFHelperStrip(tif, config, *im_t));
        }
        case type::s_ui16:
        {
          typedef typename from_type<e, type::s_ui16>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t *im_t = dynamic_cast<image_t*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return (is_tiled ? readTIFFHelperTile(tif, config, *im_t) : readTIFFHelperStrip(tif, config, *im_t));
        }
        case type::s_ui32:
        {
          typedef typename from_type<e, type::s_ui32>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t *im_t = dynamic_cast<image_t*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return (is_tiled ? readTIFFHelperTile(tif, config, *im_t) : readTIFFHelperStrip(tif, config, *im_t));
        }
        case type::s_ui64:
        {
          typedef typename from_type<e, type::s_ui64>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t *im_t = dynamic_cast<image_t*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return (is_tiled ? readTIFFHelperTile(tif, config, *im_t) : readTIFFHelperStrip(tif, config, *im_t));
        }
        case type::s_i8:
        {
          typedef typename from_type<e, type::s_i8>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t *im_t = dynamic_cast<image_t*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return (is_tiled ? readTIFFHelperTile(tif, config, *im_t) : readTIFFHelperStrip(tif, config, *im_t));
        }
        case type::s_i16:
        {
          typedef typename from_type<e, type::s_i16>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t *im_t = dynamic_cast<image_t*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return (is_tiled ? readTIFFHelperTile(tif, config, *im_t) : readTIFFHelperStrip(tif, config, *im_t));
        }
        case type::s_i32:
        {
          typedef typename from_type<e, type::s_i32>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t *im_t = dynamic_cast<image_t*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return (is_tiled ? readTIFFHelperTile(tif, config, *im_t) : readTIFFHelperStrip(tif, config, *im_t));
        }
        case type::s_i64:
        {
          typedef typename from_type<e, type::s_i64>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t *im_t = dynamic_cast<image_t*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return (is_tiled ? readTIFFHelperTile(tif, config, *im_t) : readTIFFHelperStrip(tif, config, *im_t));
        }
        case type::s_float:
        {
          typedef typename from_type<e, type::s_float>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t *im_t = dynamic_cast<image_t*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return (is_tiled ? readTIFFHelperTile(tif, config, *im_t) : readTIFFHelperStrip(tif, config, *im_t));
        }
        case type::s_double:
        {
          typedef typename from_type<e, type::s_double>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t *im_t = dynamic_cast<image_t*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return (is_tiled ? readTIFFHelperTile(tif, config, *im_t) : readTIFFHelperStrip(tif, config, *im_t));
        }
      default:
        return yaRC_E_not_implemented;
      }

    }

    yayi::type TIFF_to_yayi_format(bool is_planar, int photometric_type, int sample_per_pixel, int bit_per_sample, int sample_format)
    {
      // trouver une référence pour ce truc
      if(photometric_type!=PHOTOMETRIC_MINISBLACK &&
         photometric_type!=PHOTOMETRIC_MINISWHITE &&
         photometric_type!=PHOTOMETRIC_RGB &&
         photometric_type!=PHOTOMETRIC_SEPARATED)
      {
        if(!(photometric_type == PHOTOMETRIC_YCBCR && !is_planar))
          return type_undefined;
      }

      type ret;
      // check to see if complex should be implemented / if it does make sense
      // complex may be thought as a double channel
      switch(sample_per_pixel)
      {
      case 1:
        ret.c_type = type::c_scalar;
        break;
      case 3:
        ret.c_type = type::c_3;
        break;
      case 4:
        ret.c_type = type::c_4;
        break;
      default:
        return type_undefined;
      }

      switch(bit_per_sample)
      {
      //case 1: // support 1 bit ??
      case 8:
        assert(sample_format == SAMPLEFORMAT_INT || sample_format == SAMPLEFORMAT_UINT);
        ret.s_type = sample_format == SAMPLEFORMAT_UINT ? type::s_ui8 : type::s_i8;
        break;
      case 16:
        // not supported in our code
        if(sample_format == SAMPLEFORMAT_IEEEFP)
          return type_undefined;
        assert(sample_format == SAMPLEFORMAT_UINT || sample_format == SAMPLEFORMAT_INT);
        ret.s_type = sample_format == SAMPLEFORMAT_UINT ? type::s_ui16 : type::s_i16;
        break;
      case 32:
        //assert(sample_format == SAMPLEFORMAT_IEEEFP);
        if(sample_format == SAMPLEFORMAT_IEEEFP)
        {
          ret.s_type = type::s_float;
        }
        else
        {
          if(sample_format != SAMPLEFORMAT_UINT && sample_format != SAMPLEFORMAT_INT)
            return type_undefined;
          ret.s_type = sample_format == SAMPLEFORMAT_UINT ? type::s_ui32 : type::s_i32;
        }
        break;
      case 64:
        if(sample_format == SAMPLEFORMAT_IEEEFP)
        {
          ret.s_type = type::s_double;
        }
        else
        {
          if(sample_format != SAMPLEFORMAT_UINT && sample_format != SAMPLEFORMAT_INT)
            return type_undefined;
          ret.s_type = sample_format == SAMPLEFORMAT_UINT ? type::s_ui64 : type::s_i64;
        }
        break;
      default:
        return type_undefined;
      }

      return ret;
    }






    yaRC readTIFF(const string_type& filename, int image_index, IImage*& image)
    {
      TIFF* tif = TIFFOpen(filename.c_str(), "r");
      if(!tif)
      {
        return yaRC_E_file_io_error;
      }

      if (TIFFSetDirectory(tif, image_index) != 1) {
        // page not found
        TIFFClose(tif);
        return yaRC_E_bad_parameters;
      }


      // no use
      //char *data;
      //int res = TIFFGetField(tif, TIFFTAG_IMAGEDESCRIPTION, &data);
      //string_type description = res != 0 ? string_type(data) : "description not found";

      // warning: these types should match exactly the types in libtiff used to fill the values
      // the function to check is _TIFFVGetField
      yaUINT32 w, h;
      TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &w);
      TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &h);

      yaUINT16 sample_per_pixel(-1), photometric_type(-1), bit_per_sample(-1), config(-1), sample_format[4] = {1};
      TIFFGetField(tif, TIFFTAG_PHOTOMETRIC,      &photometric_type);
      TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL,  &sample_per_pixel);
      TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE,    &bit_per_sample);
      TIFFGetField(tif, TIFFTAG_PLANARCONFIG,     &config);
      TIFFGetField(tif, TIFFTAG_SAMPLEFORMAT,     &sample_format);

      if(config != PLANARCONFIG_SEPARATE && config != PLANARCONFIG_CONTIG)
      {
        // unsupported configuration
        TIFFClose(tif);
        return yaRC_E_not_implemented;
      }

      bool is_planar = config == PLANARCONFIG_SEPARATE;

      bool is_tiled = TIFFIsTiled(tif) != 0;

      type image_type = TIFF_to_yayi_format(is_planar, photometric_type, sample_per_pixel, bit_per_sample, sample_format[0]);
      if(image_type == type_undefined)
      {
        TIFFClose(tif);
        return yaRC_E_not_implemented;
      }

      image = IImage::Create(image_type, 2);
      if(image == 0)
      {
        TIFFClose(tif);
        return yaRC_E_unknown;
      }



      yaRC ret = image->SetSize(c2D(w, h));
      if(ret != yaRC_ok)
      {
        TIFFClose(tif);
        delete image;
        image = 0;
        return ret;
      }

      ret = image->AllocateImage();
      if(ret != yaRC_ok)
      {
        TIFFClose(tif);
        delete image;
        image = 0;
        return ret;
      }

      switch(image_type.c_type)
      {
        case type::c_scalar:
        {
          ret = readTIFFHelper<type::c_scalar>(tif, image_type, config, is_tiled, image);
          break;
        }
        case type::c_3:
        {
          ret = readTIFFHelper<type::c_3>(tif, image_type, config, is_tiled, image);
          break;
        }
        case type::c_4:
        {
          ret = readTIFFHelper<type::c_4>(tif, image_type, config, is_tiled, image);
          break;
        }
        default:
        {
          ret = yaRC_E_unknown;
          break;
        }
      }


      TIFFClose(tif);

      if(ret != yaRC_ok)
      {
        delete image;
        image = 0;
        return ret;
      }

      return ret;
    }


    bool yayi_to_TIFF_format(yayi::type const &format, yaUINT16 &photometric_type, yaUINT16 &sample_per_pixel, yaUINT16 &bit_per_sample, yaUINT16 sample_format[])
    {
      switch(format.c_type)
      {
      case type::c_scalar:
        sample_per_pixel = 1;
        photometric_type = PHOTOMETRIC_MINISBLACK;
        break;
      case type::c_3:
        sample_per_pixel = 3;
        photometric_type = PHOTOMETRIC_RGB; // check color space
        break;
      case type::c_4:
        sample_per_pixel = 4;
        photometric_type = PHOTOMETRIC_SEPARATED;
        break;
      default:
        return false;
      }

      switch(format.s_type)
      {
      case type::s_i8:
        sample_format[0] = SAMPLEFORMAT_INT;
        bit_per_sample = 8;
        break;
      case type::s_ui8:
        sample_format[0] = SAMPLEFORMAT_UINT;
        bit_per_sample = 8;
        break;
      case type::s_i16:
        sample_format[0] = SAMPLEFORMAT_INT;
        bit_per_sample = 16;
        break;
      case type::s_ui16:
        sample_format[0] = SAMPLEFORMAT_UINT;
        bit_per_sample = 16;
        break;
      case type::s_i32:
        sample_format[0] = SAMPLEFORMAT_INT;
        bit_per_sample = 32;
        break;
      case type::s_ui32:
        sample_format[0] = SAMPLEFORMAT_UINT;
        bit_per_sample = 32;
        break;
      case type::s_i64:
        sample_format[0] = SAMPLEFORMAT_INT;
        bit_per_sample = 64;
        break;
      case type::s_ui64:
        sample_format[0] = SAMPLEFORMAT_UINT;
        bit_per_sample = 64;
        break;
      case type::s_float:
        sample_format[0] = SAMPLEFORMAT_IEEEFP;
        bit_per_sample = 32;
        break;
      case type::s_double:
        sample_format[0] = SAMPLEFORMAT_IEEEFP;
        bit_per_sample = 64;
        break;
      default:
        return false;
      }

      for(int i = 1; i < sample_per_pixel; i++)
      {
        sample_format[i] = sample_format[0];
      }

      return true;
    }


    template <class T>
    struct s_yayi_to_tiff_pixel
    {
      void operator()(T const* p, T *buffer) const
      {
        *buffer = *p;
      }
      void operator()(T const* p, int , T *buffer) const
      {
        *buffer = *p;
      }
    };

    template <class T, class U>
    struct s_yayi_to_tiff_pixel< s_compound_pixel_t<T, U> >
    {
      typedef s_compound_pixel_t<T, U> pixel_t;
      static const int dimension = s_get_pixel_dimension<pixel_t>::dimension;

      void operator()(pixel_t const* p, T *buffer) const
      {
        for(int i = 0; i < dimension; i++)
          buffer[i] = (*p)[i];
      }
      void operator()(pixel_t const* p, int plane, T *buffer) const
      {
        *buffer = (*p)[plane];
      }
    };


    template <class pixel_type>
    yaRC writeTIFFHelperTile(Image<pixel_type> const& im, TIFF *tif)
    {
      typedef typename s_get_pixel_scalar_type<pixel_type>::type scalar_type;

      // should match the types used in
      yaUINT32 tile_width, tile_height;
      TIFFDefaultTileSize(tif, &tile_width, &tile_height);
      tile_width = std::min<yaUINT32>(tile_width, im.Size()[0]) & ~7; // multiple of 8
      tile_height = std::min<yaUINT32>(tile_height, im.Size()[1]) & ~7; // multiple of 8;
      TIFFSetField(tif, TIFFTAG_TILEWIDTH, tile_width);
      TIFFSetField(tif, TIFFTAG_TILELENGTH, tile_height);


      //yaUINT32 depth;
      //TIFFGetField(tif, TIFFTAG_IMAGEDEPTH, &depth); // dunno what to do with this one
      //TIFFSetField(tif, TIFFTAG_TILEDEPTH, depth);

      const uint64 tile_size = TIFFTileSize64(tif);
      const uint64 scanline = TIFFTileRowSize64(tif);
      assert(scanline % sizeof(scalar_type) == 0);
      const uint32 nb_tiles = TIFFNumberOfTiles(tif);

      tdata_t buf = _TIFFmalloc(tile_size);
      s_auto_release obj_release(buf);

      s_yayi_to_tiff_pixel<pixel_type> copy_tiff;


      #ifndef NDEBUG
      if(type_support<pixel_type>::compound == type::c_scalar)
      {
        yaUINT16 nsamples;
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &nsamples);
        assert(nsamples == s_get_pixel_dimension<pixel_type>::dimension); // compilera
      }
      #endif

      // reading strips in the strip order
      std::map<ttile_t, std::vector< boost::tuples::tuple<int, int, int> > > map_tile_to_xy;
      for (int y = 0; y < im.Size()[1]; y += tile_height)
      {
        for (int x = 0; x < im.Size()[0]; x += tile_width)
        {
          for(int s = 0; s < s_get_pixel_dimension<pixel_type>::dimension; s++ )
          {
            ttile_t tile = TIFFComputeTile(tif, x, y, 0, s);
            map_tile_to_xy[tile].push_back(boost::tuples::make_tuple(s, x, y));
          }
        }
      }

      for (ttile_t tile = 0; tile < nb_tiles; tile++)
      {

        assert(map_tile_to_xy.count(tile) > 0);
        std::vector< boost::tuples::tuple<int, int, int> > const &v_strips = map_tile_to_xy[tile];

        for(size_t i = 0; i < v_strips.size(); i++)
        {
          int current_column = boost::get<1>(v_strips[i]);
          int current_line   = boost::get<2>(v_strips[i]);
          int current_channel= boost::get<0>(v_strips[i]);

          scalar_type * bc = static_cast<scalar_type *>(buf);
          memset(bc, 0, static_cast<size_t>(tile_size));

          for(int y = 0, ycount = std::min<uint32>(tile_height, im.Size()[1] - current_line); y < ycount; y++)
          {
            pixel_type const *p = &im.pixel(c2D(current_column, current_line + y));
            int const xcount = std::min<uint32>(tile_width, im.Size()[0] - current_column);
            for(int x = 0, v = 0;
                x < xcount;
                x++, v++)
            {
              copy_tiff(p + x, current_channel, bc + v);
            }
            bc += /*xcount*/scanline / sizeof(scalar_type);
          }

          if(TIFFWriteEncodedTile(tif, tile, buf, tile_size/*(bc - static_cast<scalar_type *>(buf))*sizeof(scalar_type)*/) < 0)
          {
            return yaRC_E_file_io_error;
          }
        }
      }


      return yaRC_ok;

    }



    template <type::compound_type e>
    yaRC writeTIFFHelper(IImage const* im, TIFF* tif)
    {
      assert(im->IsAllocated());
      switch(im->DynamicType().s_type)
      {
        case type::s_ui8:
        {
          typedef typename from_type<e, type::s_ui8>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t const *im_t = dynamic_cast<image_t const*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return writeTIFFHelperTile(*im_t, tif);
        }
        case type::s_ui16:
        {
          typedef typename from_type<e, type::s_ui16>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t const *im_t = dynamic_cast<image_t const*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return writeTIFFHelperTile(*im_t, tif);
        }
        case type::s_ui32:
        {
          typedef typename from_type<e, type::s_ui32>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t const *im_t = dynamic_cast<image_t const*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return writeTIFFHelperTile(*im_t, tif);
        }
        case type::s_ui64:
        {
          typedef typename from_type<e, type::s_ui64>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t const *im_t = dynamic_cast<image_t const*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return writeTIFFHelperTile(*im_t, tif);
        }
        case type::s_i8:
        {
          typedef typename from_type<e, type::s_i8>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t const *im_t = dynamic_cast<image_t const*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return writeTIFFHelperTile(*im_t, tif);
        }
        case type::s_i16:
        {
          typedef typename from_type<e, type::s_i16>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t const *im_t = dynamic_cast<image_t const*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return writeTIFFHelperTile(*im_t, tif);
        }
        case type::s_i32:
        {
          typedef typename from_type<e, type::s_i32>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t const *im_t = dynamic_cast<image_t const*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return writeTIFFHelperTile(*im_t, tif);
        }
        case type::s_i64:
        {
          typedef typename from_type<e, type::s_i64>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t const *im_t = dynamic_cast<image_t const*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return writeTIFFHelperTile(*im_t, tif);
        }
        case type::s_float:
        {
          typedef typename from_type<e, type::s_float>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t const *im_t = dynamic_cast<image_t const*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return writeTIFFHelperTile(*im_t, tif);
        }
        case type::s_double:
        {
          typedef typename from_type<e, type::s_double>::type pixel_t;
          typedef Image<pixel_t> image_t;
          image_t const *im_t = dynamic_cast<image_t const*>(im);
          if(im_t == 0)
          {
            return yaRC_E_bad_parameters;
          }
          return writeTIFFHelperTile(*im_t, tif);
        }
      default:
        return yaRC_E_not_implemented;
      }

    }



    yaRC writeTIFF(const std::string &filename, const IImage *const & image)
    {

      if(image == 0)
        return yaRC_E_null_pointer;

      if(get_last_dimension(image->GetSize()) > 2)
        return yaRC_E_bad_size;

      type image_type = image->DynamicType();

      yaUINT16 sample_per_pixel(-1), photometric_type(-1), bit_per_sample(-1), sample_format[4] = {1};
      if(!yayi_to_TIFF_format(image_type, photometric_type, sample_per_pixel, bit_per_sample, sample_format))
      {
        return yaRC_E_not_implemented;
      }


      TIFF* tif = TIFFOpen(filename.c_str(), "w");
      if(!tif)
      {
        return yaRC_E_file_io_error;
      }

      // warning: these types should match exactly the types in libtiff used to fill the values
      // the function to check is _TIFFVGetField
      yaUINT32 const w(image->GetSize()[0]), h(image->GetSize()[1]);
      TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, w);
      TIFFSetField(tif, TIFFTAG_IMAGELENGTH, h);

      TIFFSetField(tif, TIFFTAG_PHOTOMETRIC,      photometric_type);
      TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL,  sample_per_pixel);
      TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE,    bit_per_sample);
      TIFFSetField(tif, TIFFTAG_PLANARCONFIG,     PLANARCONFIG_SEPARATE);
      TIFFSetField(tif, TIFFTAG_SAMPLEFORMAT,     sample_format[0]); // Raffi: there is nothing worst than va_arg stuff. The doc says there are N such values.
      TIFFSetField(tif, TIFFTAG_ORIENTATION,      ORIENTATION_TOPLEFT);

      TIFFSetField(tif, TIFFTAG_COMPRESSION,      COMPRESSION_DEFLATE);
      //TIFFSetField(tif, TIFFTAG_PREDICTOR,        PREDICTOR_HORIZONTAL);
      TIFFSetField(tif, TIFFTAG_PREDICTOR,        (bit_per_sample < 64 ? PREDICTOR_HORIZONTAL : PREDICTOR_NONE)); // dunno

      /* todo
      TIFFTAG_PRIMARYCHROMATICITIES = 6*RATIONAL
      TIFFTAG_WHITEPOINT = 2*RATIONAL
      */

      yaRC ret;
      switch(image_type.c_type)
      {
        case type::c_scalar:
        {
          ret = writeTIFFHelper<type::c_scalar>(image, tif);
          break;
        }

        case type::c_3:
        {
          ret = writeTIFFHelper<type::c_3>(image, tif);
          break;
        }
        case type::c_4:
        {
          ret = writeTIFFHelper<type::c_4>(image, tif);
          break;
        }
        default:
        {
          // this check is already performed in yayi_to_TIFF_format, so an existing file does not get
          // overwritten when an error occurs on the type
          ret = yaRC_E_unknown;
          break;
        }
      }


      TIFFClose(tif);

      return ret;
    }

  }
}


#if 0

// kept for TIFFRewriteDirectory
void updateTTag (SEXP fn, SEXP desc)
{
  TIFF *tiff;
  const TIFFFieldInfo *fip;
  const char* filename = CHAR(STRING_ELT(fn, 0)) ;
  const char* description = CHAR(STRING_ELT(desc, 0)) ;

  if((tiff = TIFFOpen(filename , "r+")) == NULL)
    error("Could not open image file '%s'", filename);

  fip = TIFFFieldWithTag(tiff, 270);
  if (!fip) error("Could not get field information");
  if (fip->field_type == TIFF_ASCII) {
    if (TIFFSetField(tiff, fip->field_tag, description) != 1)
      error("Failed to set field.");
  } else error("Description field is not ascii");
  TIFFRewriteDirectory(tiff);
  TIFFClose(tiff);
}

#endif
