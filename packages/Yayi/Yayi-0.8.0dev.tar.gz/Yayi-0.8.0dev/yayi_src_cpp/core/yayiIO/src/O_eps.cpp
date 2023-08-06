#include "yayi_IO.hpp"
#include <yayiCommon/common_types.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <fstream>


namespace yayi {

  namespace IO {


    template <class stream_t>
    void halfchar_to_hexa_ascii(stream_t &o, unsigned char v, int& nb_char)
    {
      DEBUG_ASSERT(v < 16, "provided value is incorrect");
      o << (v < 0xa ? v + 0x30: v + 0x65);
      nb_char++;
    }

    template <class stream_t>
    void to_hexa_ascii(stream_t &o, unsigned char v, int& nb_char)
    {
      halfchar_to_hexa_ascii(o, (v >> 4) & 0x0f, nb_char);
      halfchar_to_hexa_ascii(o, v & 0x0f, nb_char);
    }

    template <class stream_t>
    void to_hexa_ascii(stream_t &o, pixel8u_3 const& v, int& nb_char)
    {
      to_hexa_ascii(o, v.a, nb_char);
      to_hexa_ascii(o, v.b, nb_char);
      to_hexa_ascii(o, v.c, nb_char);
    }



    yaRC EPSCheckImage(const IImage* im)
    {
      if(im == 0)
        return yaRC_E_bad_parameters;

      if(!im->IsAllocated())
        return yaRC_E_not_allocated;

      if(im->DynamicType().s_type != type::s_ui8) 
        return yaRC_E_bad_parameters;

      return yaRC_ok;
    }

    yaRC encapsulated_postscript_head(std::ofstream &fp, const IImage *im)
    {
      assert(im != 0);
      fp << "%!PS-Adobe-3.0 EPSF-3.0" << std::endl;
      fp << "%%Creator: The R twins" << std::endl;
      fp << "%%Title: MorpheeCreated"<< std::endl;
      //fp << "%%%%CreationDate: today"  << std::endl;//, ctime(&t));

      fp << "%%BoundingBox: 0 0 " << im->GetSize()[0] << " " << im->GetSize()[1] << std::endl;
      fp << "%%LanguageLevel: 2" << std::endl;
      //fp << "%%%%Pages: (atend)" << std::endl;
      fp << "%%DocumentData: Clean7Bit" << std::endl;
      return yaRC_ok;
    }

    yaRC postscript_head(std::ofstream &fp, const IImage *im)
    {
      assert(im != 0);
      fp << im->GetSize()[0] << " " << im->GetSize()[1] << " scale" << std::endl;
      fp << im->GetSize()[0] << " " << im->GetSize()[1] << " 8 [";
      fp << im->GetSize()[0] << " 0 0 -" << im->GetSize()[1] << " 0 " << im->GetSize()[1] << "]" << std::endl;

      if(im->DynamicType().c_type == type::c_scalar)
      {
        fp << "{currentfile "<< im->GetSize()[0] << " string readhexstring pop} bind"<< std::endl;
        fp << "image" << std::endl;
      }
      else if(im->DynamicType().c_type == type::c_3)
      {
        fp << "{currentfile 3 "<< im->GetSize()[0] << " mul string readhexstring pop} bind"<< std::endl;
        fp << "false 3 colorimage" << std::endl;
      }
      else
      {
        return yaRC_E_bad_parameters;
      }


      return yaRC_ok;
    }


    yaRC postscript_tail(std::ofstream &fp)
    {
      fp << "%%EOF" << std::endl;
      fp << "showpage" << std::endl;
      return yaRC_ok;
    }

    template <class image_t, class stream_t>
    yaRC postscript_data_write(IImage const* iim, stream_t &s)
    {
      const image_t *im = dynamic_cast<const image_t*>(iim);
      if(im == 0)
      {
        return yaRC_E_bad_parameters;
      }
      
      int i = 0;
      for(typename image_t::const_iterator it(im->begin_block()), itend(im->end_block()); it != itend; ++it)
      {
        if(i > 80)
        {
          s << std::endl;
          i = 0;
        }
        to_hexa_ascii(s, *it, i);
      }
      
      return yaRC_ok;
    }

    yaRC writeEPS(const string_type &filename, IImage const * const & image)
    {

      if(image == 0)
        return yaRC_E_null_pointer;

      IImage::coordinate_type im_coords = image->GetSize();
      if(im_coords.dimension() < 2)
        return yaRC_E_bad_size;


      type im_type = image->DynamicType();
      if(im_type.c_type != type::c_scalar && im_type.c_type != type::c_3)
        return yaRC_E_bad_colour;
      if(im_type.s_type != type::s_ui8)
        return yaRC_E_bad_colour;


      if(!image->IsAllocated())
        return yaRC_E_not_allocated;



      std::ofstream fp(filename.c_str());
      if(!fp.is_open())
        return yaRC_E_file_io_error;

      encapsulated_postscript_head(fp, image);
      postscript_head(fp, image);

      switch(image->DynamicType().c_type)
      {
      case type::c_scalar:
      {
        if(postscript_data_write< Image<yaUINT8> >(image, fp) != yaRC_ok)
        {
          return yaRC_E_unknown;
        }
        break;
      }
      case type::c_3:
      {
        if(postscript_data_write< Image<pixel8u_3> >(image, fp) != yaRC_ok)
        {
          return yaRC_E_unknown;
        }
        break;
      }
      default:
        return yaRC_E_bad_parameters;
      }


      fp << std::endl;
      postscript_tail(fp);
      fp.close();
      return yaRC_ok;
    }


  }
}


