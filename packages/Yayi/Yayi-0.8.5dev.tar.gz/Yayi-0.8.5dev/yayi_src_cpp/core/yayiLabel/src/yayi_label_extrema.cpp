
#include <yayiLabel/yayi_label_extrema.hpp>
#include <yayiLabel/include/yayi_label_extrema_t.hpp>

#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <yayiStructuringElement/include/se_dispatcher.hpp>
#include <yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>


namespace yayi
{
  namespace label
  {
  
    yaRC ImageLabelMinimas(const IImage* imin, const se::IStructuringElement* se, IImage* imout)
    {
      using namespace dispatcher;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const se::IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_label_minima_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16>  >,
          image_label_minima_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
          image_label_minima_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32>  >,
          image_label_minima_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >
        )
        );

      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented)
        return res;

      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_label_minima_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16>  >,
          image_label_minima_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
          image_label_minima_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32>  >,
          image_label_minima_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >
        )
        );
      if(res == yaRC_ok) return return_value;
      return res;
    }

    yaRC ImageLabelMaximas(const IImage* imin, const se::IStructuringElement* se, IImage* imout)
    {
      using namespace dispatcher;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const se::IStructuringElement*, IImage*> dispatch_object(return_value, imin, se, imout);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_label_maxima_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16>  >,
          image_label_maxima_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT16> >,
          image_label_maxima_t< Image<yaUINT8>,  se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32>  >,
          image_label_maxima_t< Image<yaUINT16>, se::s_neighborlist_se_hexa_x< s_coordinate<2> >,  Image<yaUINT32> >
        )
        );

      if(res == yaRC_ok) return return_value;
      else if(res != yaRC_E_not_implemented)
        return res;

      res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          image_label_maxima_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16>  >,
          image_label_maxima_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT16> >,
          image_label_maxima_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32>  >,
          image_label_maxima_t< Image<yaUINT16>, se::s_neighborlist_se< s_coordinate<2> >,  Image<yaUINT32> >
        )
        );
      if(res == yaRC_ok) return return_value;
      return res;
    }


  }
}
