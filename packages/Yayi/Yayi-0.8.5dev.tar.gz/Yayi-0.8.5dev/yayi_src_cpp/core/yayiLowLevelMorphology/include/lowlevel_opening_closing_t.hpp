#ifndef YAYI_LOWLEVEL_MORPHOLOGY_OPEN_CLOSE_T_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_OPEN_CLOSE_T_HPP__

/*!@file
 * 
 */

#include <yayiLowLevelMorphology/include/lowlevel_erosion_dilation_t.hpp>


namespace yayi { namespace llmm {
/*!
 * @addtogroup llm_details_grp
 *
 *@{
 */    
  
  //! Opening of imin into imout, using structuring element se
  //! The structuring element is today supposed to meet the transposable concept. Otherwise,
  //! it will be changed in the near future to the Minkowski subtraction.
  template <class image_in_t, class se_t, class image_out_t>
  yaRC open_image_t(const image_in_t& imin, const se_t& se, image_out_t& imout)
  {
    image_in_t imtemp;
    imtemp.set_same(imin);
    yaRC res = erode_image_t(imin, se, imtemp);
    if(res != yaRC_ok)
      return res;
      
    res = dilate_image_t(imtemp, se.transpose(), imout);
    return res;  
  }

  //! Closing of imin into imout, using structuring element se
  //! The structuring element is today supposed to meet the transposable concept. Otherwise,
  //! it will be changed in the near future to the Minkowski subtraction.
  template <class image_in_t, class se_t, class image_out_t>
  yaRC close_image_t(const image_in_t& imin, const se_t& se, image_out_t& imout)
  {
    image_in_t imtemp;
    imtemp.set_same(imin);
    yaRC res = dilate_image_t(imin, se, imtemp);
    if(res != yaRC_ok)
      return res;
      
    res = erode_image_t(imtemp, se.transpose(), imout);
    return res;
  
  }


//! @} doxygroup: llm_details_grp        
}}

#endif /* YAYI_LOWLEVEL_MORPHOLOGY_OPEN_CLOSE_T_HPP__ */
