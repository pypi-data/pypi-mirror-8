#ifndef YAYI_MORPHOLOGICAL_LEVELING_HPP__
#define YAYI_MORPHOLOGICAL_LEVELING_HPP__

#include <yayiReconstruction/yayiReconstruction.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace reconstructions
  {
    /*!@brief Morphological leveling.
     * @ingroup reconstruction_grp
     *
     * This implementation performs the levelling as defined by Gomila & Meyer (see C.Gomila PhD thesis, @cite gomila_2001).
     * @author Raffi Enficiaud
     */
    YRec_ yaRC leveling_by_double_reconstruction(const IImage* im_marker, const IImage* im_mask, const se::IStructuringElement* se, IImage* imout);
  }
}


#endif /* YAYI_MORPHOLOGICAL_LEVELING_HPP__ */

