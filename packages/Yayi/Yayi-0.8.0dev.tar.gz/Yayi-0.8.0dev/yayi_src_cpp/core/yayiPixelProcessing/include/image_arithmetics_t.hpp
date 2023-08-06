#ifndef YAYI_PIXEL_IMAGE_ARITHMETIC_T_HPP__
#define YAYI_PIXEL_IMAGE_ARITHMETIC_T_HPP__

/*!@file
 * This file defines the arithmetic template operations on images
 */

#include <boost/call_traits.hpp>
#include <functional>

#include <yayiCommon/common_orders.hpp>

#include <yayiPixelProcessing/image_arithmetics.hpp>
#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_binary_t.hpp>
#include <yayiCommon/common_errors.hpp> // to remove

namespace yayi
{


  /*!
   * @defgroup pp_arih_details_grp Arithmetics on template images
   * @ingroup pp_arih_grp
   * @{
   */

  //! Unitary functor for addition
  template <class in1_t, class in2_t, class out_t>
  struct s_add :
    std::binary_function<
      typename boost::call_traits<in1_t>::param_type,
      typename boost::call_traits<in2_t>::param_type,
      out_t>
  {

    out_t operator()(
      typename boost::call_traits<in1_t>::param_type v1,
      typename boost::call_traits<in2_t>::param_type v2) const throw()
    {
      return static_cast<out_t>(v1 + v2);
    }
  };


  //! Addition of two images.
  //! Performs imo[p] = imin1[p] + imin2[p], for each pixel position p of the images
  template <class image_in1_, class image_in2_, class image_out_>
  yaRC add_images_t(const image_in1_& imin1, const image_in2_& imin2, image_out_& imo)
  {
    typedef s_add<
      typename image_in1_::pixel_type,
      typename image_in2_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_binary_operator op_processor;

    operator_type op;
    return op_processor(imin1, imin2, imo, op);
  }



  //! Functor for subtraction
  template <class in1_t, class in2_t, class out_t>
  struct s_sub :
    std::binary_function<
      typename boost::call_traits<in1_t>::param_type,
      typename boost::call_traits<in2_t>::param_type,
      out_t>
  {

    out_t operator()(
      typename boost::call_traits<in1_t>::param_type v1,
      typename boost::call_traits<in2_t>::param_type v2) const throw()
    {
      return static_cast<out_t>(v1 - v2);
    }

  };

  //! Subtracts the content of two images pixelwise
  template <class image_in1_, class image_in2_, class image_out_>
  yaRC subtract_images_t(const image_in1_& imin1, const image_in2_& imin2, image_out_& imo)
  {
    typedef s_sub<
      typename image_in1_::pixel_type,
      typename image_in2_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_binary_operator op_processor;

    operator_type op;
    return op_processor(imin1, imin2, imo, op);
  }


  //! Subtracts the content of two images pixelwise, with a lower bound
  template <class in1_t, class in2_t, class out_t>
  struct s_sub_lower_bound :
    std::binary_function<
      typename boost::call_traits<in1_t>::param_type,
      typename boost::call_traits<in2_t>::param_type,
      out_t>
  {
    typedef typename boost::add_const<out_t>::type lower_bound_t;
    lower_bound_t lower;

    s_sub_lower_bound(lower_bound_t &lower_) : lower(lower_){}

    out_t operator()(
      typename boost::call_traits<in1_t>::param_type v1,
      typename boost::call_traits<in2_t>::param_type v2) const throw()
    {
      return v1 >= v2 ? static_cast<out_t>(v1 - v2) : lower;
    }

  };

  /*! @brief Substract two images with a lower bound
   *
   * Each output pixel \f$p\f$ receives \f[(imin1(p) - imin2(p)) \vee lower\_bound\f]
   * The associated pixel functor is s_sub_lower_bound.
   * @author Raffi Enficiaud
   */
  template <class image_in1_, class image_in2_, class image_out_>
  yaRC subtract_with_lower_bound_images_t(
    image_in1_ const& imin1,
    image_in2_ const& imin2,
    typename image_out_::pixel_type const& lower_bound,
    image_out_& imo)
  {
    typedef s_sub_lower_bound<
      typename image_in1_::pixel_type,
      typename image_in2_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_binary_operator op_processor;

    operator_type op(lower_bound);
    return op_processor(imin1, imin2, imo, op);
  }



