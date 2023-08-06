#ifndef YAYI_COLOR_PROCESS_HLS_T_HPP__
#define YAYI_COLOR_PROCESS_HLS_T_HPP__

/*!@file
 * Contains several operations for hue processing and hue related color spaces.
 */

#include <algorithm>
#include <functional>
#include <limits>
#include <boost/mpl/or.hpp>

#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiCommon/common_constants.hpp>


namespace yayi
{
  /*!@addtogroup pp_color_details_grp
   *
   * @{
   */
  
  
  
  //! @internal
  //! Simple metafunction telling if the provided type is floating point.
  template <class T>
  struct s_restrict_on_float_representation
  {
    typedef typename boost::enable_if<typename boost::is_floating_point<T>::type>::type type;
  };


  /*! Transformation from RGB @f$[0, 255]^3@f$ to HLS l1 @f$[0, 2\pi[ \times [0,1] \times [0, 1]@f$.
   * @tparam pixel_in pixel type of the input image
   * @tparam pixel_out pixel type of the output image
   * @tparam enable_if__ sfinae for restricting the instances to floating point.
   */
  template <class pixel_in, class pixel_out, class enable_if__ = void>
    struct s_color_RGB_to_HLSl1 : public std::unary_function<pixel_in, pixel_out>
  {};

  template <class pixel_out_scalar_type>
    struct s_color_RGB_to_HLSl1<
      pixel8u_3,
      s_compound_pixel_t<pixel_out_scalar_type, mpl::int_<3> >,
      typename s_restrict_on_float_representation<pixel_out_scalar_type>::type
      >
    :
    public std::unary_function<pixel8u_3, s_compound_pixel_t<pixel_out_scalar_type, mpl::int_<3> > >
  {

    typedef pixel8u_3 pixel_in;
    typedef typename pixel8u_3::value_type pixel_in_scalar_type;
    typedef yaUINT16 pixel_in_for_calculus;
    typedef s_compound_pixel_t<pixel_out_scalar_type, mpl::int_<3> > pixel_out;

    pixel_out helper(pixel_in_scalar_type min, pixel_in_for_calculus mid, pixel_in_scalar_type max, const unsigned int lambda) const
    {
      pixel_out	 ret;
      const pixel_in_for_calculus max_p_min = max + min;

      // todo: less operations
      ret.b = static_cast<pixel_out_scalar_type>((max_p_min + mid)/3.);
      mid  *= 2;
      ret.c = (max_p_min >= mid) ? max - ret.b : ret.b - min;
      ret.b /= std::numeric_limits<pixel_in_scalar_type>::max();

      if(ret.c == 0)
      {
        ret.a = 0;
        return ret;
      }

      ret.c *= pixel_out_scalar_type(1.5) / std::numeric_limits<pixel_in_scalar_type>::max(); // 3/2

      ret.a  = mid;
      ret.a -= max_p_min;
      ret.a /= std::numeric_limits<pixel_in_scalar_type>::max();
      ret.a /= 2 * ret.c;

      if(lambda & 1)
        ret.a = -ret.a;

      ret.a += pixel_out_scalar_type(.5); // 1/2

      ret.a += lambda;
      ret.a *= static_cast<pixel_out_scalar_type>(yaPI_d3);
      return ret;
    }

    pixel_out operator()(const pixel_in& v) const YAYI_THROW_DEBUG_ONLY__
    {
      const pixel_in_scalar_type R = v.a;
      const pixel_in_scalar_type G = v.b;
      const pixel_in_scalar_type B = v.c;

      // todo : do less tests
      if(R > G)
      {
        // r > g
        if(G >= B)
          return helper(B, G, R, 0);

        // r > g && b > g
        if(B > R)
          return helper(G, R, B, 4);

        return helper(G, B, R, 5);
      }

      // r <= g
      if(R > B)
        return helper(B, R, G, 1);

      // r <= g && r <= b
      if(G > B)
        return helper(R, B, G, 2);

      return helper(R, G, B, (G > R) ? 3 : 4);
    }
  };


  /*!@brief Helper functor to prevent hue getting out of the \f$[0, 2\pi[\f$ range.
   *
   * The adjustment is done in an iterative manner, but would be slow for hues very far from \f$[0, 2\pi[\f$.
   * Another implementation is possible involving divisions and modulos.
   * @tparam pixel_in_out the type of data to be considered.
   * @tparam enable_if__ sfinae for restricting the types on which the structure is instanciated.
   */
  
  template <class pixel_in_out, class enable_if__ = void>
  struct s_color_hue_modulus_on_2pi
  {};

