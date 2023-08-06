#ifndef COLOR_DISTANCES_T_HPP__
#define COLOR_DISTANCES_T_HPP__


/*!@file
 * This file defines distance over the channels on multichannel image.
 * @author Raffi Enficiaud
 */


#include <yayiCommon/common_constants.hpp>
#include <yayiCommon/common_errors.hpp>
#include <yayiCommon/common_pixels_T.hpp>
#include <cmath>

namespace yayi
{
  /*!@defgroup colordistance_details_grp Color distance template functions and structures.
   * @ingroup distances_grp
   * @brief Color distances on value space of the image.
   *
   * Color distances are a special type of distances on the value space of images. Since a color potentially
   * has an infinite number of different meanings, their are also many ways to compare the "closeness" of two colors. This is the intend
   * of colour distances.
   * @{
   */


  /*!@brief Yuv weighted distance
   *
   * Given two 3-pixels @f$p_1 = (y_1, u_1, v_1)@f$ and @f$p_2 = (y_2, u_2, v_2)@f$ expressed in the YUV colorspace,
   * this functor computes a distance between @f$p_1@f$ and @f$p_2@f$ defined as
   * @f[d_{yuv} (p_1, p_2) = \sqrt{\frac{1}{2}(y_1-y_2)^2 + \frac{1}{4}(u_1-u_2)^2 + \frac{1}{4}(v_1-v_2)^2}@f]
   */
  template <class in1_t, class in2_t, class out_t>
  struct yuv_weighted : std::binary_function<in1_t, in2_t, out_t>
  {
    typedef out_t value_type;
    inline out_t operator()(const in1_t& t_1,  const in2_t& t_2) const throw()
    {
      yaF_double d_delta_Y = static_cast<yaF_double>(t_1[0]) - static_cast<yaF_double>(t_2[0]);
      d_delta_Y *= 0.5f*d_delta_Y;
      yaF_double d_delta_u = static_cast<yaF_double>(t_1[1]) - static_cast<yaF_double>(t_2[1]);
      d_delta_u *= d_delta_u;
      yaF_double d_delta_v = static_cast<yaF_double>(t_1[2]) - static_cast<yaF_double>(t_2[2]);
      d_delta_v *= d_delta_v;

      return static_cast<value_type>(sqrt(d_delta_Y + 0.25*(d_delta_u + d_delta_v)));
    }
  };

  //! Euclidian distance on LAB color space, using HUE differences
  template <typename in1_t, typename in2_t, typename out_t>
  struct operator_distance_labhue_t : std::binary_function<in1_t, in2_t, out_t>
  {
    typedef out_t value_type;

    value_type operator()(const in1_t& t_1,  const in2_t& t_2) const throw()
    {
      yaF_double d_delta_a = static_cast<double>(t_1[0]) - static_cast<double>(t_2[1]);
      d_delta_a *= d_delta_a;
      yaF_double d_delta_b = static_cast<double>(t_1[2]) - static_cast<double>(t_2[2]);
      d_delta_b *= d_delta_b;

      double d_delta_cab = std::sqrt(t_2[1]*t_2[1] + t_2[2]*t_2[2]);
      d_delta_cab -= std::sqrt(t_1[1]* t_1[1] + t_1[2]*t_1[2]);
      d_delta_cab *= d_delta_cab;

      return static_cast<value_type>(std::max(0., d_delta_a + d_delta_b - d_delta_cab));
    }
  };



  //! Circular distance (for scalar input). The distance value is mapped from @f$[0, pi]@f$ into @f$[0,1]@f$.
  template <typename in1_t, typename in2_t, typename out_t>
  struct s_distance_circular : std::binary_function<in1_t, in2_t, out_t>
  {
    typedef out_t value_type;
    value_type operator()(const in1_t& t_1, const in2_t& t_2) const throw()
    {
      double dummy;
      double d_delta_H = t_1 - t_2;
      if(d_delta_H < 0.) d_delta_H = -d_delta_H;

      d_delta_H /= ya2PI;
      d_delta_H  = std::modf( d_delta_H, &dummy );
      d_delta_H *= 2.;
      if(d_delta_H > 1.)
      {
        d_delta_H = 2.-d_delta_H;
      }
      return static_cast<value_type>(d_delta_H);
    }
  };

