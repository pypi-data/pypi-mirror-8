#ifndef YAYI_LOWLEVEL_MORPHOLOGY_GRADIENT_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_GRADIENT_HPP__

/*!@file
 * 
 */

#include <yayiLowLevelMorphology/yayiLowLevelMorphology.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi {
  namespace llmm {
/*!
 * @addtogroup llm_grp
 *
 *@{
 */         
  
  using namespace yayi::se;
  
  /*!@brief Computes the gradient of the input image imin, with the structuring element se, and places the
   * results inside imout
   *
   * @author Raffi Enficiaud
   */
  YLLMM_ yaRC gradient(const IImage* imin, const IStructuringElement*, IImage* imout);
  
  /*!@brief Computes the superior gradient of the input image imin, with the structuring element se, and places the
   * results inside imout
   *
   * @author Raffi Enficiaud
   */
  YLLMM_ yaRC gradient_sup(const IImage* imin, const IStructuringElement*, IImage* imout);
 
   /*!@brief Computes the inferior gradient of the input image imin, with the structuring element se, and places the
   * results inside imout
   *
   * @author Raffi Enficiaud
   */
  YLLMM_ yaRC gradient_inf(const IImage* imin, const IStructuringElement*, IImage* imout);
//! @} doxygroup: llm_grp     
   }
}

#endif /* YAYI_LOWLEVEL_MORPHOLOGY_GRADIENT_HPP__ */
