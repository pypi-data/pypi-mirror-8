#ifndef YAYI_COMPARE_T_HPP__
#define YAYI_COMPARE_T_HPP__

/*!@file
 * This file contains the image comparison template functions
 * @author Raffi Enficiaud
 */

#include <boost/call_traits.hpp>
#include <functional>
#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_binary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_ternary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_fourary_t.hpp>

#include <yayiPixelProcessing/include/image_arithmetics_t.hpp>

namespace yayi
{
  /*!@defgroup pp_comp_details_grp Comparisons of images implementation details.
   * @ingroup pp_comp_grp
   *
   * @{
   */

  //! Compare an image with a constant value, assigns a constant false or true value to output image
  template <class input, class output, class compare_op>
  struct s_compare_s :
    std::unary_function<
      typename boost::call_traits<input>::param_type,
      typename boost::add_reference<typename boost::add_const<output>::type >::type
      >
  {
    const compare_op  c_op;
    const output      true_val, false_val;
    s_compare_s(const output& true_val_, const output& false_val_) : c_op(), true_val(true_val_), false_val(false_val_) {}
    s_compare_s(const output& true_val_, const output& false_val_, const compare_op& comp) : c_op(comp), true_val(true_val_), false_val(false_val_) {}

    typename boost::add_reference<typename boost::add_const<output>::type >::type
    operator()(typename boost::call_traits<input>::param_type val) const throw()
    {
      return (c_op(val) ? true_val:false_val);
    }

  };



   /*!@brief  Special comparison operator for thresholding a pixel given an lower and upper bound.
    *
    * The result op(x) is true if x in [lower, upper], false otherwise.
    * lower and upper can be equal. The reason for the interval not being half-open (eg. \f$[lower, upper[\f$) is for preventing
    * the overflow problems when upper == std::numeric_limits<input_t>::max() or  lower == std::numeric_limits<input_t>::min()
    */
  template <class input_t>
  struct s_threshold_op : std::unary_function<typename boost::call_traits<input_t>::param_type, bool>
  {
    const input_t     lower, upper;
    s_threshold_op(const input_t& lower_, const input_t& upper_) : lower(lower_), upper(upper_)
    {}

    bool operator()(typename boost::call_traits<input_t>::param_type val) const throw()
    {
      return (val >= lower && val <= upper);
    }
  };

  //! Thresholds an image, given a lower and upper bound (imout = v_true if pixel in \f$[lower, upper[\f$, v_false otherwise)
  template <class image_in_t, class image_out_t>
  yaRC image_threshold_t(
    const image_in_t& imin,
    typename boost::call_traits<typename image_in_t::pixel_type>::param_type lower_bound,
    typename boost::call_traits<typename image_in_t::pixel_type>::param_type upper_bound,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_true,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_false,
    image_out_t& imout)
  {
    typedef s_compare_s<
      typename image_in_t::pixel_type,
      typename image_out_t::pixel_type,
      s_threshold_op<typename image_in_t::pixel_type> > operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(v_true, v_false, s_threshold_op<typename image_in_t::pixel_type>(lower_bound, upper_bound));
    return op_processor(imin, imout, op);
  }




  /*!@brief Special comparison operator for thresholding a pixel given an lower and upper bound.
   *
   * The result op(x) is given by the associative map if \f$x \in [lower,upper[ \f$, and by a default value otherwise.
   */
  template <class input_t, class output_t>
  struct s_lookup_table_transform_op : std::unary_function<typename boost::call_traits<input_t>::param_type, output_t const &>
  {
    typedef std::map<input_t, output_t> map_t;
    typedef typename map_t::const_iterator it_t;

    const map_t map_;
    const it_t ite;
    const output_t default_;

    s_lookup_table_transform_op(const map_t& map__, output_t const& default__) : map_(map__), ite(map_.end()), default_(default__)
    {}

    output_t const& operator()(typename boost::call_traits<input_t>::param_type val) const throw()
    {
      it_t it = map_.find(val);
      if(it == ite) return default_;
      return it->second;
    }
  };


  //! Specializing of the lookup table transform for a bounded range input type.
  template <class output_t>
  struct s_lookup_table_transform_op<yaUINT8, output_t> : std::unary_function<typename boost::call_traits<yaUINT8>::param_type, output_t const &>
  {
    typedef yaUINT8 input_t;
    typedef std::map<input_t, output_t> map_t;
    typedef typename map_t::const_iterator it_t;
    output_t table[256];