  //! Absolute difference (abs of the difference) functor
  template <class in1_t, class in2_t, class out_t>
  struct s_abssub :
    std::binary_function<
      typename boost::call_traits<in1_t>::param_type,
      typename boost::call_traits<in2_t>::param_type,
      out_t>
  {

    out_t operator()(
      typename boost::call_traits<in1_t>::param_type v1,
      typename boost::call_traits<in2_t>::param_type v2) const throw()
    {
      return static_cast<out_t>(std::abs(v1 - v2));
    }

  };

  //! Computes the absolute difference of two images, piwelwise
  template <class image_in1_, class image_in2_, class image_out_>
  yaRC abssubtract_images_t(const image_in1_& imin1, const image_in2_& imin2, image_out_& imo)
  {
    typedef s_abssub<
      typename image_in1_::pixel_type,
      typename image_in2_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_binary_operator op_processor;

    operator_type op;
    return op_processor(imin1, imin2, imo, op);
  }

  //! Multiplication of two images
  template <class in1_t, class in2_t, class out_t>
  struct s_mult :
    std::binary_function<
      typename boost::call_traits<in1_t>::param_type,
      typename boost::call_traits<in2_t>::param_type,
      out_t>
  {

    out_t operator()(
      typename boost::call_traits<in1_t>::param_type v1,
      typename boost::call_traits<in2_t>::param_type v2) const throw()
    {
      return static_cast<out_t>(v1 * v2);
    }

  };

  //! Mutiplies the pixels of the two images
  template <class image_in1_, class image_in2_, class image_out_>
  yaRC multiply_images_t(const image_in1_& imin1, const image_in2_& imin2, image_out_& imo)
  {
    typedef s_mult<
      typename image_in1_::pixel_type,
      typename image_in2_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_binary_operator op_processor;

    operator_type op;
    return op_processor(imin1, imin2, imo, op);
  }



  template <class in1_t, class in2_t, class out_t>
  struct s_div :
    std::binary_function<
      typename boost::call_traits<in1_t>::param_type,
      typename boost::call_traits<in2_t>::param_type,
      out_t>
  {

    out_t operator()(
      typename boost::call_traits<in1_t>::param_type v1,
      typename boost::call_traits<in2_t>::param_type v2) const throw()
    {
      return static_cast<out_t>(v1 / v2);
    }

  };

  template <class image_in1_, class image_in2_, class image_out_>
  yaRC divide_images_t(const image_in1_& imin1, const image_in2_& imin2, image_out_& imo)
  {
    typedef s_div<
      typename image_in1_::pixel_type,
      typename image_in2_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_binary_operator op_processor;

    operator_type op;
    return op_processor(imin1, imin2, imo, op);
  }




  //! Functor for adding a constant value to an image
  template <class in1_t, class val_t, class out_t>
  struct s_add_constant : std::unary_function<typename boost::call_traits<in1_t>::param_type, out_t>
  {
    typename boost::add_const<val_t>::type value;
    s_add_constant(typename boost::call_traits<val_t>::param_type p) : value(p) {}
    out_t operator()(typename boost::call_traits<in1_t>::param_type v1) const throw()
    {
      return static_cast<out_t>(v1 + value);
    }
  };


  //! Function adding a constant value to an image. May be called "in-place".
  template <class image_in1_, class image_out_>
  yaRC add_images_constant_t(const image_in1_& imin1, typename image_in1_::const_reference val, image_out_& imo)
  {
    typedef s_add_constant<
      typename image_in1_::pixel_type,
      typename image_in1_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(val);
    return op_processor(imin1, imo, op);
  }

  //! Functor for adding a constant value to an image, by bounding the result of the addition
  template <class in1_t, class val_t, class out_t>
  struct s_add_constant_upper_bound : std::unary_function<typename boost::call_traits<in1_t>::param_type, out_t>
  {
    typename boost::add_const<val_t>::type value, upper_bound;
    s_add_constant_upper_bound(typename boost::call_traits<val_t>::param_type p, typename boost::call_traits<val_t>::param_type upper_bound_) : value(p), upper_bound(upper_bound_) {}
    out_t operator()(typename boost::call_traits<in1_t>::param_type v1) const throw()
    {

      return static_cast<out_t>(v1 + value > upper_bound ? upper_bound:v1 + value);
    }
  };


