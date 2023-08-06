#ifndef YAYI_LOWLEVEL_GEODESICS_T_HPP__
#define YAYI_LOWLEVEL_GEODESICS_T_HPP__


/*!@file
 * This file defines geodesic erosions and dilations implementations
 * @author Raffi Enficiaud
 */

#include <yayiLowLevelMorphology/include/lowlevel_erosion_dilation_t.hpp>
#include <yayiPixelProcessing/include/image_arithmetics_t.hpp>

namespace yayi { namespace llmm {
  /*!@defgroup llm_details_geodesic_grp Geodesic elementary operations
   * @ingroup  llm_details_grp
   * 
   * @{
   */
  
  template <class image_in, class image_mask_in, class se_t, class image_out>
  yaRC geodesic_dilate_image_t(const image_in& imin, const image_mask_in& immask, const se_t& se, image_out& imout)
  {
    image_in imtemp;
    imtemp.set_same(imin);
    yaRC res = infimum_images_t(imin, immask, imtemp);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error from infimum : " << res);
      return res;
    }
    res = dilate_image_t(imtemp, se, imout);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error from dilate : " << res);
      return res;
    }

    return infimum_images_t(imout, immask, imout);
  }  


  template <class image_in, class image_mask_in, class se_t, class image_out>
  yaRC geodesic_erode_image_t(const image_in& imin, const image_mask_in& immask, const se_t& se, image_out& imout)
  {
    image_in imtemp;
    imtemp.set_same(imin);
    yaRC res = supremum_images_t(imin, immask, imtemp);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error from infimum : " << res);
      return res;
    }
    res = erode_image_t(imtemp, se, imout);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error from dilate : " << res);
      return res;
    }

    return supremum_images_t(imout, immask, imout);
  }    
  
  //! @}
}}

#endif /* YAYI_LOWLEVEL_GEODESICS_T_HPP__ */