    s_lookup_table_transform_op(const map_t& map__, output_t const& default__)
    {
      for(input_t i = 0; i < std::numeric_limits<input_t>::max() - std::numeric_limits<input_t>::min(); i++)
      {
        it_t it(map__.find(i));
        table[i] = it != map__.end() ? it->second : default__;
      }
    }

    output_t const& operator()(typename boost::call_traits<input_t>::param_type val) const throw()
    {
      return table[val];
    }

  protected:
    //! Different construction semantics in order to reuse the table (since it cannot be const)
    s_lookup_table_transform_op()
    {}
  };


  //! Applies the lookup table transform to an image
  template <class image_in_t, class image_out_t>
  yaRC image_lookup_transform_t(
    const image_in_t& imin,
    const std::map<typename image_in_t::pixel_type, typename image_out_t::pixel_type> &map_,
    const typename image_out_t::pixel_type& default_value,
    image_out_t& imout)
  {
    typedef s_lookup_table_transform_op<
      typename image_in_t::pixel_type,
      typename image_out_t::pixel_type > operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(map_, default_value);
    return op_processor(imin, imout, op);
  }






  //! Compare an image with a constant value, assigns a constant false or true value to output image
  template <class image_in_t, class image_out_t, class op_t>
  yaRC image_compare_s(
    const image_in_t& imin,
    op_t op_comp,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_true,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_false,
    image_out_t& imout)
  {
    typedef s_compare_s<
      typename image_in_t::pixel_type,
      typename image_out_t::pixel_type,
      op_t> operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(v_true, v_false, op_comp);
    return op_processor(imin, imout, op);
  }


  template <class image_in_t, class image_out_t>
  yaRC image_compare_s_stub(
    const image_in_t& imin,
    comparison_operations c,
    typename boost::call_traits<typename image_in_t::pixel_type>::param_type compare_value,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_true,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_false,
    image_out_t& imout)
  {

    switch(c)
    {
    case e_co_equal:
      {
        return image_compare_s(
          imin,
          std::bind2nd(std::equal_to<typename image_in_t::pixel_type>(), compare_value),
          v_true, v_false,
          imout);
      }
    case e_co_different:
      {
        return image_compare_s(
          imin,
          std::bind2nd(std::not_equal_to<typename image_in_t::pixel_type>(), compare_value),
          v_true, v_false,
          imout);
      }
    case e_co_superior:
      {
        return image_compare_s(
          imin,
          std::bind2nd(std::greater_equal<typename image_in_t::pixel_type>(), compare_value),
          v_true, v_false,
          imout);
      }
    case e_co_superior_strict:
      {
        return image_compare_s(
          imin,
          std::bind2nd(std::greater<typename image_in_t::pixel_type>(), compare_value),
          v_true, v_false,
          imout);
      }
    case e_co_inferior:
      {
        return image_compare_s(
          imin,
          std::bind2nd(std::less_equal<typename image_in_t::pixel_type>(), compare_value),
          v_true, v_false,
          imout);
      }
    case e_co_inferior_strict:
      {
        return image_compare_s(
          imin,
          std::bind2nd(std::less<typename image_in_t::pixel_type>(), compare_value),
          v_true, v_false,
          imout);
      }
    default:
      DEBUG_INFO("Comparison type not implemented");
      return yaRC_E_bad_parameters;
    }

  }







  //! Compare an image with another image pixelwise, assigns a constant false or true value to output image
  template <class input1, class input2, class output, class compare_op>
  struct s_compare_i :
    std::binary_function<
      typename boost::call_traits<input1>::param_type,
      typename boost::call_traits<input2>::param_type,
      typename boost::add_reference<typename boost::add_const<output>::type >::type
      >
  {
    const compare_op  c_op;
    const output      true_val, false_val;
    s_compare_i(const output& true_val_, const output& false_val_) : c_op(), true_val(true_val_), false_val(false_val_) {}
    s_compare_i(const output& true_val_, const output& false_val_, const compare_op& comp) : c_op(comp), true_val(true_val_), false_val(false_val_) {}

    typename boost::add_reference<typename boost::add_const<output>::type >::type
    operator()(
      typename boost::call_traits<input1>::param_type val1,
      typename boost::call_traits<input2>::param_type val2) const throw()
    {
      return (c_op(val1, val2) ? true_val:false_val);
    }

  };

