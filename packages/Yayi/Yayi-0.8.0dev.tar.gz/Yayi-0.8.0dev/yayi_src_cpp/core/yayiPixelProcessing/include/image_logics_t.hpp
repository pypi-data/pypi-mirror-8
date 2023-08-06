#ifndef YAYI_PIXEL_IMAGE_LOGIC_T_HPP__
#define YAYI_PIXEL_IMAGE_LOGIC_T_HPP__

/*!@file
 * This file defines the logic template operations on images
 */

#include <boost/call_traits.hpp>
#include <functional>
#include <yayiPixelProcessing/image_arithmetics.hpp>
#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_binary_t.hpp>
#include <yayiCommon/common_errors.hpp> // to remove

namespace yayi
{
  /*!@defgroup pp_logics_details_grp Logical and bitwise operators on template images and pixels
   * @ingroup pp_logics_grp
   *
   * @{
   */

  /*! Complement of a pixel (bitwise not)
   * @note Defined only on integer types (look for specializing for handling of compound types). Instanciation on floating
   * type results in a compilation error.
   */
  template <class U, class V = U>
  struct s_bitwise_not : public std::unary_function<U, V>
  {
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const throw()
    {
      return ~u;
    }
  };

  //! Bitwise complement of the input image
  template <class image_in1_, class image_out_>
  yaRC bitwise_not_images_t(
    const image_in1_& imin1,
    image_out_& imo)
  {
    typedef s_bitwise_not<
      typename image_in1_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op;
    return op_processor(imin1, imo, op);
  }


  //! Bitwise and
  template <class U, class V, class W>
  struct s_bitwise_and : public std::binary_function<U, V, W>
  {
    typedef typename std::binary_function<U, V, W>::result_type result_type;
    result_type operator()(const U &u, const V &v) const throw()
    {
      return u & v;
    }
  };

  //! Bitwise "and", specialization for pixel3 input1/output, and scalar input2 (mask image)
  template <class U, class V, class W>
  struct s_bitwise_and<s_compound_pixel_t<U, mpl::int_<3> >, V, s_compound_pixel_t<W, mpl::int_<3> > > :
    public std::binary_function< s_compound_pixel_t<U, mpl::int_<3> >, V, s_compound_pixel_t<W, mpl::int_<3> > >
  {
    typedef s_compound_pixel_t<U, mpl::int_<3> > p1_t;
    typedef V p2_t;
    typedef s_compound_pixel_t<W, mpl::int_<3> > result_type;

    result_type operator()(const p1_t &u, const p2_t &v) const throw()
    {
      return result_type(u[0] & v, u[1] & v, u[2] & v);
    }
  };


  //! Bitwise "and", specialization for pixel3
  template <class U, class V, class W>
  struct s_bitwise_and<s_compound_pixel_t<U, mpl::int_<3> >, s_compound_pixel_t<V, mpl::int_<3> >, s_compound_pixel_t<W, mpl::int_<3> > > :
    public std::binary_function< s_compound_pixel_t<U, mpl::int_<3> >, s_compound_pixel_t<V, mpl::int_<3> >, s_compound_pixel_t<W, mpl::int_<3> > >
  {
    typedef s_compound_pixel_t<U, mpl::int_<3> > p1_t;
    typedef s_compound_pixel_t<V, mpl::int_<3> > p2_t;
    typedef s_compound_pixel_t<W, mpl::int_<3> > result_type;

    result_type operator()(const p1_t &u, const p2_t &v) const throw()
    {
      return result_type(u[0] & v[0], u[1] & v[1], u[2] & v[2]);
    }
  };


  //! Bitwise and
  template <class image_in1_, class image_in2_, class image_out_>
  yaRC bitwise_and_images_t(const image_in1_& imin1, const image_in2_& imin2, image_out_& imo)
  {
    typedef s_bitwise_and<
      typename image_in1_::pixel_type,
      typename image_in2_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_binary_operator op_processor;

    operator_type op;
    return op_processor(imin1, imin2, imo, op);
  }


  //! Bitwise or
  template <class U, class V, class W>
  struct s_bitwise_or : public std::binary_function<U, V, W>
  {
    typedef typename std::binary_function<U, V, W>::result_type result_type;
    result_type operator()(const U &u, const V &v) const throw()
    {
      return u | v;
    }
  };

  //! Bitwise or - sprecialization for pixel3
  template <class U, class V, class W>
  struct s_bitwise_or<
    s_compound_pixel_t<U, mpl::int_<3> >,
    s_compound_pixel_t<V, mpl::int_<3> >,
    s_compound_pixel_t<W, mpl::int_<3> > > :
    public std::binary_function< s_compound_pixel_t<U, mpl::int_<3> >, s_compound_pixel_t<V, mpl::int_<3> >, s_compound_pixel_t<W, mpl::int_<3> > >
  {
    typedef s_compound_pixel_t<U, mpl::int_<3> > p1_t;
    typedef s_compound_pixel_t<V, mpl::int_<3> > p2_t;
    typedef s_compound_pixel_t<W, mpl::int_<3> > result_type;

    result_type operator()(const p1_t &u, const p2_t &v) const throw()
    {
      return result_type(u[0] | v[0], u[1] | v[1], u[2] | v[2]);
    }
  };



  //! Bitwise or
  template <class image_in1_, class image_in2_, class image_out_>
  yaRC bitwise_or_images_t(const image_in1_& imin1, const image_in2_& imin2, image_out_& imo)
  {
    typedef s_bitwise_or<
      typename image_in1_::pixel_type,
      typename image_in2_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_binary_operator op_processor;

    operator_type op;
    return op_processor(imin1, imin2, imo, op);
  }

  //! @} doxygroup: pp_logics_details_grp

}

#endif /* YAYI_PIXEL_IMAGE_LOGIC_T_HPP__ */
