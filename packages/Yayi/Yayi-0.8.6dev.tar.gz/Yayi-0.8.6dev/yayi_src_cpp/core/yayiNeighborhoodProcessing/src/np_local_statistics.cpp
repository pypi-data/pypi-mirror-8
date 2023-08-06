
#include <yayiNeighborhoodProcessing/np_local_statistics.hpp>
#include <yayiNeighborhoodProcessing/include/np_local_statistics_t.hpp>

#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiCommon/include/common_variantDispatch.hpp>

#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>

#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <yayiStructuringElement/include/se_dispatcher.hpp>

namespace yayi
{
  namespace np
  {
    yaRC image_local_mean(IImage const* imin, IStructuringElement const* se, IImage* imout)
    {
    
      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_local_mean_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
          image_local_mean_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple> >,
          image_local_mean_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple> >,

          image_local_mean_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
          image_local_mean_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple> >,
          image_local_mean_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple> >,

          image_local_mean_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
          image_local_mean_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
        )
        );
      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented)
        return res;

      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_local_mean_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
          image_local_mean_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple> >,
          image_local_mean_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple> >,

          image_local_mean_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
          image_local_mean_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple> >,
          image_local_mean_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple> >,

          image_local_mean_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
          image_local_mean_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
        )
        );

      if(res != yaRC_ok)
        return res;
      return return_value;
    }


    yaRC image_local_circular_mean_and_concentration(IImage const* imin, IStructuringElement const* se, IImage* imout)
    {
    
      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_local_circular_mean_and_concentration_t< Image<pixelFs_3>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,   Image< std::complex<yaF_simple> > >,
          image_local_circular_mean_and_concentration_t< Image<pixelFd_3>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,   Image< std::complex<yaF_double> > >,
          image_local_circular_mean_and_concentration_t< Image<pixelFs_3>, se::s_neighborlist_se< s_coordinate<2> >,          Image< std::complex<yaF_simple> > >,
          image_local_circular_mean_and_concentration_t< Image<pixelFd_3>, se::s_neighborlist_se< s_coordinate<2> >,          Image< std::complex<yaF_double> > >
        )
        );

      if(res != yaRC_ok)
        return res;
      return return_value;

    }
  
    yaRC image_local_weighted_circular_mean_and_concentration(IImage const* imin, IStructuringElement const* se, IImage* imout)
    {
    
      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_local_weighted_circular_mean_and_concentration_t< Image<pixelFs_3>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image< std::complex<yaF_simple> > >,
          image_local_weighted_circular_mean_and_concentration_t< Image<pixelFd_3>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image< std::complex<yaF_double> > >,
          image_local_weighted_circular_mean_and_concentration_t< Image<pixelFs_3>, se::s_neighborlist_se< s_coordinate<2> >,  Image< std::complex<yaF_simple> > >,
          image_local_weighted_circular_mean_and_concentration_t< Image<pixelFd_3>, se::s_neighborlist_se< s_coordinate<2> >,  Image< std::complex<yaF_double> > >
        )
        );

      if(res != yaRC_ok)
        return res;
      return return_value;

    }



    yaRC image_local_median(IImage const* imin, IStructuringElement const* se, IImage* imout)
    {
    
      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_local_median_t< Image<yaUINT8>,     se::s_neighborlist_se_hexa_x< s_coordinate<2> >, Image< yaUINT8 > >,
          image_local_median_t< Image<yaF_simple>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >, Image< yaF_simple > >,
          image_local_median_t< Image<yaF_double>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >, Image< yaF_double > >,

          image_local_median_t< Image<yaUINT8>,     se::s_neighborlist_se< s_coordinate<2> >, Image< yaUINT8 > >,
          image_local_median_t< Image<yaF_simple>,  se::s_neighborlist_se< s_coordinate<2> >, Image< yaF_simple > >,
          image_local_median_t< Image<yaF_double>,  se::s_neighborlist_se< s_coordinate<2> >, Image< yaF_double > >
        )
        );

      if(res != yaRC_ok)
        return res;
      return return_value;

    }
  }
}