  //! Compare an image with another image pixelwise, assigns a constant false or true value to output image
  template <class image_in1_t, class image_in2_t, class image_out_t, class op_t>
  yaRC image_compare_i(
    const image_in1_t& imin1,
    op_t op_comp,
    const image_in2_t& imin2,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_true,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_false,
    image_out_t& imout)
  {
    typedef s_compare_i<
      typename image_in1_t::pixel_type,
      typename image_in2_t::pixel_type,
      typename image_out_t::pixel_type,
      op_t> operator_type;

    s_apply_binary_operator op_processor;

    operator_type op(v_true, v_false, op_comp);
    return op_processor(imin1, imin2, imout, op);
  }

  //! Compare an image with another image pixelwise, assigns a constant false or true value to output image
  template <class image_in1_t, class image_in2_t, class image_out_t>
  yaRC image_compare_i_stub(
    const image_in1_t& imin1,
    comparison_operations c,
    const image_in2_t& imin2,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_true,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_false,
    image_out_t& imout)
  {

    BOOST_STATIC_ASSERT((boost::is_convertible<typename image_in2_t::pixel_type, typename image_in1_t::pixel_type>::value));

    switch(c)
    {
    case e_co_equal:
      {
        return image_compare_i(
          imin1,
          std::equal_to<typename image_in1_t::pixel_type>(),
          imin2,
          v_true, v_false,
          imout);
      }
    case e_co_different:
      {
        return image_compare_i(
          imin1,
          std::not_equal_to<typename image_in1_t::pixel_type>(),
          imin2,
          v_true, v_false,
          imout);
      }
    case e_co_superior:
      {
        return image_compare_i(
          imin1,
          std::greater_equal<typename image_in1_t::pixel_type>(),
          imin2,
          v_true, v_false,
          imout);
      }
    case e_co_superior_strict:
      {
        return image_compare_i(
          imin1,
          std::greater<typename image_in1_t::pixel_type>(),
          imin2,
          v_true, v_false,
          imout);
      }
    case e_co_inferior:
      {
        return image_compare_i(
          imin1,
          std::less_equal<typename image_in1_t::pixel_type>(),
          imin2,
          v_true, v_false,
          imout);
      }
    case e_co_inferior_strict:
      {
        return image_compare_i(
          imin1,
          std::less<typename image_in1_t::pixel_type>(),
          imin2,
          v_true, v_false,
          imout);
      }
    default:
      DEBUG_INFO("Comparison type not implemented");
      return yaRC_E_bad_parameters;
    }

  }



  //! Compare an image with a constant value, assigns a constant false or the corresponding pixel of the true image to output image
  template <class input1, class true_t, class output, class compare_op>
  struct s_compare_si :
    std::binary_function<
      typename boost::call_traits<input1>::param_type,
      typename boost::call_traits<true_t>::param_type,
      output
      >
  {
    typedef output return_type;

    const compare_op  c_op;
    const input1      compare_val;
    const output      false_val;
    s_compare_si(const input1& compare_val_, const output& false_val_) : c_op(), compare_val(compare_val_), false_val(false_val_) {}
    s_compare_si(const input1& compare_val_, const output& false_val_, const compare_op& comp) : c_op(comp), compare_val(compare_val_), false_val(false_val_) {}

    return_type operator()(
      typename boost::call_traits<input1>::param_type val1,
      typename boost::call_traits<true_t>::param_type val_true) const throw()
    {
      return (c_op(val1, compare_val) ? val_true:false_val);
    }

  };

  //! Compare an image with a constant value, assigns a constant false or the corresponding pixel of the true image to output image
  template <class image_in1_t, class image_true_t, class image_out_t, class op_t>
  yaRC image_compare_si(
    const image_in1_t& imin1,
    op_t op_comp,
    typename boost::call_traits<typename image_in1_t::pixel_type>::param_type v_compare,
    const image_true_t& imtrue,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_false,
    image_out_t& imout)
  {
    typedef s_compare_si<
      typename image_in1_t::pixel_type,
      typename image_true_t::pixel_type,
      typename image_out_t::pixel_type,
      op_t> operator_type;

    s_apply_binary_operator op_processor;

    operator_type op(v_compare, v_false, op_comp);
    return op_processor(imin1, imtrue, imout, op);
  }

