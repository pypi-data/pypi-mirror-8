#ifndef YAYI_COLOR_PROCESS_LAB_T_HPP__
#define YAYI_COLOR_PROCESS_LAB_T_HPP__

/*! @file
 *  This file defines lab transformation of images to and from XYZ color space and RGB color spaces
 *  @author Raffi Enficiaud
 */

#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiCommon/common_constants.hpp>
#include <functional>


namespace yayi
{

  /*!@addtogroup pp_color_details_grp
   *
   * @{
   */

  //! This is the main structure performing the transformation from XYZ spaces to La*b* spaces
  //! according to www.brucelindbloom.com
  template <class in_pixel_t, class out_pixel_t>
  struct s_xyz_to_lab : public std::unary_function<in_pixel_t, out_pixel_t>
  {
    const yaF_double inv_x_wref, inv_y_wref, inv_z_wref;

    s_xyz_to_lab(yaF_double const xyz_wref[]):
      inv_x_wref(1/xyz_wref[0]), inv_y_wref(1/xyz_wref[1]), inv_z_wref(1/xyz_wref[2])
    {}

    template <class T>
    yaF_double f(const T &in) const
    {
      if(in <= 216./24389.)
        return 24389./(116.*27.)* in + 16./116.;
      return std::pow(in, 1./3.); // replace by a faster variant
    }

    out_pixel_t operator()(in_pixel_t const& in) const
    {
      yaF_double const fy = f(in.b * inv_y_wref);
      return out_pixel_t(
          typename out_pixel_t::value_type(116. * fy - 16.),
          typename out_pixel_t::value_type(500 * (f(in.a * inv_x_wref) - fy)),
          typename out_pixel_t::value_type(200 * (fy - f(in.c * inv_z_wref)))
        );
    }
  };

  //! This is the main structure performing the reverse transformation from XYZ spaces to La*b* spaces
  //! according to www.brucelindbloom.com
  template <class in_pixel_t, class out_pixel_t>
  struct s_lab_to_xyz : public std::unary_function<in_pixel_t, out_pixel_t>
  {
    const yaF_double x_wref, y_wref, z_wref;

    s_lab_to_xyz(yaF_double const xyz_wref[]):
      x_wref(xyz_wref[0]), y_wref(xyz_wref[1]), z_wref(xyz_wref[2])
    {}

    template <class T>
    yaF_double finv(const T &in) const
    {
      if(in <= 6./29)
        return 3*6*6*(in-4./29)/(29*29);
      return in*in*in;
    }

    out_pixel_t operator()(in_pixel_t const& in) const
    {
      yaF_double const Lfirst = (in.a + 16)/116;
      return out_pixel_t(
          typename out_pixel_t::value_type(x_wref * finv(Lfirst + in.b/500)),
          typename out_pixel_t::value_type(y_wref * finv(Lfirst)),
          typename out_pixel_t::value_type(z_wref * finv(Lfirst - in.c/200))
        );
    }
  };

  //! XYZ to La*b* common transform, reference white as parameter
  template <class image_in_, class image_out_>
  yaRC color_XYZ_to_LAB_t(const image_in_& imin, yaF_double x, yaF_double y, image_out_& imo)
  {
    const yaF_double refW[] = { x/y, 1, (1-x-y)/y };

    typedef s_xyz_to_lab<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(refW);
    return op_processor(imin, imo, op);
  }

  //! La*b* to XYZ common transform, reference white as parameter
  template <class image_in_, class image_out_>
  yaRC color_LAB_to_XYZ_t(const image_in_& imin, yaF_double x, yaF_double y, image_out_& imo)
  {
    const yaF_double refW[] = { x/y, 1, (1-x-y)/y };

    typedef s_lab_to_xyz<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(refW);
    return op_processor(imin, imo, op);
  }



  //! XYZ to La*b* transform, reference white A
  template <class image_in_, class image_out_>
  yaRC color_XYZ_to_LAB_refWA_t(const image_in_& imin, image_out_& imout)
  {
    return color_XYZ_to_LAB_t(imin, 0.44757, 0.40745, imout);
  }

  //! La*b* to XYZ transform, reference white A
  template <class image_in_, class image_out_>
  yaRC color_LAB_to_XYZ_refWA_t(const image_in_& imin, image_out_& imout)
  {
    return color_LAB_to_XYZ_t(imin, 0.44757, 0.40745, imout);
  }

  //! XYZ to La*b* transform, reference white E
  template <class image_in_, class image_out_>
  yaRC color_XYZ_to_LAB_refWE_t(const image_in_& imin, image_out_& imout)
  {
    return color_XYZ_to_LAB_t(imin, 1./3, 1./3, imout);
  }

  //! La*b* to XYZ transform, reference white A
  template <class image_in_, class image_out_>
  yaRC color_LAB_to_XYZ_refWE_t(const image_in_& imin, image_out_& imout)
  {
    return color_LAB_to_XYZ_t(imin, 1./3, 1./3, imout);
  }


  //! XYZ to La*b* transform, reference white D65
  template <class image_in_, class image_out_>
  yaRC color_XYZ_to_LAB_refWD65_t(const image_in_& imin, image_out_& imout)
  {
    return color_XYZ_to_LAB_t(imin, 0.31278, 0.32918, imout);
  }

  //! La*b* to XYZ transform, reference white A
  template <class image_in_, class image_out_>
  yaRC color_LAB_to_XYZ_refWD65_t(const image_in_& imin, image_out_& imout)
  {
    return color_LAB_to_XYZ_t(imin, 0.31278, 0.32918, imout);
  }

  //! XYZ to La*b* transform, reference white D75
  template <class image_in_, class image_out_>
  yaRC color_XYZ_to_LAB_refWD75_t(const image_in_& imin, image_out_& imout)
  {
    return color_XYZ_to_LAB_t(imin, 0.29909, 0.31503, imout);
  }

  //! La*b* to XYZ transform, reference white A
  template <class image_in_, class image_out_>
  yaRC color_LAB_to_XYZ_refWD75_t(const image_in_& imin, image_out_& imout)
  {
    return color_LAB_to_XYZ_t(imin, 0.29909, 0.31503, imout);
  }


  //! @}

}

#endif /* YAYI_COLOR_PROCESS_LAB_T_HPP__ */
