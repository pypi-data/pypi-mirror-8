
#include <yayiLowLevelMorphology/lowlevel_geodesic.hpp>
#include <yayiLowLevelMorphology/include/lowlevel_geodesic_t.hpp>
#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <yayiStructuringElement/include/se_dispatcher.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>


namespace yayi { namespace llmm {

  yaRC geodesic_erosion(const IImage* imin, const IImage* immask, const IStructuringElement* se, IImage* imout) {
    using namespace dispatcher;
    
    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, immask, se, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        geodesic_erode_image_t< Image<yaUINT8>,  Image<yaUINT8>,      se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        geodesic_erode_image_t< Image<yaUINT16>, Image<yaUINT16>,     se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        geodesic_erode_image_t< Image<yaF_simple>, Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        geodesic_erode_image_t< Image<yaF_double>, Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >,

        geodesic_erode_image_t< Image<yaUINT8>,  Image<yaUINT8>,      se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        geodesic_erode_image_t< Image<yaUINT16>, Image<yaUINT16>,     se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        geodesic_erode_image_t< Image<yaF_simple>, Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        geodesic_erode_image_t< Image<yaF_double>, Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    return res;

  }

  yaRC geodesic_dilation(const IImage* imin, const IImage* immask, const IStructuringElement* se, IImage* imout) {
    using namespace dispatcher;
    
    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IImage*, const IStructuringElement*, IImage*> dispatch_object(return_value, imin, immask, se, imout);
    
    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        geodesic_dilate_image_t< Image<yaUINT8>,  Image<yaUINT8>,      se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        geodesic_dilate_image_t< Image<yaUINT16>, Image<yaUINT16>,     se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        geodesic_dilate_image_t< Image<yaF_simple>, Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        geodesic_dilate_image_t< Image<yaF_double>, Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >,

        geodesic_dilate_image_t< Image<yaUINT8>,  Image<yaUINT8>,      se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        geodesic_dilate_image_t< Image<yaUINT16>, Image<yaUINT16>,     se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        geodesic_dilate_image_t< Image<yaF_simple>, Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        geodesic_dilate_image_t< Image<yaF_double>, Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
      );
    if(res == yaRC_ok) return return_value;
    return res;

  }



}}
