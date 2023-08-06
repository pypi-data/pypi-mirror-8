#ifndef YAYI_MORPHOLOGICAL_FILL_HOLES_HPP__
#define YAYI_MORPHOLOGICAL_FILL_HOLES_HPP__

#include <yayiReconstruction/yayiReconstruction.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace reconstructions
  {
    /*!@brief Fills the holes of imin using the structuring element se, stores the output in imout.
     * @ingroup reconstruction_grp
     *
     * @author Raffi Enficiaud
     */
    YRec_ yaRC fill_holes(const IImage* imin, const se::IStructuringElement* se, IImage* imout);
  }
}
 
#endif /* YAYI_MORPHOLOGICAL_FILL_HOLES_HPP__ */
