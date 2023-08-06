#ifndef YAYI_LABEL_EXTREMA_HPP__
#define YAYI_LABEL_EXTREMA_HPP__


#include <yayiLabel/yayi_Label.hpp>


namespace yayi
{
  namespace label
  {
    /*!@defgroup label_extrema_grp Label Extrema
     * @ingroup label_grp
     * @{
     */
    //! Connected minima plateaus with a single "id" per minimum in the output image
    YLab_ yaRC ImageLabelMinimas(const IImage* imin, const se::IStructuringElement* se, IImage* imout);

    //! Connected maximas plateaus with a single "id" per maximas in the output image
    YLab_ yaRC ImageLabelMaximas(const IImage* imin, const se::IStructuringElement* se, IImage* imout);

  //! @} addtogroup: Label_extrema_grp
  }
}

#endif /* YAYI_LABEL_EXTREMA_HPP__ */ 
