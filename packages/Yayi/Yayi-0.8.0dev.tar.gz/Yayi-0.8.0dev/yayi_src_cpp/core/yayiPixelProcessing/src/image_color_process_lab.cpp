
#include <iostream>
#include <yayiPixelProcessing/image_color_process.hpp>
#include <yayiPixelProcessing/include/image_color_process_lab_t.hpp>

#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>

namespace yayi {
  
  yaRC color_XYZ_to_LAB_refWE(const IImage* imin, IImage* imout) {
    
    yaRC return_value;
    
    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_XYZ_to_LAB_refWE_t< Image<pixelFs_3>, Image<pixelFs_3> >, 
        color_XYZ_to_LAB_refWE_t< Image<pixelFd_3>, Image<pixelFd_3> >
      )
    );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }
  yaRC color_LAB_to_XYZ_refWE(const IImage* imin, IImage* imout) {
    
    yaRC return_value;
    
    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_LAB_to_XYZ_refWE_t< Image<pixelFs_3>, Image<pixelFs_3> >, 
        color_LAB_to_XYZ_refWE_t< Image<pixelFd_3>, Image<pixelFd_3> >
      )
    );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }
  
  yaRC color_XYZ_to_LAB_refWA(const IImage* imin, IImage* imout) {
    
    yaRC return_value;
    
    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_XYZ_to_LAB_refWA_t< Image<pixelFs_3>, Image<pixelFs_3> >, 
        color_XYZ_to_LAB_refWA_t< Image<pixelFd_3>, Image<pixelFd_3> >
      )
    );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }
  yaRC color_LAB_to_XYZ_refWA(const IImage* imin, IImage* imout) {
    
    yaRC return_value;
    
    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_LAB_to_XYZ_refWA_t< Image<pixelFs_3>, Image<pixelFs_3> >, 
        color_LAB_to_XYZ_refWA_t< Image<pixelFd_3>, Image<pixelFd_3> >
      )
    );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }
  
  yaRC color_XYZ_to_LAB_refWD65(const IImage* imin, IImage* imout) {
    
    yaRC return_value;
    
    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_XYZ_to_LAB_refWD65_t< Image<pixelFs_3>, Image<pixelFs_3> >, 
        color_XYZ_to_LAB_refWD65_t< Image<pixelFd_3>, Image<pixelFd_3> >
      )
    );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }
  yaRC color_LAB_to_XYZ_refWD65(const IImage* imin, IImage* imout) {
    
    yaRC return_value;
    
    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_LAB_to_XYZ_refWD65_t< Image<pixelFs_3>, Image<pixelFs_3> >, 
        color_LAB_to_XYZ_refWD65_t< Image<pixelFd_3>, Image<pixelFd_3> >
      )
    );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }
  
  yaRC color_XYZ_to_LAB_refWD75(const IImage* imin, IImage* imout) {
    
    yaRC return_value;
    
    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_XYZ_to_LAB_refWD75_t< Image<pixelFs_3>, Image<pixelFs_3> >, 
        color_XYZ_to_LAB_refWD75_t< Image<pixelFd_3>, Image<pixelFd_3> >
      )
    );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }
  yaRC color_LAB_to_XYZ_refWD75(const IImage* imin, IImage* imout) {
    
    yaRC return_value;
    
    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        color_LAB_to_XYZ_refWD75_t< Image<pixelFs_3>, Image<pixelFs_3> >, 
        color_LAB_to_XYZ_refWD75_t< Image<pixelFd_3>, Image<pixelFd_3> >
      )
    );
    if(res == yaRC_ok)
      return return_value;
    return res;
  }
  
  
  

  
}