  //! Function adding a constant value to an image. May be called "in-place".
  template <class image_in1_, class image_out_>
  yaRC add_images_constant_upper_bound_t(const image_in1_& imin1, typename image_in1_::const_reference val, typename image_in1_::const_reference upper_bound, image_out_& imo)
  {
    typedef s_add_constant_upper_bound<
      typename image_in1_::pixel_type,
      typename image_in1_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(val, upper_bound);
    return op_processor(imin1, imo, op);
  }



  template <class in1_t, class val_t, class out_t>
  struct s_sub_constant :
    std::unary_function<
      typename boost::call_traits<in1_t>::param_type,
      out_t>
  {
    typename boost::add_const<val_t>::type value;
    s_sub_constant(typename boost::call_traits<val_t>::param_type p) : value(p) {}
    out_t operator()(typename boost::call_traits<in1_t>::param_type v1) const throw()
    {
      return static_cast<out_t>(v1 - value);
    }
  };


  //! Function subtracting a constant value to every pixels of the input image. May be called in-place.
  template <class image_in1_, class image_out_>
  yaRC subtract_images_constant_t(
    const image_in1_& imin1,
    typename boost::call_traits<typename image_in1_::pixel_type>::param_type val,
    image_out_& imo)
  {
    typedef s_sub_constant<
      typename image_in1_::pixel_type,
      typename image_in1_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(val);
    return op_processor(imin1, imo, op);
  }

  //! Functor for substrating a constant value to an image, by bounding the result of the subtraction
  template <class in1_t, class val_t, class out_t>
  struct s_sub_constant_lower_bound : std::unary_function<typename boost::call_traits<in1_t>::param_type, out_t>
  {
    typename boost::add_const<val_t>::type value, lower_bound;
    s_sub_constant_lower_bound(typename boost::call_traits<val_t>::param_type p, typename boost::call_traits<val_t>::param_type lower_bound_) : value(p), lower_bound(lower_bound_) {}
    out_t operator()(typename boost::call_traits<in1_t>::param_type v1) const throw()
    {

      return static_cast<out_t>(v1 - value < lower_bound ? lower_bound:v1 - value);
    }
  };


  //! Function subtracting a constant value to an image and bounding the result. May be called "in-place".
  template <class image_in1_, class image_out_>
  yaRC subtract_images_constant_lower_bound_t(const image_in1_& imin1, typename image_in1_::const_reference val, typename image_in1_::const_reference lower_bound, image_out_& imo)
  {
    typedef s_sub_constant_lower_bound<
      typename image_in1_::pixel_type,
      typename image_in1_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(val, lower_bound);
    return op_processor(imin1, imo, op);
  }



  /*! Multiplication of the input by a constant value.
   * @tparam in1_t the input pixel type
   * @tparam val_t the type of the contant
   * @tparam out_t the output pixel type
   *
   * @note the existance of this functor is justified by the fact that it micht be tricky to use std::multiplies with
   * different types (eg int with double returning int).
   */
  template <class in1_t, class val_t, class out_t>
  struct s_mult_constant :
    std::unary_function<
      typename boost::call_traits<in1_t>::param_type,
      out_t>
  {
    typename boost::add_const<val_t>::type value;
    s_mult_constant(typename boost::call_traits<val_t>::param_type p) : value(p) {}
    out_t operator()(typename boost::call_traits<in1_t>::param_type v1) const throw()
    {
      return static_cast<out_t>(v1 * value);
    }
  };


  //! Image multiplication with a constant value.
  //! Care should be taken for the multiplication operand type.
  template <class image_in1_, class val_t, class image_out_>
  yaRC multiply_images_constant_t(
    const image_in1_& imin1,
    typename boost::call_traits<val_t>::param_type val,
    image_out_& imo)
  {
    typedef s_mult_constant<
      typename image_in1_::pixel_type,
      val_t,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(val);
    return op_processor(imin1, imo, op);
  }




