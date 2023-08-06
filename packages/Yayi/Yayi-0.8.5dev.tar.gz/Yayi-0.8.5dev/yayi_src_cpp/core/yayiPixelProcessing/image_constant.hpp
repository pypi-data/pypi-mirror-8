#ifndef YAYI_PIXEL_IMAGE_CONSTANT_HPP__
#define YAYI_PIXEL_IMAGE_CONSTANT_HPP__

#include <yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>


namespace yayi
{
  /*!@defgroup pp_const_grp Initialisations and generation of images.
   * @ingroup pp_grp
   * @brief
   * @{
   */

  /*!@brief Sets an image to a constant value
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC constant(const variant&, IImage* imin);


  /*!@brief Sets the window of an image to a constant value
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC constant(const variant&, const variant &rect, IImage* imin);

  //! @} doxygroup: pp_const_grp

}

#endif

