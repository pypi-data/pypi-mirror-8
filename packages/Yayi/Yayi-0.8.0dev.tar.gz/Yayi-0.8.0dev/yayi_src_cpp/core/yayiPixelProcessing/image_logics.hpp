#ifndef YAYI_PIXEL_IMAGE_LOGIC_HPP__
#define YAYI_PIXEL_IMAGE_LOGIC_HPP__

/*!@file
 * This file defines the logical/bitwise operations on images
 */

#include <yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>

namespace yayi
{
  /*!@defgroup pp_logics_grp Logical and bitwise operations
   * @ingroup pp_grp
   *
   *@{
   */
  //! Performs a logical "not" on the input image
  YPix_ yaRC image_bitwise_not(const IImage* imin, IImage* imout);

  //! Performs a logical "and" between two images
  YPix_ yaRC image_bitwise_and(const IImage* imin1, const IImage* imin2, IImage* imout);

  //! Performs a logical "or" between two images
  YPix_ yaRC image_bitwise_or(const IImage* imin1, const IImage* imin2, IImage* imout);

  //! @}
}



#endif /* YAYI_PIXEL_IMAGE_LOGIC_HPP__ */
