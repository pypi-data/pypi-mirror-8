
#include <yayiPixelProcessing/image_logics.hpp>
#include <yayiPixelProcessing/include/image_logics_t.hpp>

#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>


namespace yayi
{

  yaRC image_bitwise_not(const IImage* imin, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        bitwise_not_images_t< Image<yaUINT8>,     Image<yaUINT8> >,
        bitwise_not_images_t< Image<yaUINT16>,    Image<yaUINT16> >,
        bitwise_not_images_t< Image<yaUINT32>,    Image<yaUINT32> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }


  yaRC image_bitwise_and(const IImage* imin1, const IImage* imin2, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin1, imin2, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        bitwise_and_images_t< Image<yaUINT8>,     Image<yaUINT8>,     Image<yaUINT8> >,
        bitwise_and_images_t< Image<yaUINT16>,    Image<yaUINT16>,    Image<yaUINT16> >,
        bitwise_and_images_t< Image<yaUINT32>,    Image<yaUINT32>,    Image<yaUINT32> >,
        bitwise_and_images_t< Image<pixel8u_3>,   Image<pixel8u_3>,   Image<pixel8u_3> >,
        bitwise_and_images_t< Image<pixel8u_3>,   Image<yaUINT8>,     Image<pixel8u_3> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }


  yaRC image_bitwise_or(const IImage* imin1, const IImage* imin2, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin1, imin2, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        bitwise_or_images_t< Image<yaUINT8>,     Image<yaUINT8>,     Image<yaUINT8> >,
        bitwise_or_images_t< Image<yaUINT16>,    Image<yaUINT16>,    Image<yaUINT16> >,
        bitwise_or_images_t< Image<yaUINT32>,    Image<yaUINT32>,    Image<yaUINT32> >,
        bitwise_or_images_t< Image<pixel8u_3>,   Image<pixel8u_3>,   Image<pixel8u_3> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

}
