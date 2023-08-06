


#include <yayiPixelProcessing/image_copy.hpp>
#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiPixelProcessing/include/image_copy_T.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>
#include <yayiCommon/include/common_variantDispatch.hpp>
namespace yayi
{

  yaRC copy(const IImage* imin, const variant &rectin, const variant &rectout, IImage* imout)
  {
    yaRC return_value, res;
    
    if(imin == 0 || imout == 0)
      return yaRC_E_null_pointer;

    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const variant &, const variant &,  IImage*> 
      dispatch_object(return_value, imin, rectin, rectout, imout);
    
    
    switch(imin->DynamicType().c_type)
    {
    
    case type::c_scalar:
    {
    
      // 2D images
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          copy_image_windowed_t< Image<yaUINT8>, Image<yaUINT8 > >,
          copy_image_windowed_t< Image<yaUINT8>, Image<yaUINT16> >,
          copy_image_windowed_t< Image<yaUINT8>, Image<yaUINT32> >,
          copy_image_windowed_t< Image<yaUINT8>, Image<yaUINT64> >,

          copy_image_windowed_t< Image<yaUINT8>, Image<yaINT8 > >,
          copy_image_windowed_t< Image<yaUINT8>, Image<yaINT16> >,
          copy_image_windowed_t< Image<yaUINT8>, Image<yaINT32> >,
          copy_image_windowed_t< Image<yaUINT8>, Image<yaINT64> >,

          copy_image_windowed_t< Image<yaUINT8>, Image<yaF_simple> >,
          copy_image_windowed_t< Image<yaUINT8>, Image<yaF_double> >));


      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented) {return res;}
        
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          copy_image_windowed_t< Image<yaUINT16  >, Image<yaUINT16  > >,
          copy_image_windowed_t< Image<yaUINT32  >, Image<yaUINT32  > >,
          copy_image_windowed_t< Image<yaF_simple>, Image<yaF_simple> >,
          copy_image_windowed_t< Image<yaF_double>, Image<yaF_double> >,
          
          copy_image_windowed_t< Image<yaUINT16  >, Image<yaUINT8   > >,
          copy_image_windowed_t< Image<yaUINT32  >, Image<yaUINT8   > >,

          copy_image_windowed_t< Image<yaF_simple>, Image<yaUINT8   > >,
          copy_image_windowed_t< Image<yaF_simple>, Image<yaUINT16  > >,
          copy_image_windowed_t< Image<yaF_double>, Image<yaUINT8   > >
          ));

      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented) {return res;}


      // 3D images
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          copy_image_windowed_t< Image<yaUINT8, s_coordinate<3> >, Image<yaUINT8,  s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaUINT8, s_coordinate<3> >, Image<yaUINT16, s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaUINT8, s_coordinate<3> >, Image<yaUINT32, s_coordinate<3> > >,
          //copy_image_windowed_t< Image<yaUINT8, s_coordinate<3> >, Image<yaUINT64, s_coordinate<3> > >,

          copy_image_windowed_t< Image<yaUINT8, s_coordinate<3> >, Image<yaINT8,   s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaUINT8, s_coordinate<3> >, Image<yaINT16,  s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaUINT8, s_coordinate<3> >, Image<yaINT32,  s_coordinate<3> > >,
          //copy_image_windowed_t< Image<yaUINT8, s_coordinate<3> >, Image<yaINT64,  s_coordinate<3> > >,

          copy_image_windowed_t< Image<yaUINT8, s_coordinate<3> >, Image<yaF_simple, s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaUINT8, s_coordinate<3> >, Image<yaF_double, s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaF_simple, s_coordinate<3> >, Image<yaUINT8, s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaF_double, s_coordinate<3> >, Image<yaUINT8, s_coordinate<3> > >
        ));

      
      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented) {return res;}


      // 3D images
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          copy_image_windowed_t< Image<yaF_simple, s_coordinate<3> >, Image<yaF_simple, s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaF_double, s_coordinate<3> >, Image<yaF_double, s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaF_simple, s_coordinate<3> >, Image<yaUINT16, s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaF_double, s_coordinate<3> >, Image<yaUINT16, s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaF_simple, s_coordinate<3> >, Image<yaUINT32, s_coordinate<3> > >,
          copy_image_windowed_t< Image<yaF_double, s_coordinate<3> >, Image<yaUINT32, s_coordinate<3> > >
        ));

      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented) {return res;}

      // 3D images into 2D images
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          copy_image_windowed_t< Image<yaF_simple, s_coordinate<3> >, Image<yaF_simple> >,
          copy_image_windowed_t< Image<yaF_double, s_coordinate<3> >, Image<yaF_double> >,
          copy_image_windowed_t< Image<yaUINT8, s_coordinate<3> >, Image<yaUINT8> >,
          copy_image_windowed_t< Image<yaUINT16, s_coordinate<3> >, Image<yaUINT16> >,
          copy_image_windowed_t< Image<yaUINT32, s_coordinate<3> >, Image<yaUINT32> >
        ));

      if(res == yaRC_E_not_implemented) {return res;}
      return return_value;
    }

    case type::c_3:
    {
      // 2D-Color images
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          copy_image_windowed_t< Image< pixel8u_3 >, Image< pixel8u_3 > >,
          copy_image_windowed_t< Image< pixelFs_3 >, Image< pixelFs_3 > >,
          copy_image_windowed_t< Image< pixelFd_3 >, Image< pixelFd_3 > >
        ));
      if(res == yaRC_E_not_implemented) {return res;}
      return return_value;

    }
    
    default:
      std::cout << "blablabla false " << imin->DynamicType() << std::endl;
      return yaRC_E_not_implemented;
    }
  }
}