  //! Compare an image with a constant value, assigns a constant false or the corresponding pixel of the true image to output image
  template <class image_in1_t, class image_true_t, class image_out_t>
  yaRC image_compare_si_stub(
    const image_in1_t& imin1,
    comparison_operations c,
    typename boost::call_traits<typename image_in1_t::pixel_type>::param_type v_compare,
    const image_true_t& im_true,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_false,
    image_out_t& imout)
  {

    BOOST_STATIC_ASSERT((boost::is_convertible<typename image_true_t::pixel_type, typename image_out_t::pixel_type>::value));

    switch(c)
    {
    case e_co_equal:
      return image_compare_si(imin1, std::equal_to<typename image_in1_t::pixel_type>(),v_compare, im_true, v_false, imout);
    case e_co_different:
      return image_compare_si(imin1, std::not_equal_to<typename image_in1_t::pixel_type>(),v_compare, im_true, v_false, imout);
    case e_co_superior:
      return image_compare_si(imin1, std::greater_equal<typename image_in1_t::pixel_type>(),v_compare, im_true, v_false, imout);
    case e_co_superior_strict:
      return image_compare_si(imin1, std::greater<typename image_in1_t::pixel_type>(),v_compare, im_true, v_false, imout);
    case e_co_inferior:
      return image_compare_si(imin1, std::less_equal<typename image_in1_t::pixel_type>(),v_compare, im_true, v_false, imout);
    case e_co_inferior_strict:
      return image_compare_si(imin1, std::less<typename image_in1_t::pixel_type>(),v_compare, im_true, v_false, imout);
    default:
      DEBUG_INFO("Comparison type not implemented");
      return yaRC_E_bad_parameters;
    }

  }











  //! Compare an image with another, assigns a constant false or the corresponding pixel of the true image to output image
  template <class input1, class input2, class true_t, class output, class compare_op>
  struct s_compare_ii
  {
    typedef output result_type;

    const compare_op  c_op;
    const output      false_val;
    s_compare_ii(const output& false_val_) : c_op(), false_val(false_val_) {}
    s_compare_ii(const output& false_val_, const compare_op& comp) : c_op(comp), false_val(false_val_) {}

    result_type operator()(
      typename boost::call_traits<input1>::param_type val1,
      typename boost::call_traits<input2>::param_type val2,
      typename boost::call_traits<true_t>::param_type val_true) const throw()
    {
      return (c_op(val1, val2) ? val_true:false_val);
    }

  };

  //! Compare an image with another, assigns a constant false or the corresponding pixel of the true image to output image
  template <class image_in1_t, class image_in2_t, class image_true_t, class image_out_t, class op_t>
  yaRC image_compare_ii(
    const image_in1_t& imin1,
    op_t op_comp,
    const image_in2_t& imin2,
    const image_true_t& imtrue,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_false,
    image_out_t& imout)
  {
    typedef s_compare_ii<
      typename image_in1_t::pixel_type,
      typename image_in2_t::pixel_type,
      typename image_true_t::pixel_type,
      typename image_out_t::pixel_type,
      op_t> operator_type;

    s_apply_ternary_operator op_processor;

    operator_type op(v_false, op_comp);
    return op_processor(imin1, imin2, imtrue, imout, op);
  }

