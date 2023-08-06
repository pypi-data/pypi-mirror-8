
#include <yayiIO/include/yayi_IO.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <fstream>
#include <boost/scoped_array.hpp>

namespace yayi
{
  namespace IO
  {

    template <class pixel_t, int dim>
    yaRC readRAW_helper(std::ifstream &f, const s_coordinate<dim>& c, Image<pixel_t, s_coordinate<dim> >& imout) {

      offset size = total_number_of_points(c);
      f.read(reinterpret_cast<char *>(&imout.pixel(0)), sizeof(pixel_t) * size);

      return f.fail() ? yaRC_E_file_io_error : yaRC_ok;
    }

    template <class pixel_scalar_t, class pixel_dimension, int dim>
    yaRC readRAW_helper(std::ifstream &f, const s_coordinate<dim>& c, Image<s_compound_pixel_t<pixel_scalar_t, pixel_dimension>, s_coordinate<dim> >& imout) {

      typedef Image<s_compound_pixel_t<pixel_scalar_t, pixel_dimension>, s_coordinate<dim> > image_t;
      typedef typename image_t::iterator iterator_t;
      offset size = total_number_of_points(c);

      // maybe restrict this to a particular amount of lines
      boost::scoped_array<pixel_scalar_t> arr(new pixel_scalar_t[size]);
      pixel_scalar_t const *p = arr.get();

      for(int i = 0; i < pixel_dimension::value; i++)
      {
        f.read(reinterpret_cast<char *>(arr.get()), sizeof(pixel_scalar_t) * size);
        if(f.fail())
        {
          YAYI_DEBUG_MESSAGE("Error during the file reading");
          return yaRC_E_file_io_error;
        }

        offset o(0);
        for(iterator_t it(imout.begin_block()), ite(imout.end_block()); it != ite; ++it, o++)
        {
          (*it)[i] = p[o];
        }
      }

      return yaRC_ok;
    }



    template <class pixel_t>
    yaRC readRAW_helper_dim(std::ifstream &f, const s_coordinate<0>& c, IImage*& imout) {
      int dim = get_last_dimension(c);
      switch(dim) {
        case 2:
        {
          Image<pixel_t, s_coordinate<2> >* pim = dynamic_cast<Image<pixel_t, s_coordinate<2> >*>(imout);
          if(pim == 0) {
            YAYI_DEBUG_MESSAGE("Error on the dynamic cast: image of type " + imout->Description());
            return yaRC_E_unknown;
          }
          return readRAW_helper(f, s_coordinate<2>(c), *pim);
        }
        case 3:
        {
          Image<pixel_t, s_coordinate<3> >* pim = dynamic_cast<Image<pixel_t, s_coordinate<3> >*>(imout);
          if(pim == 0) {
            YAYI_DEBUG_MESSAGE("Error on the dynamic cast: image of type " + imout->Description());
            return yaRC_E_unknown;
          }
          return readRAW_helper(f, s_coordinate<3>(c), *pim);
        }
        case 4:
        {
          Image<pixel_t, s_coordinate<4> >* pim = dynamic_cast<Image<pixel_t, s_coordinate<4> >*>(imout);
          if(pim == 0) {
            YAYI_DEBUG_MESSAGE("Error on the dynamic cast: image of type " + imout->Description());
            return yaRC_E_unknown;
          }
          return readRAW_helper(f, s_coordinate<4>(c), *pim);
        }

        default:
          return yaRC_E_not_implemented;
      }
    }


