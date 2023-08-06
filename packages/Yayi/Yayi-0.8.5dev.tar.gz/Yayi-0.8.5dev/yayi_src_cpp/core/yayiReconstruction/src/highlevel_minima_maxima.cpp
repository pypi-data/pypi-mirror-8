
#include <yayiReconstruction/highlevel_minima_maxima.hpp>
#include <yayiReconstruction/include/highlevel_minima_maxima_t.hpp>
#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <yayiStructuringElement/include/se_dispatcher.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>
#include <yayiCommon/include/common_variantDispatch.hpp>

namespace yayi { namespace hlmm {

  yaRC image_h_minima(const IImage* imin, const IStructuringElement* se,variant c, IImage* imout) {
    using namespace dispatcher;

    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*,variant,IImage*> dispatch_object(return_value, imin, se,c,imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_h_minima_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        image_h_minima_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        image_h_minima_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >,

        image_h_minima_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT8>  >,
        image_h_minima_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT16> >,
        image_h_minima_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT32> >,

        image_h_minima_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        image_h_minima_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
      )
    );
    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_h_minima_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        image_h_minima_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        image_h_minima_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >,

        image_h_minima_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT8>  >,
        image_h_minima_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT16> >,
        image_h_minima_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT32> >,

        image_h_minima_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        image_h_minima_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
    );

    if(res == yaRC_ok) return return_value;
    return res;

  }


  yaRC image_h_concave(const IImage* imin, const IStructuringElement* se,variant c, IImage* imout) {
    using namespace dispatcher;

    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*,variant,IImage*> dispatch_object(return_value, imin, se,c,imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_h_concave_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        image_h_concave_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        //image_h_concave_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >,

        image_h_concave_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT8>  >,
        image_h_concave_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT16> >,
        image_h_concave_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT32> >,

        image_h_concave_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        image_h_concave_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
      )
    );
    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_h_concave_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        image_h_concave_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        //image_h_concave_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >, FIXME abs ambiguiyty

        image_h_concave_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT8>  >,
        image_h_concave_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT16> >,
        image_h_concave_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT32> >,

        image_h_concave_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        image_h_concave_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
    );

    if(res == yaRC_ok) return return_value;
    return res;

  }

  yaRC image_h_maxima(const IImage* imin, const IStructuringElement* se,variant c, IImage* imout) {
    using namespace dispatcher;

    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*,variant,IImage*> dispatch_object(return_value, imin, se,c,imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_h_maxima_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        image_h_maxima_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        image_h_maxima_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >,

        image_h_maxima_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT8>  >,
        image_h_maxima_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT16> >,
        image_h_maxima_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT32> >,

        image_h_maxima_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        image_h_maxima_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
      )
    );
    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_h_maxima_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        image_h_maxima_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        image_h_maxima_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >,

        image_h_maxima_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT8>  >,
        image_h_maxima_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT16> >,
        image_h_maxima_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT32> >,

        image_h_maxima_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        image_h_maxima_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
    );

    if(res == yaRC_ok) return return_value;
    return res;

  }

  yaRC image_h_convex(const IImage* imin, const IStructuringElement* se,variant c, IImage* imout) {
    using namespace dispatcher;

    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*,variant,IImage*> dispatch_object(return_value, imin, se,c,imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_h_convex_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
        image_h_convex_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
        //image_h_convex_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >, fixme abs ambiguity

        image_h_convex_t< Image<yaINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT8>  >,
        image_h_convex_t< Image<yaINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT16> >,
        image_h_convex_t< Image<yaINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaINT32> >,

        image_h_convex_t< Image<yaF_simple>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_simple>  >,
        image_h_convex_t< Image<yaF_double>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaF_double>  >
      )
    );
    if(res == yaRC_ok) return return_value;
    else if(res != yaRC_E_not_implemented)
      return res;

    res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_h_convex_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
        image_h_convex_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
        //image_h_convex_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >,

        image_h_convex_t< Image<yaINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT8>  >,
        image_h_convex_t< Image<yaINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT16> >,
        image_h_convex_t< Image<yaINT32>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaINT32> >,

        image_h_convex_t< Image<yaF_simple>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_simple>  >,
        image_h_convex_t< Image<yaF_double>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaF_double>  >
      )
    );

    if(res == yaRC_ok) return return_value;
    return res;

  }

  yaRC image_pseudo_dynamic_opening(const IImage* imin, const IStructuringElement* se,variant c, IImage* imout)
  {
    using namespace dispatcher;

    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*,variant,IImage*> dispatch_object(return_value, imin, se,c,imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_h_dynamic_opening_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >
      )
    );
    if(res == yaRC_ok) return return_value;
    return res;

  }

  yaRC image_pseudo_dynamic_closing(const IImage* imin, const IStructuringElement* se,variant c, IImage* imout)
  {
    using namespace dispatcher;

    yaRC return_value;
    yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IStructuringElement*,variant,IImage*> dispatch_object(return_value, imin, se,c,imout);

    yaRC res = dispatch_object.calls_first_suitable(
      fusion::vector_tie(
        image_h_dynamic_closing_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >
      )
    );
    if(res == yaRC_ok) return return_value;
    return res;

  }
}}
