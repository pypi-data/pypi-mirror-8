
#include <yayiMeasurements/measurements_mean_variance.hpp>
#include <yayiMeasurements/include/measurements_mean_variance_t.hpp>

#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>
#include <yayiCommon/include/common_variantDispatch.hpp>

namespace yayi
{
  namespace measurements
  {

    yaRC image_meas_mean(const IImage* imin, variant& out)
    {
      if(imin == 0)
        return yaRC_E_null_pointer;
      yaRC return_value;
      

      yayi::dispatcher::s_dispatcher<
        yaRC, 
        const IImage*, 
        variant&> dispatch_object(return_value, imin, out);
  
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_meas_mean_t< Image<yaUINT8> >,
          image_meas_mean_t< Image<yaUINT16> >,
          image_meas_mean_t< Image<yaUINT32> >,
          image_meas_mean_t< Image<yaUINT64> >,
          image_meas_mean_t< Image<yaF_simple> >,
          image_meas_mean_t< Image<yaF_double> >
        )
        );
      
      if(res == yaRC_ok)
        return return_value;
      return res;   
    }
    
    yaRC image_meas_mean_on_region(const IImage* imin, const IImage* imregions, variant& out)
    {
      if(imin == 0)
        return yaRC_E_null_pointer;
      yaRC return_value;
      

      yayi::dispatcher::s_dispatcher<
        yaRC, 
        const IImage*, 
        const IImage*,
        variant&> dispatch_object(return_value, imin, imregions, out);
  
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_meas_mean_on_region_t< Image<yaUINT8> , Image<yaUINT16> >,
          image_meas_mean_on_region_t< Image<yaUINT16>, Image<yaUINT16> >,
          image_meas_mean_on_region_t< Image<yaUINT32>, Image<yaUINT16> >,
          image_meas_mean_on_region_t< Image<yaUINT64>, Image<yaUINT16> >,
          image_meas_mean_on_region_t< Image<yaF_simple>, Image<yaUINT16> >,
          image_meas_mean_on_region_t< Image<yaF_double>, Image<yaUINT16> >
        )
        );
      
      if(res == yaRC_ok)
        return return_value;
      return res;   
    }
    
    yaRC image_meas_circular_mean_and_concentration_on_region(const IImage* imin, const IImage* imregions, variant& out)
    {
      if(imin == 0)
        return yaRC_E_null_pointer;
      yaRC return_value;
      
      yayi::dispatcher::s_dispatcher<
        yaRC, 
        const IImage*, 
        const IImage*,
        variant&> dispatch_object(return_value, imin, imregions, out);
  
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_meas_circular_mean_and_concentration_on_region_t< Image<pixelFs_3>, Image<yaUINT16> >,
          image_meas_circular_mean_and_concentration_on_region_t< Image<pixelFd_3>, Image<yaUINT16> >
        )
        );
      
      if(res == yaRC_ok)
        return return_value;
      return res;   
    }
    
    yaRC image_meas_weighted_circular_mean_and_concentration_on_region(const IImage* imin, const IImage* imregions, variant& out)
    {
      if(imin == 0)
        return yaRC_E_null_pointer;
      yaRC return_value;
      
      yayi::dispatcher::s_dispatcher<
        yaRC, 
        const IImage*, 
        const IImage*,
        variant&> dispatch_object(return_value, imin, imregions, out);
  
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_meas_weighted_circular_mean_and_concentration_on_region_t< Image<pixelFs_3>, Image<yaUINT16> >,
          image_meas_weighted_circular_mean_and_concentration_on_region_t< Image<pixelFd_3>, Image<yaUINT16> >
        )
        );
      
      if(res == yaRC_ok)
        return return_value;
      return res;   
    }    
    
    
    yaRC image_meas_circular_mean_and_concentration_on_mask(const IImage* imin, const IImage* immask, variant const& mask_value, variant& out)
    {
      if(imin == 0)
        return yaRC_E_null_pointer;
      yaRC return_value;

      yayi::dispatcher::s_dispatcher<
        yaRC,
        const IImage*,
        const IImage*,
        variant const&,
        variant&> dispatch_object(return_value, imin, immask, mask_value, out);

      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_meas_circular_mean_and_concentration_on_mask_t< Image<pixelFs_3>, Image<yaUINT16> >,
          image_meas_circular_mean_and_concentration_on_mask_t< Image<pixelFd_3>, Image<yaUINT16> >
        )
        );

      if(res == yaRC_ok)
        return return_value;
      return res;
    }
    
    yaRC image_meas_weighted_circular_mean_and_concentration_on_mask(const IImage* imin, const IImage* immask, variant const& mask_value, variant& out)
    {
      if(imin == 0)
        return yaRC_E_null_pointer;
      yaRC return_value;

      yayi::dispatcher::s_dispatcher<
        yaRC,
        const IImage*,
        const IImage*,
        variant const&,
        variant&> dispatch_object(return_value, imin, immask, mask_value, out);

      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_meas_weighted_circular_mean_and_concentration_on_mask_t< Image<pixelFs_3>, Image<yaUINT16> >,
          image_meas_weighted_circular_mean_and_concentration_on_mask_t< Image<pixelFd_3>, Image<yaUINT16> >
        )
        );

      if(res == yaRC_ok)
        return return_value;
      return res;
    }
    
    
  }
}
