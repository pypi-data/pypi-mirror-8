#ifndef YAYI_PIXEL_PROCESSING_MAIN_HPP__
#define YAYI_PIXEL_PROCESSING_MAIN_HPP__



#include <yayiCommon/common_config.hpp>


#ifdef YAYI_EXPORT_PIXELPROC_
#define YPix_ MODULE_EXPORT
#else
#define YPix_ MODULE_IMPORT
#endif


namespace yayi
{
  /*!@defgroup pp_grp Pixel Processing
   * @brief Pixel processing on images
   *
   * Pixel processing means that there is no neighborhood involved in the processings. The operations are hence
   * pixel to pixel, involving 1 to N images. The class of operations is hence rather large, from image basic arithmetics
   * and logical combinations, to color transforms, or random image generation.
   * @{
   */

  //! Comparison types
  typedef enum e_comparison_operations
  {
    e_co_equal,                 //!< test for equality
    e_co_different,             //!< test for inequality
    e_co_superior,              //!< test if left is superior (or equal) than right
    e_co_superior_strict,       //!< test if left is superior (and inequal) than right
    e_co_inferior,              //!< test if left is inferior (or equal) than right
    e_co_inferior_strict        //!< test if left is inferior (and inequal) than right
  } comparison_operations;
  //! @}
}


#endif

