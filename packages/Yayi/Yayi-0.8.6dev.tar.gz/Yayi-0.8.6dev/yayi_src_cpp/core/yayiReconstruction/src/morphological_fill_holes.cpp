
#include <yayiReconstruction/morphological_fill_holes.hpp>
#include <yayiReconstruction/include/morphological_fill_holes_t.hpp>

#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <yayiStructuringElement/include/se_dispatcher.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>


namespace yayi
{
  namespace reconstructions
  {
    yaRC fill_holes(const IImage* imin, const se::IStructuringElement* se, IImage* imout)
    {
      using namespace dispatcher;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const se::IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);

      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          fill_holes_image_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> > >,
          fill_holes_image_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> > >,
          fill_holes_image_t< Image<yaUINT32>, se::s_neighborlist_se_hexa_x< s_coordinate<2> > >
        )
        );

      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented)
        return res;
      
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          fill_holes_image_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> > >,
          fill_holes_image_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> > >,
          fill_holes_image_t< Image<yaUINT32>, se::s_neighborlist_se< s_coordinate<2> > >,
          fill_holes_image_t< Image<yaUINT8,  s_coordinate<3> >, se::s_neighborlist_se< s_coordinate<3> > >,
          fill_holes_image_t< Image<yaUINT16, s_coordinate<3> >, se::s_neighborlist_se< s_coordinate<3> > >,
          fill_holes_image_t< Image<yaUINT32, s_coordinate<3> >, se::s_neighborlist_se< s_coordinate<3> > >
        )
        );

      if(res == yaRC_ok) return return_value;
      return res;
    
    
    }
  
  }
  
}