  //! Circular distance on hue channel only (in HLS color space). The distance value is mapped from @f$[0, pi]@f$ into @f$[0,1]@f$.
  template <typename in1_t, typename in2_t, typename out_t>
  struct s_distanceHLS_HUE : s_distance_circular<in1_t, in2_t, out_t>
  {
    typedef out_t value_type;
    typedef s_distance_circular<in1_t, in2_t, out_t> parent_type;
    value_type operator()(const in1_t& t_1,  const in2_t& t_2) const throw()
    {
      return parent_type(t_1[0], t_2[0]);
    }
  };


  //!Distance on the compilation-time specified channel only (in HLS color space).
  template <class in1_t, class in2_t, class out_t, int channel>
  struct s_distance_absolute_channel_t : std::binary_function<in1_t, in2_t, out_t>
  {
    typedef out_t value_type;
    value_type operator()(const in1_t& t_1,  const in2_t& t_2) const throw()
    {
      return static_cast<out_t>(std::abs(t_1[channel]) - static_cast<double>(t_2[channel]));
    }
  };

  //! Distance defined by the sup of the difference on all channels.
  //! This distance handles properly the range of the hue channel (@f$[0, 2pi[@f$) and hence differs from a simple
  //! supremum over the three channels.
  template <class in1_t, class in2_t, class out_t>
  struct s_distanceHLS_sup_t : std::binary_function<in1_t, in2_t, out_t>
  {
    typedef s_distanceHLS_HUE<typename in1_t::value_type, typename in2_t::value_type, double> circular_distance_t;
    circular_distance_t op_distance;

    typedef typename s_supertype<typename in1_t::value_type, typename in2_t::value_type>::type super_type;
    s_distance_absolute_channel_t<in1_t, in2_t, super_type, 1> op_c1;
    s_distance_absolute_channel_t<in1_t, in2_t, super_type, 2> op_c2;

    typedef out_t value_type;
    value_type operator()(const in1_t& t_1,  const in2_t& t_2) const throw()
    {
      double maxval = op_distance(t_1, t_2);

      super_type d_delta = op_c1(t_1, t_2);
      if(d_delta > maxval)
        maxval = d_delta;

      super_type = op_c2(t_1, t_2);
      if(d_delta > maxval)
        maxval = d_delta;

      return static_cast<value_type>(maxval);
    }
  };





  //! Distance operator on HLS color space.
  //! The distance is defined as : @f[d(pix_1, pix_2) = (sat_1 + sat_2) / 2 * | hue_1 - hue_2 | + (1 - (sat_1 + sat_2) / 2) * | lum_1 - lum_2 |@f]
  //! where \f$| hue_1 - hue_2 |\f$ is the modulo @f$\pi@f$ difference ranged to @f$[0, 1]@f$.
  template <class in1_t, class in2_t, class out_t>
  struct s_distanceHLS_HLweighted : std::binary_function<in1_t, in2_t, out_t>
  {
    typedef s_distanceHLS_HUE<typename in1_t::value_type, typename in2_t::value_type, double> circular_distance_t;
    circular_distance_t op_distance;
    typedef typename s_supertype<typename in1_t::value_type, typename in2_t::value_type>::type super_type;
    s_distance_absolute_channel_t<in1_t, in2_t, super_type, 1> op_c1;


    typedef out_t value_type;
    value_type operator()(const in1_t& t_1,  const in2_t& t_2) const YAYI_THROW_DEBUG_ONLY__
    {
      assert(t_1[2] >= 0 && t_1[2] <= 1);

      double d_delta_H = op_distance(t_1, t2);
      super_type d_delta_L = op_c1(t_1, t_2);
      super_type d_weight = t_1[2]+t_2[2]; // Raffi: gérer la saturation
      d_weight /= 2; // Raffi: voir pour la normalisation
      return static_cast<out_t>(d_weight * d_delta_H + (1-d_weight)*d_delta_L);
    }
  };


}

#endif /* COLOR_DISTANCES_T_HPP__ */