  //! Specializing of s_color_hue_modulus_on_2pi for pixel_3 of float type.
  //! @note The hue is considered to be the first channel.
  template <class pixel_in_out_scalar_type>
  struct s_color_hue_modulus_on_2pi<
    s_compound_pixel_t<pixel_in_out_scalar_type, mpl::int_<3> >,
    typename s_restrict_on_float_representation<pixel_in_out_scalar_type>::type
    >
    : public std::unary_function<s_compound_pixel_t<pixel_in_out_scalar_type, mpl::int_<3> >, void >
  {
    typedef s_compound_pixel_t<pixel_in_out_scalar_type, mpl::int_<3> > pixel_in_out;

    void operator()(pixel_in_out& v) const
    {
      static const pixel_in_out_scalar_type ya2PI__ = static_cast<pixel_in_out_scalar_type>(ya2PI);
      pixel_in_out_scalar_type H = v.a;
      if(H < ya2PI__ && H >= 0)
        return;

      if(H < 0)
      {
        H += ya2PI__;
        while(H < 0)
        {
          H += ya2PI__;
        }
      }
      else
      {
        H -= ya2PI__;
        while(H >= ya2PI__)
        {
          H -= ya2PI__;
        }
        //pixel_in_scalar_type f_dummy;
        //H = static_cast<pixel_in_scalar_type>(ya2PI * std::modf(static_cast<pixel_in_scalar_type>(H/ya2PI), &f_dummy));
      }
      v.a = H;
    }
  };






  /*!@brief Transformation from HLS @f$\ell_1@f$ \f$[0, 2\pi[ \times [0,1] \times [0, 1]\f$ to RGB \f$[0, 255]^3\f$.
   *
   * @note This is the inverse transformation of s_color_RGB_to_HLSl1
   */
  template <class pixel_in, class pixel_out, class enable_if__ = void>
  struct s_color_HLSl1_to_RGB : public std::unary_function<pixel_in, pixel_out>
  {};