  //! Compare an image with a constant value, assigns a constant false or the corresponding pixel of the true image to output image
  template <class image_in1_t, class image_in2_t, class image_true_t, class image_out_t>
  yaRC image_compare_ii_stub(
    const image_in1_t& imin1,
    comparison_operations c,
    const image_in2_t& imin2,
    const image_true_t& im_true,
    typename boost::call_traits<typename image_out_t::pixel_type>::param_type v_false,
    image_out_t& imout)
  {

    BOOST_STATIC_ASSERT((boost::is_convertible<typename image_true_t::pixel_type, typename image_out_t::pixel_type>::value));

    switch(c)
    {
    case e_co_equal:
      return image_compare_ii(imin1, std::equal_to<typename image_in1_t::pixel_type>(),imin2, im_true, v_false, imout);
    case e_co_different:
      return image_compare_ii(imin1, std::not_equal_to<typename image_in1_t::pixel_type>(),imin2, im_true, v_false, imout);
    case e_co_superior:
      return image_compare_ii(imin1, std::greater_equal<typename image_in1_t::pixel_type>(),imin2, im_true, v_false, imout);
    case e_co_superior_strict:
      return image_compare_ii(imin1, std::greater<typename image_in1_t::pixel_type>(),imin2, im_true, v_false, imout);
    case e_co_inferior:
      return image_compare_ii(imin1, std::less_equal<typename image_in1_t::pixel_type>(),imin2, im_true, v_false, imout);
    case e_co_inferior_strict:
      return image_compare_ii(imin1, std::less<typename image_in1_t::pixel_type>(),imin2, im_true, v_false, imout);
    default:
      DEBUG_INFO("Comparison type not implemented");
      return yaRC_E_bad_parameters;
    }

  }




  //! Compare an image with another, assigns the corresponding pixel of the true or false image to output image
  template <class input1, class input2, class true_t, class false_t, class output, class compare_op>
  struct s_compare_iii
  {
    typedef output result_type;

    const compare_op  c_op;
    s_compare_iii() : c_op() {}
    s_compare_iii(const compare_op& comp) : c_op(comp) {}

    result_type operator()(
      typename boost::call_traits<input1>::param_type  val1,
      typename boost::call_traits<input2>::param_type  val2,
      typename boost::call_traits<true_t>::param_type  val_true,
      typename boost::call_traits<false_t>::param_type val_false) const throw()
    {
      return (c_op(val1, val2) ? val_true:val_false);
    }

  };

  //! Compare an image with another, assigns the corresponding pixel of the true or false image to output image
  template <class image_in1_t, class image_in2_t, class image_true_t, class image_false_t, class image_out_t, class op_t>
  yaRC image_compare_iii(
    const image_in1_t&    imin1,
    op_t op_comp,
    const image_in2_t&    imin2,
    const image_true_t&   imtrue,
    const image_false_t&  imfalse,
    image_out_t& imout)
  {
    typedef s_compare_iii<
      typename image_in1_t::pixel_type,
      typename image_in2_t::pixel_type,
      typename image_true_t::pixel_type,
      typename image_false_t::pixel_type,
      typename image_out_t::pixel_type,
      op_t> operator_type;

    s_apply_fourary_operator op_processor;

    operator_type op(op_comp);
    return op_processor(imin1, imin2, imtrue, imfalse, imout, op);
  }

  //! Compare an image with another, assigns the corresponding pixel of the true or false image to output image
  template <class image_in1_t, class image_in2_t, class image_true_t, class image_false_t, class image_out_t>
  yaRC image_compare_iii_stub(
    const image_in1_t& imin1,
    comparison_operations c,
    const image_in2_t& imin2,
    const image_true_t& im_true,
    const image_false_t& im_false,
    image_out_t& imout)
  {

    BOOST_STATIC_ASSERT((boost::is_convertible<typename image_true_t::pixel_type, typename image_out_t::pixel_type>::value));

    switch(c)
    {
    case e_co_equal:
      return image_compare_iii(imin1, std::equal_to<typename image_in1_t::pixel_type>(),imin2, im_true, im_false, imout);
    case e_co_different:
      return image_compare_iii(imin1, std::not_equal_to<typename image_in1_t::pixel_type>(),imin2, im_true, im_false, imout);
    case e_co_superior:
    {
      if(are_images_same(imin1, im_true) && are_images_same(imin2, im_false))
        return supremum_images_t(imin1, imin2, imout);
      if(are_images_same(imin1, im_false) && are_images_same(imin2, im_true))
        return infimum_images_t(imin1, imin2, imout);
      return image_compare_iii(imin1, std::greater_equal<typename image_in1_t::pixel_type>(),imin2, im_true, im_false, imout);
    }
    case e_co_superior_strict:
      return image_compare_iii(imin1, std::greater<typename image_in1_t::pixel_type>(),imin2, im_true, im_false, imout);
    case e_co_inferior:
    {
      if(are_images_same(imin1, im_true) && are_images_same(imin2, im_false))
        return infimum_images_t(imin1, imin2, imout);
      if(are_images_same(imin1, im_false) && are_images_same(imin2, im_true))
        return supremum_images_t(imin1, imin2, imout);
      return image_compare_iii(imin1, std::less_equal<typename image_in1_t::pixel_type>(),imin2, im_true, im_false, imout);
    }
    case e_co_inferior_strict:
      return image_compare_iii(imin1, std::less<typename image_in1_t::pixel_type>(),imin2, im_true, im_false, imout);
    default:
      DEBUG_INFO("Comparison type not implemented");
      return yaRC_E_bad_parameters;
    }

  }

