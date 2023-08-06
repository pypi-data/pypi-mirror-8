#ifndef YAYI_MORPHOLOGICAL_RECONSTRUCTIONS_HPP__
#define YAYI_MORPHOLOGICAL_RECONSTRUCTIONS_HPP__

#include <yayiReconstruction/yayiReconstruction.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace reconstructions
  {
    /*!@addtogroup reconstruction_grp
     * @{
     */  
    
    /*!@brief Algebraic opening by morphological reconstruction
     *
     * @author Raffi Enficiaud
     */
    YRec_ yaRC opening_by_reconstruction(const IImage* im_marker, const IImage* im_mask, const se::IStructuringElement* se, IImage* imout);

    /*!@brief Algebraic closing by morphological reconstruction
     *
     * @author Raffi Enficiaud
     */
    YRec_ yaRC closing_by_reconstruction(const IImage* im_marker, const IImage* im_mask, const se::IStructuringElement* se, IImage* imout);
    
    //! @}

  }
}


#endif /* YAYI_MORPHOLOGICAL_RECONSTRUCTIONS_HPP__ */