  template <class pixel_in_scalar_type>
  struct s_color_HLSl1_to_RGB<
    s_compound_pixel_t<pixel_in_scalar_type, mpl::int_<3> >,
    pixel8u_3,
    typename s_restrict_on_float_representation<pixel_in_scalar_type>::type
    >
    :
    public std::unary_function<s_compound_pixel_t<pixel_in_scalar_type, mpl::int_<3> >, pixel8u_3>
  {
    //! Input pixel type
    typedef s_compound_pixel_t<pixel_in_scalar_type, mpl::int_<3> > pixel_in;

    //! Output pixel type (8 bits)
    typedef pixel8u_3 pixel_out;

    pixel_out operator()(pixel_in v) const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(v.a < ya2PI && v.a >= 0, "Bad hue value " + any_to_string(v.a));
      static const s_color_hue_modulus_on_2pi<typename boost::remove_const<pixel_in>::type> op_modulus = s_color_hue_modulus_on_2pi<typename boost::remove_const<pixel_in>::type>();
      op_modulus(v); // needed ???

      pixel_in_scalar_type lambda_f;
      pixel_in_scalar_type	phi = std::modf(static_cast<pixel_in_scalar_type>(v.a * yaPI_d3), &lambda_f);
      unsigned int lambda = static_cast<unsigned int>(lambda_f);

      DEBUG_ASSERT(lambda >= 0 && lambda < 6, "Lambda bad value " + int_to_string(lambda));
      //lambda %= 6;

      const pixel_in_scalar_type	p1 = static_cast<pixel_in_scalar_type>(v.c/3.);
      const pixel_in_scalar_type	p2 = 2*p1;
      const pixel_in_scalar_type	p2phi = p2 * phi;
      pixel_in_scalar_type	max, med, min;

      if(lambda & 1)
      {
        med = v.b + p1 - p2phi;
      }
      else
      {
        med = v.b - p1 + p2phi;
      }

      if(v.b > med)
      {
        max = v.b + p2;
        min = 3*v.b - max - med;
      }
      else
      {
        min = v.b - p2;
        max = 3*v.b - min - med;
      }

      static const yaUINT8 v_mult = std::numeric_limits<yaUINT8>::max();
      switch(lambda)
      {
      case 0:
        return pixel_out(static_cast<yaUINT8>(max*v_mult), static_cast<yaUINT8>(med*v_mult), static_cast<yaUINT8>(min*v_mult));
      case 1:
        return pixel_out(static_cast<yaUINT8>(med*v_mult), static_cast<yaUINT8>(max*v_mult), static_cast<yaUINT8>(min*v_mult));
      case 2:
        return pixel_out(static_cast<yaUINT8>(min*v_mult), static_cast<yaUINT8>(max*v_mult), static_cast<yaUINT8>(med*v_mult));
      case 3:
        return pixel_out(static_cast<yaUINT8>(min*v_mult), static_cast<yaUINT8>(med*v_mult), static_cast<yaUINT8>(max*v_mult));
      case 4:
        return pixel_out(static_cast<yaUINT8>(med*v_mult), static_cast<yaUINT8>(min*v_mult), static_cast<yaUINT8>(max*v_mult));
      case 5:
        return pixel_out(static_cast<yaUINT8>(max*v_mult), static_cast<yaUINT8>(min*v_mult), static_cast<yaUINT8>(med*v_mult));

      default:
        errors::yayi_error_stream() << YAYI_DEBUG_MESSAGE("FATAL ERROR on lambda") << std::endl;
        break;
      }


      DEBUG_ASSERT(false, "Bad value of lambda");
    }

  };



  /*!@brief Transforms an RGB image into an HLS @f$\ell_1@f$.
   *
   * The HLS @f$\ell_1@f$ color space was proposed by J.Angulo in his PhD thesis @cite angulo_lopez_2003. This transformation
   * is named after the underkying norm it uses.
   */
  template <class image_in_, class image_out_>
  yaRC color_RGB_to_HLSl1_t(const image_in_& imin, image_out_& imo)
  {
    typedef s_color_RGB_to_HLSl1<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op;
    return op_processor(imin, imo, op);
  }

  //! @brief Transforms an HLS @f$\ell_1@f$ image into an RGB image.
  //! The inversion formulae can be found in the PhD of Raffi Enficiaud @cite enficiaud:2007.
  template <class image_in_, class image_out_>
  yaRC color_HLSl1_to_RGB_t(const image_in_& imin, image_out_& imo)
  {
    typedef s_color_HLSl1_to_RGB<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op;
    return op_processor(imin, imo, op);
  }






  /*! @brief Transform operator from RGB to HLS with the so-called GHLS definition.
   *	The input image should previously have been normalized into the range @f$[0,1]@f$
   *  The hue component is in @f$[0, 2\pi[@f$ range.
   */
  template<class pixel_in, class pixel_out, class enable_if__ = void>
  struct s_color_RGB_to_HLStrigonometric : public std::unary_function<pixel_in, pixel_out>
  {
    typedef pixel_out value_type;
    value_type operator()(const pixel_in& u) const YAYI_THROW_DEBUG_ONLY__
    {
      value_type ret;
      typedef typename value_type::value_type scalar_value_type;

      ret.b = static_cast<scalar_value_type>(0.2125f * u.a + 0.7154f * u.b + 0.0721f * u.c);
      const scalar_value_type C1= static_cast<scalar_value_type>(u.a - (u.b + u.c)/2.);

      const scalar_value_type C2= static_cast<scalar_value_type>(yaSqrt3_d2 * (u.c - u.b));
      const scalar_value_type C = ::sqrt(C1 * C1 + C2 * C2);

      if(C == 0)
      {
        // H is always positive, except when it is not defined. In this case, the saturation is set to 0 as well
        ret.c = ret.a = 0;
      }
      else
      {
        yaF_double hue = ::acos(C1/C);
        if(C2 > 0)
        {
          hue = ya2PI - hue;
        }
        ret.a = static_cast<scalar_value_type>(hue);

        yaF_simple f_integral;
        yaF_simple f_reminder = std::modf(static_cast<scalar_value_type>(hue/yaPI_d3), &f_integral);
        DEBUG_ASSERT(f_integral <= 5., "There is an error with the reminder");

        //scalar_value_type const Hprime = static_cast<scalar_value_type>(H - f_dummy * yaPI_d3); // ca ne serait pas f_reste par hazard ?
        // (hue - f_dummy * yaPI_d3) seems to be f_reminder
        DEBUG_ASSERT(static_cast<scalar_value_type>(::sin(ya2PI_d3 - (hue - f_integral * yaPI_d3))) != 0., "consistency problem in the HLS transform");
        ret.c = static_cast<scalar_value_type>(ya2_dSqrt3 * C * ::sin(ya2PI_d3 - (hue - f_integral * yaPI_d3)));
      }
      return ret;
    }
  };



  //!@ Inverse tranformation of the s_color_RGB_to_HLStrigonometric tranformation.
  template<class pixel_in, class pixel_out, class enable_if__ = void>
  struct s_color_HLStrigonometric_to_RGB : public std::unary_function<pixel_in, pixel_out>
  {
    typedef pixel_out value_type;
    value_type operator()(pixel_in u) const YAYI_THROW_DEBUG_ONLY__
    {
      typedef typename value_type::value_type scalar_value_type;


      if(u.c != 0)
      {
        yaF_simple f_integral;
        if(!((u.a < ya2PI) && (u.a >= 0)))
        {
          u.a = static_cast<scalar_value_type>(ya2PI * std::modf(u.a/ya2PI, &f_integral));
          if(u.a < 0)
          {
            u.a += ya2PI;
          }
        }
        std::modf(u.a/yaPI_d3, &f_integral);

        DEBUG_ASSERT(f_integral <= 5., "a problem in the modulus");
        DEBUG_ASSERT(::sin(ya2PI_d3 - (u.a - f_integral * yaPI_d3)) != 0., "a problem in the consistency of the transform");

        scalar_value_type C	= static_cast<scalar_value_type>(yaSqrt3_d2 * u.c / (::sin(ya2PI_d3 - (u.a - f_integral * yaPI_d3))));
        scalar_value_type C1 = C * ::cos(u.a);
        scalar_value_type C2 =-C * ::sin(u.a);

        return
          pixel_out(
            u.b + 0.7875 * C1 + 0.3714 * C2,
            u.b - 0.2125 * C1 - 0.2059 * C2,
            u.b - 0.2125 * C1 + 0.9488 * C2
            );
      }
      else
      {
        return pixel_out(u.b, u.b, u.b);
      }

    }
  };


  //! @} doxygroup: pp_color_details_grp
}

#endif // YAYI_COLOR_PROCESS_HLS_T_HPP__