  //! Compare an image with a constant, assigns the corresponding pixel of the true or false image to output image
  template <class input1, class true_t, class false_t, class output, class compare_op>
  struct s_compare_sii
  {
    typedef output result_type;

    const compare_op  c_op;
    const input1      compare_val;
    s_compare_sii(const input1& compare_val_) : c_op(), compare_val(compare_val_) {}
    s_compare_sii(const input1& compare_val_, const compare_op& comp) : c_op(comp), compare_val(compare_val_) {}

    result_type operator()(
      typename boost::call_traits<input1>::param_type  val1,
      typename boost::call_traits<true_t>::param_type  val_true,
      typename boost::call_traits<false_t>::param_type val_false) const throw()
    {
      return (c_op(val1, compare_val) ? val_true:val_false);
    }

  };

  //! Compare an image with a constant, assigns the corresponding pixel of the true or false image to output image
  template <class image_in1_t, class image_true_t, class image_false_t, class image_out_t, class op_t>
  yaRC image_compare_sii(
    const image_in1_t&    imin1,
    op_t op_comp,
    typename boost::call_traits<typename image_in1_t::pixel_type>::param_type v_compare,
    const image_true_t&   imtrue,
    const image_false_t&  imfalse,
    image_out_t& imout)
  {
    typedef s_compare_sii<
      typename image_in1_t::pixel_type,
      typename image_true_t::pixel_type,
      typename image_false_t::pixel_type,
      typename image_out_t::pixel_type,
      op_t> operator_type;

    s_apply_ternary_operator op_processor;

    operator_type op(v_compare, op_comp);
    return op_processor(imin1, imtrue, imfalse, imout, op);
  }

  //! Compare an image with a constant, assigns the corresponding pixel of the true or false image to output image
  template <class image_in1_t, class image_true_t, class image_false_t, class image_out_t>
  yaRC image_compare_sii_stub(
    const image_in1_t& imin1,
    comparison_operations c,
    typename boost::call_traits<typename image_in1_t::pixel_type>::param_type v_compare,
    const image_true_t& im_true,
    const image_false_t& im_false,
    image_out_t& imout)
  {

    BOOST_STATIC_ASSERT((boost::is_convertible<typename image_true_t::pixel_type, typename image_out_t::pixel_type>::value));

    switch(c)
    {
    case e_co_equal:
      return image_compare_sii(imin1, std::equal_to<typename image_in1_t::pixel_type>(),v_compare, im_true, im_false, imout);
    case e_co_different:
      return image_compare_sii(imin1, std::not_equal_to<typename image_in1_t::pixel_type>(),v_compare, im_true, im_false, imout);
    case e_co_superior:
      return image_compare_sii(imin1, std::greater_equal<typename image_in1_t::pixel_type>(),v_compare, im_true, im_false, imout);
    case e_co_superior_strict:
      return image_compare_sii(imin1, std::greater<typename image_in1_t::pixel_type>(),v_compare, im_true, im_false, imout);
    case e_co_inferior:
      return image_compare_sii(imin1, std::less_equal<typename image_in1_t::pixel_type>(),v_compare, im_true, im_false, imout);
    case e_co_inferior_strict:
      return image_compare_sii(imin1, std::less<typename image_in1_t::pixel_type>(),v_compare, im_true, im_false, imout);
    default:
      DEBUG_INFO("Comparison type not implemented");
      return yaRC_E_bad_parameters;
    }

  }

  //! @} doxygroup: pp_comp_details_grp
}

#endif /* YAYI_COMPARE_T_HPP__ */
