
#include <yayiPixelProcessing/image_compare.hpp>
#include <yayiPixelProcessing/include/image_compare_T.hpp>

#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>
#include <yayiCommon/include/common_variantDispatch.hpp>

namespace yayi
{

  yaRC image_threshold(const IImage* imin, variant const &lower_bound, variant const &upper_bound, variant const &true_value, variant const &false_value, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      variant const &, 
      variant const &,
      variant const &,
      variant const &, 
      IImage*> dispatch_object(return_value, imin, lower_bound, upper_bound, true_value, false_value, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_threshold_t< Image<yaUINT8>, Image<yaUINT8> >,
        image_threshold_t< Image<yaUINT16>, Image<yaUINT8> >,
        image_threshold_t< Image<yaF_simple>, Image<yaUINT8> >,
        image_threshold_t< Image<yaF_double>, Image<yaUINT8> >,
        image_threshold_t< Image<yaUINT8>, Image<yaUINT16> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

  yaRC image_lookup_transform(const IImage* imin, variant const &map_lut, variant const &default_value, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      variant const &, 
      variant const &, 
      IImage*> dispatch_object(return_value, imin, map_lut, default_value, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_lookup_transform_t< Image<yaUINT8>,   Image<yaUINT8> >,
        image_lookup_transform_t< Image<yaUINT16>,  Image<yaUINT8> >,
        image_lookup_transform_t< Image<yaUINT16>,  Image<yaUINT16> >,
        image_lookup_transform_t< Image<yaUINT8>,   Image<pixel8u_3> >,
        image_lookup_transform_t< Image<yaUINT16>,  Image<pixel8u_3> >,
        image_lookup_transform_t< Image<yaUINT32>,  Image<pixel8u_3> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }



  yaRC image_compare_s(const IImage* imin, comparison_operations c, variant value, variant true_value, variant false_value, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      comparison_operations,
      variant, 
      variant,
      variant, 
      IImage*> dispatch_object(return_value, imin, c, value, true_value, false_value, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_compare_s_stub< Image<yaUINT8>, Image<yaUINT8> >,
        image_compare_s_stub< Image<yaUINT8>, Image<yaUINT16> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

  yaRC image_compare_i(const IImage* imin1, comparison_operations c, const IImage* imin2, variant true_value, variant false_value, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      comparison_operations,
      const IImage*, 
      variant,
      variant, 
      IImage*> dispatch_object(return_value, imin1, c, imin2, true_value, false_value, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_compare_i_stub< Image<yaUINT8>,   Image<yaUINT8>,   Image<yaUINT8> >,
        image_compare_i_stub< Image<yaUINT8>,   Image<yaUINT8>,   Image<yaUINT16> >,
        image_compare_i_stub< Image<yaUINT16>,  Image<yaUINT16>,  Image<yaUINT16> >,
        image_compare_i_stub< Image<yaUINT8>,   Image<yaUINT8>,   Image<pixel8u_3> >,
        image_compare_i_stub< Image<yaUINT16>,  Image<yaUINT16>,  Image<pixel8u_3> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;    
  }
  

}

