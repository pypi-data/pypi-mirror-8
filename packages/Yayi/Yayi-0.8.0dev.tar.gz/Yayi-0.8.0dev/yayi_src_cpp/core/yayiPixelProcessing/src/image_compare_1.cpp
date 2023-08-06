#include <yayiPixelProcessing/image_compare.hpp>
#include <yayiPixelProcessing/include/image_compare_T.hpp>

#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>
#include <yayiCommon/include/common_variantDispatch.hpp>



namespace yayi
{

  yaRC image_compare_si(const IImage* imin1, comparison_operations c, variant v_compare, const IImage* im_true_value, variant false_value, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      comparison_operations,
      variant, 
      const IImage*,
      variant, 
      IImage*> dispatch_object(return_value, imin1, c, v_compare, im_true_value, false_value, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        // image_in, image_true, image_out
        image_compare_si_stub< Image<yaUINT8>,  Image<yaUINT8>,   Image<yaUINT8> >,
        image_compare_si_stub< Image<yaUINT8>,  Image<yaUINT16>,  Image<yaUINT16> >,
        image_compare_si_stub< Image<yaUINT16>, Image<yaUINT8>,   Image<yaUINT8> >,
        image_compare_si_stub< Image<yaUINT8>,  Image<pixel8u_3>, Image<pixel8u_3> >,
        image_compare_si_stub< Image<yaUINT16>, Image<pixel8u_3>, Image<pixel8u_3> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;    
  }

  yaRC image_compare_ii(const IImage* imin1, comparison_operations c, const IImage* imin2, const IImage* im_true_value, variant false_value, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      comparison_operations,
      const IImage*, 
      const IImage*,
      variant, 
      IImage*> dispatch_object(return_value, imin1, c, imin2, im_true_value, false_value, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        // image_in, image_in2, image_true, image_out
        image_compare_ii_stub< Image<yaUINT8>, Image<yaUINT8>, Image<yaUINT8>, Image<yaUINT8> >,
        image_compare_ii_stub< Image<yaUINT8>, Image<yaUINT8>, Image<yaUINT16>, Image<yaUINT16> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;    
  }

  yaRC image_compare_iii(const IImage* imin1, comparison_operations c, const IImage* imin2, const IImage* im_true_value, const IImage* im_false_value, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      comparison_operations,
      const IImage*, 
      const IImage*,
      const IImage*, 
      IImage*> dispatch_object(return_value, imin1, c, imin2, im_true_value, im_false_value, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        // image_in, image_in2, image_true, image_false, image_out
        image_compare_iii_stub< Image<yaUINT8>, Image<yaUINT8>, Image<yaUINT8>, Image<yaUINT8>, Image<yaUINT8> >,
        image_compare_iii_stub< Image<yaUINT8>, Image<yaUINT8>, Image<yaUINT16>, Image<yaUINT16>, Image<yaUINT16> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;    
  }


  yaRC image_compare_sii(const IImage* imin1, comparison_operations c, variant v_compare, const IImage* im_true_value, const IImage* im_false_value, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      comparison_operations,
      variant, 
      const IImage*,
      const IImage*, 
      IImage*> dispatch_object(return_value, imin1, c, v_compare, im_true_value, im_false_value, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        // image_in, image_true, image_false, image_out
        image_compare_sii_stub< Image<yaUINT8>, Image<yaUINT8>, Image<yaUINT8>, Image<yaUINT8> >,
        image_compare_sii_stub< Image<yaUINT8>, Image<yaUINT16>, Image<yaUINT16>, Image<yaUINT16> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;    
  }



}

