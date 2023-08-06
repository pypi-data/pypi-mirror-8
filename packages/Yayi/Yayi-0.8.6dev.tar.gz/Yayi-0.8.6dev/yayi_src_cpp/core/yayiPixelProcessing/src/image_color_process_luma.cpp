#include <yayiPixelProcessing/image_color_process.hpp>
#include <yayiPixelProcessing/include/image_color_process_luma_t.hpp>

#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>

namespace yayi {

  yaRC color_RGB_to_L601(const IImage* imin, IImage* imout) {
  
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);
      
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_RGB_to_L601_t< Image<pixel8u_3>, Image<yaF_simple> >,
        color_RGB_to_L601_t< Image<pixel8u_3>, Image<yaUINT8> >,
        color_RGB_to_L601_t< Image<pixelFs_3>, Image<yaF_simple> >,
        color_RGB_to_L601_t< Image<pixelFd_3>, Image<yaF_double> >
      )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }


  yaRC color_RGB_to_L709(const IImage* imin, IImage* imout)
  {
  
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_RGB_to_L709_t< Image<pixel8u_3>, Image<yaF_simple> >,
        color_RGB_to_L709_t< Image<pixel8u_3>, Image<yaUINT8> >,
        color_RGB_to_L709_t< Image<pixelFs_3>, Image<yaF_simple> >,
        color_RGB_to_L709_t< Image<pixelFd_3>, Image<yaF_double> >
      )
      );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }

}
