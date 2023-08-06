
#include <yayiPixelProcessing/image_arithmetics.hpp>
#include <yayiPixelProcessing/include/image_arithmetics_t.hpp>

#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>
#include <yayiCommon/include/common_variantDispatch.hpp>


namespace yayi
{




  yaRC image_add(const IImage* imin1, const IImage* imin2, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin1, imin2, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        add_images_t< Image<yaUINT8>,     Image<yaUINT8>,    Image<yaUINT8> >,
        add_images_t< Image<yaUINT8>,     Image<yaUINT8>,    Image<yaUINT16> >,
        add_images_t< Image<yaF_simple>,  Image<yaF_simple>, Image<yaF_simple> >,
        add_images_t< Image<yaF_double>,  Image<yaF_double>, Image<yaF_double> >,
        add_images_t< Image<yaUINT8>,     Image<yaINT8>,     Image<yaINT16> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

  yaRC image_subtract(const IImage* imin1, const IImage* imin2, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin1, imin2, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        subtract_images_t< Image<yaUINT8>,     Image<yaUINT8>,    Image<yaUINT8> >,
        subtract_images_t< Image<yaUINT8>,     Image<yaUINT8>,    Image<yaINT16> >,
        subtract_images_t< Image<yaF_simple>,  Image<yaF_simple>, Image<yaF_simple> >,
        subtract_images_t< Image<yaF_double>,  Image<yaF_double>, Image<yaF_double> >,
        subtract_images_t< Image<yaUINT8>,     Image<yaINT8>,     Image<yaINT16> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

  yaRC image_subtract_with_lower_bound(const IImage* imin1, const IImage* imin2, const variant& lower_bound, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const IImage*, 
      const variant&,
      IImage*> dispatch_object(return_value, imin1, imin2, lower_bound, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        subtract_with_lower_bound_images_t< Image<yaUINT8>,     Image<yaUINT8>,    Image<yaUINT8> >,
        subtract_with_lower_bound_images_t< Image<yaUINT16>,    Image<yaUINT16>,   Image<yaUINT16> >,
        subtract_with_lower_bound_images_t< Image<yaF_simple>,  Image<yaF_simple>, Image<yaF_simple> >,
        subtract_with_lower_bound_images_t< Image<yaF_double>,  Image<yaF_double>, Image<yaF_double> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

  

  yaRC image_abssubtract(const IImage* imin1, const IImage* imin2, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin1, imin2, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        abssubtract_images_t< Image<yaUINT8>,     Image<yaUINT8>,    Image<yaUINT8> >,
        abssubtract_images_t< Image<yaUINT8>,     Image<yaUINT8>,    Image<yaINT16> >,
        abssubtract_images_t< Image<yaF_simple>,  Image<yaF_simple>, Image<yaF_simple> >,
        abssubtract_images_t< Image<yaF_double>,  Image<yaF_double>, Image<yaF_double> >,
        abssubtract_images_t< Image<yaUINT8>,     Image<yaINT8>,     Image<yaINT16> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }
  

  yaRC image_multiply(const IImage* imin1, const IImage* imin2, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin1, imin2, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        multiply_images_t< Image<yaUINT8>,     Image<yaUINT8>,    Image<yaUINT16> >,
        multiply_images_t< Image<yaF_simple>,  Image<yaF_simple>, Image<yaF_simple> >,
        multiply_images_t< Image<yaF_double>,  Image<yaF_double>, Image<yaF_double> >,
        multiply_images_t< Image<yaUINT8>,     Image<yaINT8>,     Image<yaINT16> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }



  yaRC image_add_constant(const IImage* imin, variant const &c, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      variant const&,
      IImage*> dispatch_object(return_value, imin, c, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        add_images_constant_t< Image<yaUINT8>,     Image<yaUINT8> >,
        add_images_constant_t< Image<yaUINT16>,    Image<yaUINT16> >,
        add_images_constant_t< Image<yaF_simple>,  Image<yaF_simple> >,
        add_images_constant_t< Image<yaF_double>,  Image<yaF_double> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

  yaRC image_add_constant_upper_bound(const IImage* imin, variant const& c, variant const &up, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      variant const&,
      variant const&,
      IImage*> dispatch_object(return_value, imin, c, up, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        add_images_constant_upper_bound_t< Image<yaUINT8>,     Image<yaUINT8> >,
        add_images_constant_upper_bound_t< Image<yaUINT16>,    Image<yaUINT16> >,
        add_images_constant_upper_bound_t< Image<yaF_simple>,  Image<yaF_simple> >,
        add_images_constant_upper_bound_t< Image<yaF_double>,  Image<yaF_double> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }






  yaRC image_subtract_constant(const IImage* imin, variant const &c, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      variant const&,
      IImage*> dispatch_object(return_value, imin, c, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        subtract_images_constant_t< Image<yaUINT8>,     Image<yaUINT8> >,
        subtract_images_constant_t< Image<yaUINT16>,    Image<yaUINT16> >,
        subtract_images_constant_t< Image<yaF_simple>,  Image<yaF_simple> >,
        subtract_images_constant_t< Image<yaF_double>,  Image<yaF_double> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

  yaRC image_subtract_constant_lower_bound(const IImage* imin, variant const &c, variant const &lower_bound, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      variant const&,
      variant const&,
      IImage*> dispatch_object(return_value, imin, c, lower_bound, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        subtract_images_constant_lower_bound_t< Image<yaUINT8>,     Image<yaUINT8> >,
        subtract_images_constant_lower_bound_t< Image<yaUINT16>,    Image<yaUINT16> >,
        subtract_images_constant_lower_bound_t< Image<yaF_simple>,  Image<yaF_simple> >,
        subtract_images_constant_lower_bound_t< Image<yaF_double>,  Image<yaF_double> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

  yaRC image_multiply_constant(const IImage* imin, variant const &c, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      variant const&,
      IImage*> dispatch_object(return_value, imin, c, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        multiply_images_constant_t< Image<yaUINT8>,     yaINT32,    Image<yaUINT8> >,
        multiply_images_constant_t< Image<yaF_simple>,  yaUINT8,    Image<yaUINT8> >,
        multiply_images_constant_t< Image<yaF_double>,  yaUINT8,    Image<yaUINT8> >,
        multiply_images_constant_t< Image<yaF_simple>,  yaF_simple, Image<yaF_simple> >,
        multiply_images_constant_t< Image<yaF_double>,  yaF_double, Image<yaF_double> >,
        multiply_images_constant_t< Image<yaUINT8>,     yaINT32,    Image<yaUINT16> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }


  yaRC image_supremum(const IImage* imin1, const IImage* imin2, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin1, imin2, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        supremum_images_t< Image<yaUINT8>,     Image<yaUINT8>,    Image<yaUINT8> >,
        supremum_images_t< Image<yaUINT16>,    Image<yaUINT16>,   Image<yaUINT16> >,
        supremum_images_t< Image<yaUINT32>,    Image<yaUINT32>,   Image<yaUINT32> >,
        supremum_images_t< Image<yaF_simple>,  Image<yaF_simple>, Image<yaF_simple> >,
        supremum_images_t< Image<yaF_double>,  Image<yaF_double>, Image<yaF_double> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }

  yaRC image_infimum(const IImage* imin1, const IImage* imin2, IImage* imout)
  {
    yaRC return_value;

    yayi::dispatcher::s_dispatcher<
      yaRC, 
      const IImage*, 
      const IImage*, 
      IImage*> dispatch_object(return_value, imin1, imin2, imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        infimum_images_t< Image<yaUINT8>,     Image<yaUINT8>,    Image<yaUINT8> >,
        infimum_images_t< Image<yaUINT16>,    Image<yaUINT16>,   Image<yaUINT16> >,
        infimum_images_t< Image<yaUINT32>,    Image<yaUINT32>,   Image<yaUINT32> >,
        infimum_images_t< Image<yaF_simple>,  Image<yaF_simple>, Image<yaF_simple> >,
        infimum_images_t< Image<yaF_double>,  Image<yaF_double>, Image<yaF_double> >
      )
      );
      
    if(res == yaRC_ok)
      return return_value;
    return res;  
  }


}

