#ifndef YAYI_COLORPROCESS_LUMA_T_HPP__
#define YAYI_COLORPROCESS_LUMA_T_HPP__


#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiCommon/common_constants.hpp>
#include <yayiCommon/common_errors.hpp>

/*!@file
 * This file contains the transformations to luminance according to 2 video standards.
 * @author Raffi Enficiaud
 */

namespace yayi
{
  /*!@addtogroup pp_color_details_grp
   *
   * @{
   */

  //! Extracts the luminance from an RGB image, according to Rec 601
  template<class pixel_in_t, class pixel_out_t>
  struct s_RGB_to_L601 : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    pixel_out_t operator()(pixel_in_t const& u) const YAYI_THROW_DEBUG_ONLY__
    {
      static const yaF_simple c1 = 0.2989f, c2 = 0.5866f, c3 = 0.1145f;
      DEBUG_ASSERT(static_cast<pixel_out_t>(c1 * u.a + c2 * u.b + c3 * u.c) <= std::numeric_limits<pixel_out_t>::max(), "Overflow problem in the transformation");
      return static_cast<pixel_out_t>(c1 * u.a + c2 * u.b + c3 * u.c);
    }
  };

  template <class image_in_, class image_out_>
  yaRC color_RGB_to_L601_t(const image_in_& imin, image_out_& imo)
  {
    typedef s_RGB_to_L601<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op;
    return op_processor(imin, imo, op);
  }


  //! Extracts the luminance from an RGB image, according to Rec 709 (HDTV/D65)
  template<class pixel_in_t, class pixel_out_t >
  struct s_RGB_to_L709 : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    pixel_out_t operator()(pixel_in_t const& u) const YAYI_THROW_DEBUG_ONLY__
    {
      static const yaF_simple c1 = 0.2126f, c2 = 0.7152f, c3 = 0.0722f;
      // there should not be any overflow
      DEBUG_ASSERT(static_cast<pixel_out_t>(c1 * u.a + c2 * u.b + c3 * u.c) <= std::numeric_limits<pixel_out_t>::max(), "Overflow problem in the transformation");
      return static_cast<pixel_out_t>(c1 * u.a + c2 * u.b + c3 * u.c);
    }
  };

  template <class image_in_, class image_out_>
  yaRC color_RGB_to_L709_t(const image_in_& imin, image_out_& imo)
  {
    typedef s_RGB_to_L709<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op;
    return op_processor(imin, imo, op);
  }

  //! @} doxygroup: pp_color_details_grp
}

#endif /* YAYI_COLORPROCESS_LUMA_T_HPP__ */
