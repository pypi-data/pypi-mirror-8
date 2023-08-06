#ifndef YAYI_LOWLEVEL_MORPHOLOGY_HIT_OR_MISS_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_HIT_OR_MISS_HPP__

/*!@file
 * This file contains the hit-or-miss operations for ordered images, based on the work of
 * Soille and Ronse.
 */

#include <yayiLowLevelMorphology/yayiLowLevelMorphology.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi { namespace llmm {
  /*!@addtogroup llm_grp
   *
   * @{
   */

  /*!@brief Hit or miss operation on images, using the Soille definition.
   *  This function implements the hit-or-miss transform for ordered images in the sense defined by Soille @cite soille:1999.
   *
   *  se_foreground and se_background are the structuring elements that should fit the foreground and the background respectively.
   *  se_background should not contain the center and the two structuring elements should have disjoint support (an error is returned otherwise).
   *
   *  @author Raffi Enficiaud
   */
  YLLMM_ yaRC hit_or_miss_soille(const IImage* imin, const se::IStructuringElement* se_foreground, const se::IStructuringElement* se_background, IImage* imout);

  //! @} doxygroup: llm_grp

}}


#endif /* YAYI_LOWLEVEL_MORPHOLOGY_HIT_OR_MISS_HPP__ */