    yaRC readRAW (const string_type &filename, const s_coordinate<0> &sizes, const type &image_type_, IImage* &out_image)
    {

      std::ifstream f(filename.c_str(), std::ios::binary);
      if(!f.is_open())
      {
        YAYI_DEBUG_MESSAGE("Unable to open file " + filename);
        return yaRC_E_file_io_error;
      }

      int dim = get_last_dimension(sizes);
      IImage *temp = IImage::Create(image_type_, dim);

      if(temp == 0)
        return yaRC_E_unknown;

      yaRC ret = temp->SetSize(sizes);
      if(ret != yaRC_ok)
        return ret;

      ret = temp->AllocateImage();
      if(ret != yaRC_ok)
        return ret;


      std::auto_ptr<IImage> lock(temp);



      switch(image_type_.c_type) {
      case type::c_scalar:
      {
        switch(image_type_.s_type) {
        case type::s_ui8:  ret = readRAW_helper_dim<yaUINT8> (f, sizes, temp); break;
        case type::s_ui16: ret = readRAW_helper_dim<yaUINT16>(f, sizes, temp); break;
        case type::s_ui32: ret = readRAW_helper_dim<yaUINT32>(f, sizes, temp); break;
        case type::s_ui64: ret = readRAW_helper_dim<yaUINT64>(f, sizes, temp); break;

        case type::s_i8:   ret = readRAW_helper_dim<yaINT8> (f, sizes, temp); break;
        case type::s_i16:  ret = readRAW_helper_dim<yaINT16>(f, sizes, temp); break;
        case type::s_i32:  ret = readRAW_helper_dim<yaINT32>(f, sizes, temp); break;
        case type::s_i64:  ret = readRAW_helper_dim<yaINT64>(f, sizes, temp); break;

        case type::s_float:   ret = readRAW_helper_dim<yaF_simple>(f, sizes, temp); break;
        case type::s_double:  ret = readRAW_helper_dim<yaF_double>(f, sizes, temp); break;
        default:
          return yaRC_E_not_implemented;
        }

        break;

      }
      case type::c_3:
      {
        switch(image_type_.s_type) {
        case type::s_ui8:  ret = readRAW_helper_dim<pixel8u_3> (f, sizes, temp); break;
        case type::s_ui16: ret = readRAW_helper_dim<pixel16u_3>(f, sizes, temp); break;
        case type::s_ui32: ret = readRAW_helper_dim<pixel32u_3>(f, sizes, temp); break;
        case type::s_ui64: ret = readRAW_helper_dim<pixel64u_3>(f, sizes, temp); break;

        case type::s_i8:   ret = readRAW_helper_dim<pixel8s_3> (f, sizes, temp); break;
        case type::s_i16:  ret = readRAW_helper_dim<pixel16s_3>(f, sizes, temp); break;
        case type::s_i32:  ret = readRAW_helper_dim<pixel32s_3>(f, sizes, temp); break;
        case type::s_i64:  ret = readRAW_helper_dim<pixel64s_3>(f, sizes, temp); break;

        case type::s_float:   ret = readRAW_helper_dim<pixelFs_3>(f, sizes, temp); break;
        case type::s_double:  ret = readRAW_helper_dim<pixelFd_3>(f, sizes, temp); break;
        default:
          return yaRC_E_not_implemented;
        }

        break;

      }
      case type::c_4:
      {
        switch(image_type_.s_type) {
        case type::s_ui8:  ret = readRAW_helper_dim<pixel8u_4> (f, sizes, temp); break;
        case type::s_ui16: ret = readRAW_helper_dim<pixel16u_4>(f, sizes, temp); break;
        case type::s_ui32: ret = readRAW_helper_dim<pixel32u_4>(f, sizes, temp); break;
        case type::s_ui64: ret = readRAW_helper_dim<pixel64u_4>(f, sizes, temp); break;

        case type::s_i8:   ret = readRAW_helper_dim<pixel8s_4> (f, sizes, temp); break;
        case type::s_i16:  ret = readRAW_helper_dim<pixel16s_4>(f, sizes, temp); break;
        case type::s_i32:  ret = readRAW_helper_dim<pixel32s_4>(f, sizes, temp); break;
        case type::s_i64:  ret = readRAW_helper_dim<pixel64s_4>(f, sizes, temp); break;

        case type::s_float:   ret = readRAW_helper_dim<pixelFs_4>(f, sizes, temp); break;
        case type::s_double:  ret = readRAW_helper_dim<pixelFd_4>(f, sizes, temp); break;
        default:
          return yaRC_E_not_implemented;
        }

        break;

      }
      default:
        //delete temp;
        return yaRC_E_not_implemented;
      }

      if(ret != yaRC_ok)
        return ret;

      out_image = lock.release();

      return yaRC_ok;
    }



    template <class pixel_t, int dim>
    yaRC writeRAW_helper(
      std::ofstream &f,
      Image<pixel_t, s_coordinate<dim> > const & imin) {

      offset size = total_number_of_points(imin.Size());

      f.write(reinterpret_cast<const char *>(&imin.pixel(0)), sizeof(pixel_t) * size);

      return f.fail() ? yaRC_E_file_io_error : yaRC_ok;
    }

    template <class pixel_scalar_t, class pixel_dimension, int dim>
    yaRC writeRAW_helper(std::ofstream &f,
      Image<s_compound_pixel_t<pixel_scalar_t, pixel_dimension>, s_coordinate<dim> > const & imin) {

      typedef Image<s_compound_pixel_t<pixel_scalar_t, pixel_dimension>, s_coordinate<dim> > image_t;
      typedef typename image_t::const_iterator const_iterator_t;
      offset size = total_number_of_points(imin.Size());

      // maybe restrict this to a particular amount of lines
      boost::scoped_array<pixel_scalar_t> arr(new pixel_scalar_t[size]);
      pixel_scalar_t *p = arr.get();

      for(int i = 0; i < pixel_dimension::value; i++)
      {
        offset o(0);
        for(const_iterator_t it(imin.begin_block()), ite(imin.end_block()); it != ite; ++it, o++)
        {
          p[o] = (*it)[i];
        }

        f.write(reinterpret_cast<char *>(arr.get()), sizeof(pixel_scalar_t) * size);
        if(f.fail())
        {
          YAYI_DEBUG_MESSAGE("Error during the file reading");
          return yaRC_E_file_io_error;
        }

      }

      return yaRC_ok;
    }