  template <class in1_t, class in2_t, class out_t, class compare_t = std::less<typename s_supertype<in1_t, in2_t>::type> >
  struct s_predicate_image :
    std::binary_function<
      typename boost::call_traits<in1_t>::param_type,
      typename boost::call_traits<in2_t>::param_type,
      out_t>
  {
    const compare_t op_;
    s_predicate_image() : op_() {}
    s_predicate_image(const compare_t& op) : op_(op) {}

    out_t operator()(
      typename boost::call_traits<in1_t>::param_type v1,
      typename boost::call_traits<in2_t>::param_type v2) const throw()
    {
      return static_cast<out_t>(op_(v1, v2) ? v1 : v2);
    }

  };

  template <class in_t, class compare_t>
  struct s_predicate_image<in_t, in_t, in_t, compare_t> :
    std::binary_function<
      typename boost::add_reference<typename boost::add_const<in_t>::type>,
      typename boost::add_reference<typename boost::add_const<in_t>::type>,
      typename boost::add_reference<typename boost::add_const<in_t>::type> >
  {
    typedef typename boost::add_reference<typename boost::add_const<in_t>::type>::type result_type;

    const compare_t op_;
    s_predicate_image() : op_() {}
    s_predicate_image(const compare_t& op) : op_(op) {}
    result_type operator()(result_type v1, result_type v2) const throw()
    {
      return (op_(v1, v2) ? v1 : v2);
    }

  };

  //! Predicate operation on two images
  //! Each pixel (x1, x2) respectively from imin1, imin2, receives the value pred(x1, x2) ? x1:x2
  template <class image_in1_, class image_in2_, class pred_t, class image_out_>
  yaRC predicate_images_t(const image_in1_& imin1, const image_in2_& imin2, const pred_t& pred, image_out_& imo)
  {
    typedef s_predicate_image<
      typename image_in1_::pixel_type,
      typename image_in2_::pixel_type,
      typename image_out_::pixel_type,
      pred_t>  operator_type;

    s_apply_binary_operator op_processor;

    operator_type op(pred);
    return op_processor(imin1, imin2, imo, op);
  }


  //! Supremum (union) of two images
  template <class image_in1_, class image_in2_, class image_out_>
  yaRC supremum_images_t(const image_in1_& imin1, const image_in2_& imin2, image_out_& imo)
  {
    return predicate_images_t(imin1, imin2, std::greater<typename image_in1_::pixel_type>(), imo);
  }

  //! Infimum (intersection) of two images
  template <class image_in1_, class image_in2_, class image_out_>
  yaRC infimum_images_t(const image_in1_& imin1, const image_in2_& imin2, image_out_& imo)
  {
    return predicate_images_t(imin1, imin2, std::less<typename image_in1_::pixel_type>(), imo);
  }





  //! Complements the value of the pixel (the lattice is supposed to have a chain structure)
  template <class in1_t, class out_t>
  struct s_complement :
    std::unary_function<
      typename boost::call_traits<in1_t>::param_type,
      out_t>
  {
    typename boost::add_const<in1_t>::type max_value;
    s_complement() : max_value(s_bounds_helper<in1_t>::max()) {}
    out_t operator()(typename boost::call_traits<in1_t>::param_type v1) const throw()
    {
      return static_cast<out_t>(max_value - v1);
    }
  };


  template <class image_in1_, class image_out_>
  yaRC complement_images_t(const image_in1_& imin1, image_out_& imo)
  {
    typedef s_complement<
      typename image_in1_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op;
    return op_processor(imin1, imo, op);
  }

  template <class image_in1_, class image_out_>
  yaRC complement_images_windowed_t(
    const image_in1_& imin1,
    const s_hyper_rectangle<image_in1_::coordinate_type::static_dimensions> &rect_in,
    const s_hyper_rectangle<image_out_::coordinate_type::static_dimensions> &rect_out,
    image_out_& imo)
  {
    typedef s_complement<
      typename image_in1_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op;
    return op_processor(imin1, rect_in, imo, rect_out, op);
  }

  //! @} doxygroup: pp_arih_details_grp
}

#endif
