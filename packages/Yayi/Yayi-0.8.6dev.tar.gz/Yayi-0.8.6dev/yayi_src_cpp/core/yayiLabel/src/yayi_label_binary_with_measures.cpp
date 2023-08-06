
#include <yayiLabel/yayi_label_binary_with_measure.hpp>
#include <yayiLabel/include/yayi_label_binary_with_measure_t.hpp>

#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiCommon/include/common_variantDispatch.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <yayiStructuringElement/include/se_dispatcher.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>


namespace yayi
{
  namespace label
  {
  
  
    yaRC image_label_binary_components_with_area(const IImage* imin, const se::IStructuringElement* se, IImage* imout, variant& areas)
    {
      using namespace dispatcher;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const se::IStructuringElement*, IImage*, variant&> 
        dispatch_object(return_value, imin, se, imout, areas);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          // 2D
          image_binary_label_with_area_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,          Image<yaUINT16>  >,
          image_binary_label_with_area_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,   Image<yaUINT16>  >,
          
          // 3D
          image_binary_label_with_area_t< Image<yaUINT8, s_coordinate<3> >,  se::s_neighborlist_se< s_coordinate<3> >,          Image<yaUINT16, s_coordinate<3> >  >,
          image_binary_label_with_area_t< Image<yaUINT8, s_coordinate<3> >,  se::s_neighborlist_se_hexa_x< s_coordinate<3> >,   Image<yaUINT16, s_coordinate<3> >  >
        )
        );

      if(res == yaRC_ok) return return_value;
      return res;
    }
  
  
  }
}
