#ifndef YAYI_PIXEL_IMAGE_COPY_HPP__
#define YAYI_PIXEL_IMAGE_COPY_HPP__

#include <yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>


namespace yayi
{
  /*!@defgroup pp_copy_grp Copy
   * @ingroup pp_grp
   *
   * @{
   */

  /*!@brief Copies and casts an image into another.
   *
   * The function copies the input image into the output image. The images are not required to be of the same pixel type. In that case, a transformation should
   * exists from the input to the output pixel type (eg 8bits char to float, float to short, but float to pixel_3 float not allowed). The images should
   * however have the same dimensions for the coordinate system. It is not required that the images have the same number of pixels: in that case, the
   * minimum number of pixels are copied.
   *
   * @param[in] imin input image
   * @param[out] imout output image
   * @returns yaRC_ok on success, an error code otherwise.
   *
   * @pre imin and imout are allocated
   * @note if the images have different coordinate system, consider the windowed version of copy.
   * @author Raffi Enficiaud
   */
  YPix_ yaRC copy(const IImage* imin, IImage* imout);

  /*!@brief Copies and casts a window of an image into a window of another image
   *
   * @param[in] imin the input image
   * @param[in] rectin the input window, stored in a variant
   * @param[in] rectout the output window, stored in a variant
   * @param[out] imout the input image
   *
   * This function may also be used to copy slices of an image into an image of lower dimension.
   *
   * @note the windows do not have to be of the same size or dimension. The copy will stop at after having
   * copied the minimum number of pixels.
   * @note the input and output windows should be of the same dimension as their corresponding images (eg dimension 3 for both
   * imin and rectin).
   * @author Raffi Enficiaud
   */
  YPix_ yaRC copy(const IImage* imin, const variant &rectin, const variant &rectout, IImage* imout);
  //! @}
}

#endif