    template <class pixel_t>
    yaRC writeRAW_helper_dim(std::ofstream &f, const IImage*const& imin) {

      int dim = get_last_dimension(imin->GetSize());

      switch(dim) {
        case 2:
        {
          typedef Image<pixel_t, s_coordinate<2> > image_t;
          image_t const *im = dynamic_cast<image_t const*>(imin);
          if(!im)
          {
            YAYI_DEBUG_MESSAGE("Error on the dynamic cast: image of type " + imin->Description());
            return yaRC_E_null_pointer;
          }
          return writeRAW_helper(f, *im);
        }
        case 3:
        {
          typedef Image<pixel_t, s_coordinate<3> > image_t;
          image_t const *im = dynamic_cast<image_t const*>(imin);
          if(!im)
          {
            YAYI_DEBUG_MESSAGE("Error on the dynamic cast: image of type " + imin->Description());
            return yaRC_E_null_pointer;
          }
          return writeRAW_helper(f, *im);
        }
        case 4:
        {
          typedef Image<pixel_t, s_coordinate<4> > image_t;
          image_t const *im = dynamic_cast<image_t const*>(imin);
          if(!im)
          {
            YAYI_DEBUG_MESSAGE("Error on the dynamic cast: image of type " + imin->Description());
            return yaRC_E_null_pointer;
          }
          return writeRAW_helper(f, *im);
        }

        default:
          return yaRC_E_not_implemented;
      }
    }

    yaRC writeRAW(const string_type &filename, const IImage*const &imin)
    {
      if(!imin->IsAllocated())
        return yaRC_E_not_allocated;


      std::ofstream f(filename.c_str(), std::ios::binary);
      if(!f.is_open())
      {
        YAYI_DEBUG_MESSAGE("Unable to open file " + filename);
        return yaRC_E_file_io_error;
      }


      switch(imin->DynamicType().c_type) {
      case type::c_scalar:
      {
        switch(imin->DynamicType().s_type) {
        case type::s_ui8:  return writeRAW_helper_dim<yaUINT8> (f, imin);
        case type::s_ui16: return writeRAW_helper_dim<yaUINT16>(f, imin);
        case type::s_ui32: return writeRAW_helper_dim<yaUINT32>(f, imin);
        case type::s_ui64: return writeRAW_helper_dim<yaUINT64>(f, imin);

        case type::s_i8:   return writeRAW_helper_dim<yaINT8> (f, imin);
        case type::s_i16:  return writeRAW_helper_dim<yaINT16>(f, imin);
        case type::s_i32:  return writeRAW_helper_dim<yaINT32>(f, imin);
        case type::s_i64:  return writeRAW_helper_dim<yaINT64>(f, imin);

        case type::s_float:   return writeRAW_helper_dim<yaF_simple>(f, imin);
        case type::s_double:  return writeRAW_helper_dim<yaF_double>(f, imin);
        default:
          return yaRC_E_not_implemented;
        }

      }
      case type::c_3:
      {
        switch(imin->DynamicType().s_type) {
        case type::s_ui8:  return writeRAW_helper_dim<pixel8u_3> (f, imin);
        case type::s_ui16: return writeRAW_helper_dim<pixel16u_3>(f, imin);
        case type::s_ui32: return writeRAW_helper_dim<pixel32u_3>(f, imin);
        case type::s_ui64: return writeRAW_helper_dim<pixel64u_3>(f, imin);

        case type::s_i8:   return writeRAW_helper_dim<pixel8s_3>(f, imin);
        case type::s_i16:  return writeRAW_helper_dim<pixel16s_3>(f, imin);
        case type::s_i32:  return writeRAW_helper_dim<pixel32s_3>(f, imin);
        case type::s_i64:  return writeRAW_helper_dim<pixel64s_3>(f, imin);

        case type::s_float:   return writeRAW_helper_dim<pixelFs_3>(f, imin);
        case type::s_double:  return writeRAW_helper_dim<pixelFd_3>(f, imin);
        default:
          return yaRC_E_not_implemented;
        }

        break;

      }
      case type::c_4:
      {
        switch(imin->DynamicType().s_type) {
        case type::s_ui8:  return writeRAW_helper_dim<pixel8u_4> (f, imin);
        case type::s_ui16: return writeRAW_helper_dim<pixel16u_4>(f, imin);
        case type::s_ui32: return writeRAW_helper_dim<pixel32u_4>(f, imin);
        case type::s_ui64: return writeRAW_helper_dim<pixel64u_4>(f, imin);

        case type::s_i8:   return writeRAW_helper_dim<pixel8s_4>(f, imin);
        case type::s_i16:  return writeRAW_helper_dim<pixel16s_4>(f, imin);
        case type::s_i32:  return writeRAW_helper_dim<pixel32s_4>(f, imin);
        case type::s_i64:  return writeRAW_helper_dim<pixel64s_4>(f, imin);

        case type::s_float:   return writeRAW_helper_dim<pixelFs_4>(f, imin);
        case type::s_double:  return writeRAW_helper_dim<pixelFd_4>(f, imin);
        default:
          return yaRC_E_not_implemented;
        }

        break;

      }

      default:
        //delete temp;
        DEBUG_ASSERT(false, "unsupported type");
        return yaRC_E_not_implemented;
      }


      return yaRC_ok;
    }




  }
}

