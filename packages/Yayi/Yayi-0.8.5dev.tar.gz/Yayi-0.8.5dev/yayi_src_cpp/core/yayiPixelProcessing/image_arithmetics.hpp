#ifndef YAYI_PIXEL_IMAGE_ARITHMETIC_HPP__
#define YAYI_PIXEL_IMAGE_ARITHMETIC_HPP__

/*!@file
 * This file defines the arithmetic operations on images
 */

#include <yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>

namespace yayi
{
  /*!@defgroup pp_arih_grp Arithmetics
   * @ingroup pp_grp
   * @{
   */

  //! Adds two images
  YPix_ yaRC image_add(const IImage* imin1, const IImage* imin2, IImage* imout);

  //! Subtracts two images
  YPix_ yaRC image_subtract(const IImage* imin1, const IImage* imin2, IImage* imout);

  //! Subtracts two images, with a lower bound (in case left < right)
  YPix_ yaRC image_subtract_with_lower_bound(const IImage* imin1, const IImage* imin2, const variant& lower_bound, IImage* imout);

  //! Absolute difference of two images
  YPix_ yaRC image_abssubtract(const IImage* imin1, const IImage* imin2, IImage* imout);

  //! Multiplies two images
  YPix_ yaRC image_multiply(const IImage* imin1, const IImage* imin2, IImage* imout);

  //! Adds a contant value to the image
  YPix_ yaRC image_add_constant(const IImage* imin, variant const &c, IImage* imout);

  //! Adds a contant value to the image, with an upper-bound on the addition.
  //! The constant and the upper-bound should be compatible with the images' types.
  YPix_ yaRC image_add_constant_upper_bound(const IImage* imin, variant const &c, variant const &upper_bound, IImage* imout);

  //! Subtracts a contant value from the image
  YPix_ yaRC image_subtract_constant(const IImage* imin, variant const &c, IImage* imout);

  //! Subtracts a contant value from the image with a lower-bound on the subtraction.
  //! The constant and the lower-bound should be compatible with the images' types.
  YPix_ yaRC image_subtract_constant_lower_bound(const IImage* imin, variant const &c, variant const &lower_bound, IImage* imout);

  //! Multiplies an image by a constant value
  YPix_ yaRC image_multiply_constant(const IImage* imin, variant const &c, IImage* imout);

  //! Computes the intersection (infimum) of two images
  YPix_ yaRC image_infimum(const IImage*imin1, const IImage* imin2, IImage* imout);

  //! Computes the union (supremum) of two images
  YPix_ yaRC image_supremum(const IImage*imin1, const IImage* imin2, IImage* imout);

  //! @} doxygroup: pp_arih_grp
}

#endif
