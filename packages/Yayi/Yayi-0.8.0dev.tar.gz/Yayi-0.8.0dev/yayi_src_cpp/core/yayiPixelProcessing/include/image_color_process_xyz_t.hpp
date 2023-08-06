#ifndef YAYI_COLORPROCESS_XYZ_T_HPP__
#define YAYI_COLORPROCESS_XYZ_T_HPP__


#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiCommon/common_constants.hpp>
#include <yayiCommon/common_colorspace.hpp>
#include <yayiPixelProcessing/include/image_math_t.hpp>

/*!@file
 * This file contains the transformations to xyz spaces.
 * @author Raffi Enficiaud
 */

namespace yayi
{
  /*!@addtogroup pp_color_details_grp
   *
   * @{
   */

  //! Transforms a pixel 3 according to a matrix
  //! Currently only pixel3 are supported (9 elements in the matrix)
  template<class pixel_in_t, class pixel_out_t, class coefficient_t = yaF_simple>
  struct s_apply_flat_matrix : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    coefficient_t const * const coefficients;
    s_apply_flat_matrix(coefficient_t const * coefficients_) : coefficients(coefficients_) {}
    pixel_out_t operator()(pixel_in_t const& u) const throw()
    {
      return
        pixel_out_t(
          typename pixel_out_t::value_type(coefficients[0] * u.a + coefficients[1] * u.b + coefficients[2] * u.c),
          typename pixel_out_t::value_type(coefficients[3] * u.a + coefficients[4] * u.b + coefficients[5] * u.c),
          typename pixel_out_t::value_type(coefficients[6] * u.a + coefficients[7] * u.b + coefficients[8] * u.c));
    }
  };

  //! Transforms a pixel 3 by applying a gamma correction followed by a matrix multiplication (see @c s_matrix_transform)
  //! Currently only pixel3 are supported (9 elements in the matrix)
  template<
    class pixel_in_t,
    class pixel_out_t,
    class linearisation_t = s_power<pixel_in_t, pixel_out_t>,
    class coefficient_t = yaF_simple
    >
  struct s_apply_flat_matrix_with_gamma_correction : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    linearisation_t const linear_op;
    s_apply_flat_matrix<pixel_out_t, pixel_out_t, coefficient_t> const matrix_op;

    s_apply_flat_matrix_with_gamma_correction(double gamma_, coefficient_t const * coefficients_) : linear_op(gamma_), matrix_op(coefficients_) {}
    pixel_out_t operator()(pixel_in_t const& u) const throw()
    {
      return matrix_op(linear_op(u));
    }
  };

  //! Inverse transforms a pixel 3 by applying a gamma correction followed by a matrix multiplication (see s_matrix_transform, s_apply_flat_matrix_with_gamma_correction)
  //! This is exactly the inverse of the transform given by @c s_apply_flat_matrix_with_gamma_correction, but
  //! the values of the matrix are not computed within this function.
  template<
    class pixel_in_t,
    class pixel_out_t,
    class linearisation_inverse_t = s_power<pixel_in_t, pixel_out_t>,
    class coefficient_t = yaF_simple>
  struct s_apply_inverse_flat_matrix_with_gamma_correction : public std::unary_function<pixel_in_t, pixel_out_t>
  {
    linearisation_inverse_t const linear_op;
    s_apply_flat_matrix<pixel_out_t, pixel_out_t, coefficient_t> const matrix_op;

    s_apply_inverse_flat_matrix_with_gamma_correction(double gamma_, coefficient_t const * coefficients_) : linear_op(gamma_), matrix_op(coefficients_) {}
    pixel_out_t operator()(pixel_in_t const& u) const throw()
    {
      return linear_op(matrix_op(u));
    }
  };


  //! Transforms an RGB image into an XYZ image, considering the input RGB space as CIE-RGB (CIE RGB primaries, ref white E, gamma 2.2)
  template <class image_in_, class image_out_>
  yaRC color_CIERGB_to_XYZ_refWE_t(const image_in_& imin, image_out_& imo)
  {
    static const yaF_simple coefficients[] =
    {
      0.4887180f, 0.3106803f, 0.2006017f,
      0.1762044f, 0.8129847f, 0.0108109f,
      0.0000000f, 0.0102048f, 0.9897952f
    };
    static const yaF_double gamma = 2.2;

    typedef s_apply_flat_matrix_with_gamma_correction<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(gamma, coefficients);
    return op_processor(imin, imo, op);
  }

  //! Inverse transforms from RGB to XYZ, considering the output RGB space as CIE-RGB (CIE RGB primaries, ref white E, gamma 2.2)
  template <class image_in_, class image_out_>
  yaRC color_XYZ_to_CIERGB_refWE_t(const image_in_& imin, image_out_& imo)
  {
    static const yaF_simple coefficients[] =
    {
       2.3706743f, -0.9000405f, -0.4706338f,
      -0.5138850f,  1.4253036f,  0.0885814f,
       0.0052982f, -0.0146949f,  1.0093968f
    };
    static const yaF_double gamma = 1./2.2;

    typedef s_apply_inverse_flat_matrix_with_gamma_correction<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(gamma, coefficients);
    return op_processor(imin, imo, op);
  }


  //! Transforms an RGB image into an XYZ image, considering the input RGB space as Adobe-RGB (Adobe RGB primaries, ref white D65, gamma 2.2)
  template <class image_in_, class image_out_>
  yaRC color_AdobeRGB_to_XYZ_refWD65_t(const image_in_& imin, image_out_& imo)
  {
    static const yaF_simple coefficients[] =
    {
      0.5767309f, 0.1855540f, 0.1881852f,
      0.2973769f, 0.6273491f, 0.0752741f,
      0.0270343f, 0.0706872f, 0.9911085f
    };
    static const yaF_double gamma = 2.2;

    typedef s_apply_flat_matrix_with_gamma_correction<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(gamma, coefficients);
    return op_processor(imin, imo, op);
  }

  //! Inverse transform an RGB image into an XYZ image, considering the output RGB space as Adobe-RGB (Adobe RGB primaries, ref white D65, gamma 2.2)
  template <class image_in_, class image_out_>
  yaRC color_XYZ_to_AdobeRGB_refWD65_t(const image_in_& imin, image_out_& imo)
  {
    static const yaF_simple coefficients[] =
    {
       2.0413690f, -0.5649464f, -0.3446944f,
      -0.9692660f,  1.8760108f,  0.0415560f,
       0.0134474f, -0.1183897f,  1.0154096f
    };
    static const yaF_double gamma = 1./2.2;

    typedef s_apply_inverse_flat_matrix_with_gamma_correction<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(gamma, coefficients);
    return op_processor(imin, imo, op);
  }



    //! sRGB linearising operator
  template <class T>
  struct s_srgb_linearising : public std::unary_function<T, yaF_double>
  {
    //! Default constructor (for specialising in multichannel versions)
    s_srgb_linearising(){}

    template <class U>
    s_srgb_linearising(U const&){} // dummy constructor, avoid

    yaF_double operator()(T const& value) const
    {
            static const yaF_simple a = 0.055f;
      return value > 0.04045f ? std::pow(T((value+a) / (1+a)), T(2.4f)) : value/12.92f;
    }
  };

    //! sRGB inverse linearising operator (special case for multiple channels)
  template <class T>
  struct s_srgb_linearising< s_compound_pixel_t< T,  mpl::int_<3> > >
    : public std::unary_function<s_compound_pixel_t< T,  mpl::int_<3> > const&, s_compound_pixel_t< yaF_double,  mpl::int_<3> > >
  {
    typedef s_srgb_linearising< s_compound_pixel_t< T,  mpl::int_<3> > > this_type;
    template <class U>
    s_srgb_linearising(U const&){} // dummy constructor, avoid

    typedef s_srgb_linearising<T> op_t;
    op_t op;

    typename this_type::result_type operator()(typename this_type::argument_type value) const
    {
            return typename this_type::result_type(op(value.a), op(value.b), op(value.c));
    }
  };



  //! Transforms an RGB image into an XYZ image, considering the input RGB space as sRGB (sRGB primaries, ref white D65, gamma 2.4, specific linearising)
  template <class image_in_, class image_out_>
  yaRC color_sRGB_to_XYZ_refWD65_t(const image_in_& imin, image_out_& imo)
  {
    static const yaF_simple coefficients[] =
    {
      0.412424f,  0.357579f, 0.180464f,
      0.212656f,  0.715158f, 0.0721856f,
      0.0193324f, 0.119193f, 0.950444f
    };
    static const yaF_double gamma = 0;

    typedef s_apply_flat_matrix_with_gamma_correction<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type,
      s_srgb_linearising<typename image_in_::pixel_type> >  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(gamma, coefficients);
    return op_processor(imin, imo, op);
  }

    //! sRGB inverse linearising operator
  template <class T>
  struct s_srgb_linearising_inverse : public std::unary_function<T, yaF_double>
  {
    //! Default constructor (for specialising in multichannel versions)
    s_srgb_linearising_inverse(){}

    template <class U>
    s_srgb_linearising_inverse(U const&){} // dummy constructor, avoid

    yaF_double operator()(T const& value) const
    {
            static const yaF_simple a = 0.055f;
      return value > 0.0031308f ? (1+a) * std::pow(value, T(0.4166667f)) - a: 12.92f*value; // 0.4166667 = 1/2.4
    }
  };

    //! sRGB inverse linearising operator (special case for multiple channels)
  template <class T>
  struct s_srgb_linearising_inverse< s_compound_pixel_t< T,  mpl::int_<3> > >
    : public std::unary_function<s_compound_pixel_t< T,  mpl::int_<3> > const&, s_compound_pixel_t< yaF_double,  mpl::int_<3> > >
  {
    typedef s_srgb_linearising_inverse< s_compound_pixel_t< T,  mpl::int_<3> > > this_type;
    template <class U>
    s_srgb_linearising_inverse(U const&){} // dummy constructor, avoid

    typedef s_srgb_linearising_inverse<T> op_t;
    op_t op;

    typename this_type::result_type operator()(typename this_type::argument_type value) const
    {
            return typename this_type::result_type(op(value.a), op(value.b), op(value.c));
    }
  };



  //! Transforms an XYZ image into an sRGB image, considering the input RGB space as sRGB (sRGB primaries, ref white D65, gamma 2.4, specific linearising)
  template <class image_in_, class image_out_>
  yaRC color_XYZ_to_sRGB_refWD65_t(const image_in_& imin, image_out_& imo)
  {
    static const yaF_simple coefficients[] =
    {
      3.24071f,  -1.53726f, -0.498571f,
      -0.969258f, 1.87599f, 0.0415557f,
      0.0556352f, -0.203996f, 1.05707f
    };
    static const yaF_double gamma = 0;

    typedef s_apply_inverse_flat_matrix_with_gamma_correction<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type,
      s_srgb_linearising_inverse<typename image_in_::pixel_type> >  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(gamma, coefficients);
    return op_processor(imin, imo, op);
  }


  //! Returns the reference white of a given colorspace in the xyY space
  //! This is useful in case the xyY point is not correctly specified (full black for instance)
  inline bool get_reference_white_xyY(yaColorSpace const &cs)
  {

  }

  //! @} doxygroup: pp_color_details_grp
}

#endif /* YAYI_COLORPROCESS_XYZ_T_HPP__ */
