#ifndef YAYI_COMPARE_HPP__
#define YAYI_COMPARE_HPP__

/*!@file
 * This file contains the image comparison stub functions
 * @author Raffi Enficiaud
 */

#include <yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>

namespace yayi
{
  /*!@defgroup pp_comp_grp Comparisons of images
   * @ingroup pp_grp
   *
   * @{
   */

  //! Returns a pixel wise comparison of imin with lower and upper bound. For each pixel, assigns true_value to imout(x) if imin(x) is in [lower_bound, upper_bound], false_value otherwise.
  YPix_ yaRC image_threshold(const IImage* imin, variant const &lower_bound, variant const &upper_bound, variant const &true_value, variant const &false_value, IImage* imout);

  //! Transforms each pixel of the image imin according to the lookup table map_lut. If a pixel is not inside the lut, then use the default value.
  YPix_ yaRC image_lookup_transform(const IImage* imin, variant const &map_lut, variant const &default_value, IImage* imout);

  //! Returns a pixel wise comparison of imin with value. For each pixel, assigns true_value or false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_s(const IImage* imin, comparison_operations c, variant value, variant true_value, variant false_value, IImage* imout);

  //! Returns a pixel wise comparison of imin1 with imin2. For each pixel, assigns true_value or false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_i(const IImage* imin1, comparison_operations c, const IImage* imin2, variant true_value, variant false_value, IImage* imout);

  //! Returns a pixel wise comparison of imin1 with value. For each pixel, assigns the corresponding pixel of im_true_value or false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_si(const IImage* imin1, comparison_operations c, variant value, const IImage* im_true_value, variant false_value, IImage* imout);

  //! Returns a pixel wise comparison of imin1 with imin2. For each pixel, assigns the corresponding pixel of im_true_value or false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_ii(const IImage* imin1, comparison_operations c, const IImage* imin2, const IImage* im_true_value, variant false_value, IImage* imout);

  //! Returns a pixel wise comparison of imin1 with imin2. For each pixel, assigns the corresponding pixel of im_true_value or im_false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_iii(const IImage* imin1, comparison_operations c, const IImage* imin2, const IImage* im_true_value, const IImage* im_false_value, IImage* imout);

  //! Returns a pixel wise comparison of imin1 with the constant value. For each pixel, assigns the corresponding pixel of im_true_value or im_false_value into imout, according to the comparison result.
  YPix_ yaRC image_compare_sii(const IImage* imin1, comparison_operations c, variant value, const IImage* im_true_value, const IImage* im_false_value, IImage* imout);

  //! @}
}

#endif /* YAYI_COMPARE_HPP__ */
