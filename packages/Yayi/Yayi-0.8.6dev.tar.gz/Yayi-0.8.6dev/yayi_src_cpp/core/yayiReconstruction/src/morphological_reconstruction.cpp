
#include <yayiReconstruction/morphological_reconstruction.hpp>
#include <yayiReconstruction/include/morphological_reconstruction_t.hpp>


#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <yayiStructuringElement/include/se_dispatcher.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>


namespace yayi
{
  namespace reconstructions
  {
  
    yaRC opening_by_reconstruction(const IImage* im_marker, const IImage* im_mask, const se::IStructuringElement* se, IImage* imout)
    {
      using namespace dispatcher;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IImage*, const se::IStructuringElement*, IImage*> dispatch_object(return_value, im_marker, im_mask, se, imout);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          opening_by_reconstruction_t< Image<yaUINT8>, Image<yaUINT8>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
          opening_by_reconstruction_t< Image<yaUINT16>,Image<yaUINT16>,se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16>  >,
          opening_by_reconstruction_t< Image<yaUINT32>,Image<yaUINT32>,se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32>  >
        )
        );

      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented)
        return res;
      
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          opening_by_reconstruction_t< Image<yaUINT8>, Image<yaUINT8>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
          opening_by_reconstruction_t< Image<yaUINT16>,Image<yaUINT16>,se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16>  >,
          opening_by_reconstruction_t< Image<yaUINT32>,Image<yaUINT32>,se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32>  >
        )
        );

      if(res == yaRC_ok) return return_value;
      return res;
    }

    yaRC closing_by_reconstruction(const IImage* im_marker, const IImage* im_mask, const se::IStructuringElement* se, IImage* imout)
    {
      using namespace dispatcher;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const IImage*, const se::IStructuringElement*, IImage*> dispatch_object(return_value, im_marker, im_mask, se, imout);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          closing_by_reconstruction_t< Image<yaUINT8>, Image<yaUINT8>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT8>  >,
          closing_by_reconstruction_t< Image<yaUINT16>,Image<yaUINT16>,se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16>  >,
          closing_by_reconstruction_t< Image<yaUINT32>,Image<yaUINT32>,se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32>  >
        )
        );

      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented)
        return res;
      
      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          closing_by_reconstruction_t< Image<yaUINT8>, Image<yaUINT8>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT8>  >,
          closing_by_reconstruction_t< Image<yaUINT16>,Image<yaUINT16>,se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16>  >,
          closing_by_reconstruction_t< Image<yaUINT32>,Image<yaUINT32>,se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32>  >
        )
        );

      if(res == yaRC_ok) return return_value;
      return res;
    }

  }
}
