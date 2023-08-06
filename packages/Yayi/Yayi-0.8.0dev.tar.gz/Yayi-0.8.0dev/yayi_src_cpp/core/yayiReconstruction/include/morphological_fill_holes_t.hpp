#ifndef YAYI_MORPHOLOGICAL_FILL_HOLES_T_HPP__
#define YAYI_MORPHOLOGICAL_FILL_HOLES_T_HPP__


/*!@file
 * This file contains the algorithm for morphological hole filling
 *
 */
#include <yayiReconstruction/include/morphological_reconstruction_t.hpp>
#include <yayiPixelProcessing/include/image_borders_t.hpp>
namespace yayi
{
  namespace reconstructions
  {
    /*!@addtogroup reconstruction_details_grp
     *
     * @{
     */
    
    //!@brief Fills the holes of the image using the provided structuring element.
    template <class image_inout_t, class se_t>
    yaRC fill_holes_image_t(const image_inout_t& image_in, const se_t& se, image_inout_t& image_out)
    {
      image_inout_t imtemp;
      yaRC res = imtemp.set_same(image_in);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("Error during the set_same " << res);
        return res;
      }
      
      res = constant_image_t(s_bounds_helper<typename image_inout_t::pixel_type>::max(), imtemp);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("Error during the constant_image_t " << res);
        return res;
      }
    
      res = image_copy_borders_t(image_in, imtemp);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("Error during the constant_image_t " << res);
        return res;
      }
      
      return closing_by_reconstruction_t(imtemp, image_in, se, image_out);
    
    }
    //! @}
  }
}
#endif /* YAYI_MORPHOLOGICAL_FILL_HOLES_T_HPP__ */
