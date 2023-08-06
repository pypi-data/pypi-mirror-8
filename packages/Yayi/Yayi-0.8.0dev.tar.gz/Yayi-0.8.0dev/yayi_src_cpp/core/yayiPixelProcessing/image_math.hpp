#ifndef YAYI_PIXEL_IMAGE_MATH_HPP__
#define YAYI_PIXEL_IMAGE_MATH_HPP__

#include <yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>


/*!@file
 * This file contains several mathematical function (log, power, sqrt, random...)
 */

namespace yayi
{
  /*!@defgroup pp_maths_grp Mathemetical transformation of pixels.
   * @ingroup pp_grp
   * @brief Mathematical transformations.
   *
   * This class of transformation are all unary operators (involving one input).
   *
   * @{
   */


  /*!@brief Computes the logarithm of each pixels of the image
   * @author Raffi Enficiaud
   */
  YPix_ yaRC logarithm(const IImage *imin, IImage *imout);

  /*!@brief Computes the exponential of each pixels of the image
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC exponential(const IImage *imin, IImage *imout);

  /*!@brief Computes the power of each pixels of the image
   * @param[in] imin image interface
   * @param[in] var exponent
   * @param[out] imout image interface
   * @author Raffi Enficiaud
   */
  YPix_ yaRC power(const IImage *imin, const variant& var, IImage *imout);

  /*!@brief Computes the square of each pixels of the image
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC square(const IImage *imin, IImage *imout);

  /*!@brief Computes the square root of each pixels of the image
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC square_root(const IImage *imin, IImage *imout);

  /*!@brief Generates the pixels of the image as being drawn from a gaussian distribution
   * with zero mean and unary variance
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC generate_gaussian_random(IImage* imin, yaF_double mean = 0., yaF_double std_deviation = 1.);

  //! @} doxygroup: pp_maths_grp

}

#endif

