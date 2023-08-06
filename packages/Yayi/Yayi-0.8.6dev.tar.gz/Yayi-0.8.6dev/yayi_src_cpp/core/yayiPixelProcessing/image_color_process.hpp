#ifndef YAYI_COLOR_PROCESS_HPP__
#define YAYI_COLOR_PROCESS_HPP__


/*!@file
 * This file contains the declaration for color space conversion
 * @author Raffi Enficiaud
 */


#include <yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>

#include <algorithm>
#include <functional>


namespace yayi
{
  /*!@defgroup pp_color_grp Color Processing
   * @ingroup pp_grp
   * @brief Image color conversions.
   * 
   * Mainly 3 classes of transformations are distinguished: the "video" color space transforms (YUV and so on),
   * the colorimetric color space transforms (XYZ, Lab), and the color space for human interpretation (HLS, etc..)
   *@{
   */
   
  /*!Transforms the image from RGB color space to HLS, defined with the \f$\ell_1\f$ norm
   * References: Jesus Angulo Lopez's PhD, Raffi Enficiaud's PhD
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_RGB_to_HLS_l1(const IImage* imin, IImage* imout);

  /*!Transforms the image from HLS \f$\ell_1\f$ color space to RGB
   * References: Jesus Angulo Lopez's PhD, Raffi Enficiaud's PhD
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_HLS_l1_to_RGB(const IImage* imin, IImage* imout);



  /*!Transforms a color image in RGB into a luminosity image
   * 
   * The transformation is made according to the YUV L 709 specifications.
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_RGB_to_L601(const IImage* imin, IImage* imout);


  /*!Transforms a color image in RGB into a luminosity image
   * 
   * The transformation is made according to the YUV L 709 specifications.
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_RGB_to_L709(const IImage* imin, IImage* imout);



  /*!Transforms a color image in RGB colour space to a colour image in YUV colour space
   * 
   * The transformation is made according to the YUV specification.
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_RGB_to_YUV(const IImage* imin, IImage* imout);

  /*!Transforms a color image in YUV colour space to a colour image in RGB colour space
   * 
   * The reverse transformation is made according to the YUV specification.
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_YUV_to_RGB(const IImage* imin, IImage* imout);




  /*!Transforms a color image in RGB colour space to a colour image in XYZ colour space, assuming
   * the RGB space is CIE-RGB (reference white E, CIE rgb primaries, gamma 2.2)
   * 
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_CIERGB_to_XYZ_refWE(const IImage* imin, IImage* imout);

  /*!Transforms a color image in XYZ colour space to a colour image in RGB colour space, assuming
   * the RGB space is CIE-RGB (reference white E, CIE rgb primaries, gamma 2.2)
   * 
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_XYZ_to_CIERGB_refWE(const IImage* imin, IImage* imout);

  /*!Transforms a color image in RGB colour space to a colour image in XYZ colour space, assuming
   * the RGB space is AdobeRGB (reference white D65, AdobeRGB rgb primaries, gamma 2.2)
   * 
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_AdobeRGB_to_XYZ_refWD65(const IImage* imin, IImage* imout);

  /*!Transforms a color image in XYZ colour space to a colour image in RGB colour space, assuming
   * the RGB space is AdobeRGB (reference white D65, AdobeRGB rgb primaries, gamma 2.2)
   * 
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_XYZ_to_AdobeRGB_refWD65(const IImage* imin, IImage* imout);

  /*!Transforms a color image in RGB colour space to a colour image in XYZ colour space, assuming
   * the RGB space is sRGB (reference white D65, CIE rgb primaries, gamma 2.4, specific linearising)
   * 
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_sRGB_to_XYZ_refWD65(const IImage* imin, IImage* imout);

  /*!Transforms a color image in XYZ colour space to a colour image in sRGB colour space, assuming
   * the RGB space is sRGB (reference white D65, CIE rgb primaries, gamma 2.4, specific linearising)
   * 
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_XYZ_to_sRGB_refWD65(const IImage* imin, IImage* imout);







  /*!Transforms a color image in XYZ colour space to a colour image in LAB colour space, using 
   * "E" as reference white.
   * 
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_XYZ_to_LAB_refWE(const IImage* imin, IImage* imout);

  /*!Transforms a color image in LAB colour space to a colour image in XYZ colour space, using 
   * "E" as reference white.
   * 
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_LAB_to_XYZ_refWE(const IImage* imin, IImage* imout);
  
  /*!Transforms a color image in XYZ colour space to a colour image in LAB colour space, using 
   * "A" as reference white.
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_XYZ_to_LAB_refWA(const IImage* imin, IImage* imout);
  
  /*!Transforms a color image in LAB colour space to a colour image in XYZ colour space, using 
   * "A" as reference white.
   * 
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_LAB_to_XYZ_refWA(const IImage* imin, IImage* imout);

  /*!Transforms a color image in XYZ colour space to a colour image in LAB colour space, using 
   * "D65" as reference white.
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_XYZ_to_LAB_refWD65(const IImage* imin, IImage* imout);

  /*!Transforms a color image in LAB colour space to a colour image in XYZ colour space, using 
   * "D65" as reference white.
   * 
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_LAB_to_XYZ_refWD65(const IImage* imin, IImage* imout);
  
  /*!Transforms a color image in XYZ colour space to a colour image in LAB colour space, using 
   * "D75" as reference white.
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_XYZ_to_LAB_refWD75(const IImage* imin, IImage* imout);

  /*!Transforms a color image in LAB colour space to a colour image in XYZ colour space, using 
   * "D75" as reference white.
   * 
   * @author Raffi Enficiaud
   */
  YPix_ yaRC color_LAB_to_XYZ_refWD75(const IImage* imin, IImage* imout);


  //! @} doxygroup: pp_color_grp

}

#endif // YAYI_COLOR_PROCESS_HPP__
