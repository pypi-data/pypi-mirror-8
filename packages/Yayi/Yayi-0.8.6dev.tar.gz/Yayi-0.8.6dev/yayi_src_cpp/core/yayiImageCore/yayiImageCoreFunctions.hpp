#ifndef YAYI_IMAGE_CORE_FUNCTIONS_HPP__
#define YAYI_IMAGE_CORE_FUNCTIONS_HPP__

/*!@file
 * This file defines some utility functions on the images
 * @author Raffi Enficiaud
 */

#include <yayiImageCore/include/yayiImageCore.hpp>

namespace yayi {
  /*!@addtogroup image_utilities_core
   * @{
   */

  /*!@brief Returns the same image as im
   *
   * The returned image is of the same type and dimension of the input image, and is allocated
   * if im is allocated.
   *
   * @note the content of the image is not copied. Consider the @ref copy function.
   * @see copy
   */
  YCor_ IImage* GetSameImage(const IImage* const &im);

  /*!@brief Returns an image with the same geometrical properties than im, but with the type of pixels set to t
   *
   * @note the content of the image is not copied nor casted.
   */
  YCor_ IImage* GetSameImage(const IImage* const &im, const type& t);

  //!@} //addtogroup image_utilities_core
}

#endif
