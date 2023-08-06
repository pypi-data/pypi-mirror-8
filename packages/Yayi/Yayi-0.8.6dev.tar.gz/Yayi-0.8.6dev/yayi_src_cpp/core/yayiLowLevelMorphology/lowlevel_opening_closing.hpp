#ifndef YAYI_LOWLEVEL_MORPHOLOGY_OPENCLOSE_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_OPENCLOSE_HPP__


/*!@file
 * This file defines opening and closing/closure functions
 * @author Raffi Enficiaud
 */



#include <yayiLowLevelMorphology/yayiLowLevelMorphology.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace llmm
  {
/*!
 * @addtogroup llm_grp
 *
 *@{
 */      

    using namespace yayi::se;
    
    /*!@brief Computes the open of the input image imin, with the structuring element se, and places the
     * results inside imout
     *
     * @author Raffi Enficiaud
     */
    YLLMM_ yaRC open(const IImage* imin, const IStructuringElement*, IImage* imout);


    /*!@brief Computes the closure of the input image imin, with the structuring element se, and places the
     * results inside imout
     *
     * @author Raffi Enficiaud
     */
    YLLMM_ yaRC close(const IImage* imin, const IStructuringElement*, IImage* imout);
   //! @} doxygroup: llm_grp       
  }
}
#endif /* YAYI_LOWLEVEL_MORPHOLOGY_OPENCLOSE_HPP__ */
