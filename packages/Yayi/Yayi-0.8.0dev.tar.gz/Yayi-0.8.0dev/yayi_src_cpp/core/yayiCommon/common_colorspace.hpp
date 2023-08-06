#ifndef YAYI_COMMON_COLORSPACE_HPP__
#define YAYI_COMMON_COLORSPACE_HPP__

/*!@file
 * This file contains the necessary elements for colour information. It contains also several functions for the computation
 * of spectral information (blackbody, gamut)...
 *
 * @author Raffi Enficiaud
 */

#include <yayiCommon/common_types.hpp>
#include <yayiCommon/common_constants.hpp>

namespace yayi
{
  /*!@defgroup common_color_grp Colour 
   * @brief Color spaces and utilities.
   * @ingroup common_grp
   * @{
   */


  //! Standard observer tables structure
  struct s_standard_observer_data
  {
    yaUINT32      nanometer;
    yaF_double    x,y,z;
  };

  //! The CIE 1931 2 degrees standard observer table (within the range [380, 780] nm).
  YCom_ extern s_standard_observer_data const xyz_CIE_1931[];


  /*!@brief Structure encoding the colour space (which should be associated to an image)
   *
   * @author Raffi Enficiaud
   */
  struct s_yaColorSpace
  {
    //! @internal
    typedef s_yaColorSpace this_type;
    
    //! The major category of the color space
    typedef enum e_colorspace_major
    {
      ecd_undefined,    //!< Undefined color space
      ecd_rgb,          //!< Color space is of class RGB
      ecd_hls,          //!< Color space is of class HLS
      ecd_lab,          //!< Color space is of class La*b*
      ecd_xyz,          //!< Color space is of class XYZ
      ecd_xyY,          //!< Color space is of class xyY
      ecd_yuv           //!< Color space is of class YUV
    } yaColorSpaceMajor;

    //! The minor category of the color space (variation/implementation of the major color space)
    typedef enum e_colorspace_minor
    {
      ecdm_undefined,   //!< Undefined subcategory
      ecdm_hls_l1,      //!< The HLS color space follows the \f$\ell_1\f$ norm
      ecdm_hls_trig     //!< The HLS color space follows the trigonometric definition
    } yaColorSpaceMinor;

    //! Standard illuminants
    typedef enum e_illuminant
    {
      ei_undefined,     //!< Undefined illuminant
      ei_d50,           //!< D50 illuminant
      ei_d55,           //!< D55 illuminant
      ei_d65,           //!< D65 illuminant
      ei_d75,           //!< D75 illuminant
      ei_A,             //!< Illuminant CIE "A" definition
      ei_B,             //!< Illuminant CIE "B" definition
      ei_C,             //!< Illuminant CIE "C" definition
      ei_E,             //!< Illuminant CIE "E" definition
      ei_blackbody      //!< The illuminant is defined from the corresponding blackbody radiator temperature
    } yaIlluminant;

    //! RGB standard primaries used to define the RGB color space
    typedef enum e_rgb_primaries
    {
      ergbp_undefined,  //!< Undefined primaries
      ergbp_CIE,        //!< CIE standard primaries
      ergbp_sRGB,       //!< sRGB primaries
      ergbp_AdobeRGB,   //!< Adobe RGB primaries
      ergbp_AppleRGB,   //!< Apple RGB primaries
      ergbp_NTSCRGB,    //!< NTSC primaries
      ergbp_SecamRGB    //!< Secam primaries
    } yaRGBPrimary;

    yaColorSpaceMajor cs_major;
    yaColorSpaceMinor cs_minor;
    yaIlluminant      illuminant;
    yaRGBPrimary      primary;
    
    
    //! Color space equality operator
    bool operator==(this_type const & r) const
    {
      return cs_major == r.cs_major &&
        cs_minor == r.cs_minor &&
        illuminant == r.illuminant &&
        primary == r.primary;
    }

    //! Stringifier
    YCom_ operator string_type() const throw();
    
    //! Streaming
    template <class stream_t>
    friend stream_t& operator<<(stream_t& o, const this_type& t) {
      o << t.operator string_type(); return o;
    }
    
    
    //! Default constructor
    s_yaColorSpace() 
      : cs_major(ecd_undefined), cs_minor(ecdm_undefined), illuminant(ei_undefined), primary(ergbp_undefined) {}
    
    //! Direct constructor
    s_yaColorSpace(yaColorSpaceMajor mm, yaIlluminant ill = ei_undefined, yaRGBPrimary prim = ergbp_undefined, yaColorSpaceMinor m = ecdm_undefined) 
      : cs_major(mm), cs_minor(m), illuminant(ill), primary(prim) {}
    
  };
  
  //! The type used for color space definition
  typedef s_yaColorSpace yaColorSpace;

  // Predefined color spaces
  const static yaColorSpace 
    //! sRGB colorspace
    cs_sRGB(yaColorSpace::ecd_rgb),
    //! CIE RGB colorspace
    cs_CIERGB(yaColorSpace::ecd_rgb, yaColorSpace::ei_d65, yaColorSpace::ergbp_CIE),
    //! HLS with l1 norm colorspace
    cs_HLSl1(yaColorSpace::ecd_hls, yaColorSpace::ei_undefined, yaColorSpace::ergbp_undefined, yaColorSpace::ecdm_hls_l1)
  ;
  
  
  /*!@brief Returns the radiation of the black-body at the specified wavelenght and temperature.
   * The wavelenght is in nanometer and the temperature is in Kelvin.
   * 
   * @param[in] wavelenght_nanometer The wavelenght, in nanometer
   * @param[in] temperature temperature, in Kelvin
   *  
   * @return the radiation of the black-body at the specified wavelenght and temperature. The returned value
   * may be huge. Consider the blackbody radiation normalized by a temperature.
   * @author Raffi Enficiaud   
   */
  YCom_ yaF_double blackbody_radiation(yaUINT32 const wavelenght_nanometer, yaUINT32 temperature);


  /*!@brief Returns the radiation of the black-body at the specified wavelenght and temperature, normalized by
   * the radiation at a specific temperature.
   
   * The wavelenght is in nanometer and the temperature is in Kelvin.
   * 
   * @param[in] wavelenght_nanometer The wavelenght, in nanometer
   * @param[in] temperature temperature, in Kelvin
   * @param[in] temperature_normalized temperature used for normalization, in Kelvin
   *  
   * @return the radiation of the black-body at the specified wavelenght and temperature, normalized by radiation of the black body at a
   * specific temperature.
   * @author Raffi Enficiaud   
   */
  YCom_ yaF_double blackbody_radiation_normalized(yaUINT32 const wavelenght_nanometer, yaUINT32 temperature, yaUINT32 temperature_normalized);


  


  //! @} // defgroup common_color_grp

}
 
 
#endif /* YAYI_COMMON_COLORSPACE_HPP__ */
