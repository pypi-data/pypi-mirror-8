#ifndef YAYI_CHANNELS_PROCESS_T_HPP__
#define YAYI_CHANNELS_PROCESS_T_HPP__



#include <algorithm>
#include <functional>
#include <iostream>
#include <yayiImageCore/include/ApplyToImage_T.hpp>
#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_binary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_ternary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_fourary_t.hpp>

#include  <boost/type_traits/is_complex.hpp>

namespace yayi
{
  /*!@defgroup pp_channel_details_grp Channels processing function details
   * @ingroup pp_channel_grp
   *
   * @{
   */


  //! Main functor for the simple copy of one channel a scalar representation of it
  template <class pixel_in, class pixel_out, class Enable = void>
  struct s_copy_one_channel : public std::unary_function<pixel_in, pixel_out>
  {
    typename pixel_in::dimension::value_type const dimension;

    s_copy_one_channel(typename pixel_in::dimension::value_type const d_) : dimension(d_)
    {}

    pixel_out operator()(const pixel_in& p) const
    {
      return static_cast<pixel_out>(p[dimension]);
    }
  };

  //! Specializing of s_copy_one_channel in case the types match
  template <class pixel_in>
  struct s_copy_one_channel<pixel_in, typename pixel_in::value_type, boost::disable_if< boost::is_complex<pixel_in> > > :
    public std::unary_function<pixel_in, typename boost::add_reference<typename boost::add_const<typename pixel_in::value_type>::type>::type>
  {
    typename pixel_in::dimension::value_type const dimension;
    typedef typename boost::add_reference<typename boost::add_const<typename pixel_in::value_type>::type>::type result_type;

    s_copy_one_channel(typename pixel_in::dimension::value_type const d_) : dimension(d_)
    {}

    result_type operator()(const pixel_in& p) const
    {
      return p[dimension];
    }
  };

  //! Specialization of s_copy_into_channel for complex types: channel 0 is the real part while channel 1 is the imaginary part.
  template <class pixel_in_scalar_t>
  struct s_copy_one_channel<std::complex<pixel_in_scalar_t>, pixel_in_scalar_t > :
    public std::unary_function<typename boost::add_reference<typename boost::add_const<std::complex<pixel_in_scalar_t> >::type>::type, pixel_in_scalar_t>
  {
    unsigned char const dimension;
    typedef std::complex<pixel_in_scalar_t> pixel_in_t;
    typedef pixel_in_scalar_t pixel_out_t;

    s_copy_one_channel(unsigned char d_) : dimension(d_)
    {
      if(dimension != 0 && dimension != 1)
        throw errors::yaException(yaRC_E_bad_parameters);
    }

    pixel_out_t operator()(const pixel_in_t& p) const YAYI_THROW_DEBUG_ONLY__
    {
      return (dimension == 0 ? p.real() : p.imag());
    }
  };

  //! Template function for copying one of the channels of the input image into another image
  //! For complex images, dimension 0 stands for the real part, while dimension 1 stands for the imaginary part
  template <class image_in_, class image_out_>
  yaRC copy_one_channel_image_t(const image_in_& imin, const unsigned int dimension_i, image_out_& imo)
  {
    typedef s_copy_one_channel<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(dimension_i);
    return op_processor(imin, imo, op);
  }




  //! Main functor for the simple copy of one channel a scalar representation of it
  template <class pixel_in, class pixel_out>
  struct s_copy_into_channel : public std::binary_function<pixel_in, pixel_out, void>
  {
    typename pixel_out::dimension::value_type const dimension;

    s_copy_into_channel(typename pixel_out::dimension::value_type const d_) : dimension(d_)
    {
      if(dimension < 0 && dimension >= pixel_out::dimension::value)
        throw errors::yaException(yaRC_E_bad_parameters);
    }

    void operator()(const pixel_in& p_in, pixel_out& p) const YAYI_THROW_DEBUG_ONLY__
    {
      p[dimension] = p_in;
    }
  };

  //! Specialization of s_copy_into_channel for complex types: channel 0 is the real part while channel 1 is the imaginary part.
  template <class pixel_in_t, class pixel_out_scalar_t>
  struct s_copy_into_channel<pixel_in_t, std::complex<pixel_out_scalar_t> > : public std::binary_function<pixel_in_t, std::complex<pixel_out_scalar_t>, void>
  {
    unsigned char const dimension;
    typedef std::complex<pixel_out_scalar_t> pixel_out_t;

    s_copy_into_channel(unsigned char d_) : dimension(d_)
    {
      if(dimension != 0 && dimension != 1)
        throw errors::yaException(yaRC_E_bad_parameters);
    }

    void operator()(const pixel_in_t& p_in, pixel_out_t& p) const YAYI_THROW_DEBUG_ONLY__
    {
      if(dimension == 0)
        p = pixel_out_t(static_cast<pixel_out_scalar_t>(p_in), p.imag());
      else
        p = pixel_out_t(p.real(), static_cast<pixel_out_scalar_t>(p_in));
    }
  };

  //! Template function for copying one of the channels of the input image into another image
  //! For complex images, dimension 0 stands for the real part and dimension 1 for the imaginary part
  template <class image_in_, class image_out_>
  yaRC copy_into_channel_image_t(const image_in_& imin, const unsigned int dimension_o, image_out_& imo)
  {
    typedef s_copy_into_channel<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_binary_operator op_processor;

    operator_type op(dimension_o);
    return op_processor(imin, imo, op);
  }







  //! Functor for copying one channel of the input pixel into one channel of the output pixel
  template <class pixel_in, class pixel_out>
  struct s_copy_one_channel_into_another :
    public std::binary_function<pixel_in, pixel_out, void>
  {
    typename pixel_in::dimension::value_type const dimension_in;
    typename pixel_out::dimension::value_type const dimension_out;

    s_copy_one_channel_into_another(
      typename pixel_in::dimension::value_type const di_,
      typename pixel_out::dimension::value_type const do_) : dimension_in(di_), dimension_out(do_)
    {}
    void operator()(const pixel_in& p, pixel_out& o) const
    {
      o[dimension_out] = static_cast<typename pixel_out::value_type>(p[dimension_in]);
    }
  };

  //! Specializing of s_copy_one_channel_into_another in case the types match
  template <class pixel_in>
  struct s_copy_one_channel_into_another<pixel_in, pixel_in> :
    public std::binary_function<pixel_in, pixel_in, void>
  {
    typename pixel_in::dimension::value_type const dimension_in;
    typename pixel_in::dimension::value_type const dimension_out;

    s_copy_one_channel_into_another(
      typename pixel_in::dimension::value_type const di_,
      typename pixel_in::dimension::value_type const do_) : dimension_in(di_), dimension_out(do_)
    {}
    void operator()(const pixel_in& p, pixel_in& o) const
    {
      o[dimension_out] = p[dimension_in];
    }
  };

  //! Template function for copying a channel of the input image into a channel of the output image
  template <class image_in_, class image_out_>
  yaRC copy_one_channel_image_into_another_t(const image_in_& imin, const unsigned int dimension_i, const unsigned int dimension_o, image_out_& imo)
  {
    typedef s_copy_one_channel_into_another<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_binary_operator op_processor;

    operator_type op(dimension_i, dimension_o);
    return op_processor(imin, imo, op);
  }



  //! Pixel-wise functor for channel extraction
  template <class pixel_in, class pixel_out>
  struct s_extract_all_3_channels
  {
    typedef void result_type;
    void operator()(const pixel_in& p, pixel_out& o1, pixel_out& o2, pixel_out& o3) const
    {
      o1 = p[0];
      o2 = p[1];
      o3 = p[2];
    }
  };

  //! Template function for copying a channel of the input image into a channel of the output image
  template <class image_in_, class image_out_>
  yaRC channels_split_t(const image_in_& imin, image_out_& imo1, image_out_& imo2, image_out_& imo3)
  {
    typedef s_extract_all_3_channels<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_fourary_operator op_processor;

    operator_type op;
    return op_processor(imin, imo1, imo2, imo3, op);
  }


  //! Pixel-wise functor for channel composition
  template <class pixel_in, class pixel_out>
  struct s_compose_all_3_channels
  {
    typedef void result_type;
    void operator()(const pixel_in& p1, const pixel_in& p2, const pixel_in& p3, pixel_out& o) const
    {
      o[0] = p1;
      o[1] = p2;
      o[2] = p3;
    }
  };

  //! Template function for recomposing a multichannel image from multiple sources
  template <class image_in_, class image_out_>
  yaRC channels_compose_t(const image_in_& imin1, const image_in_& imin2, const image_in_& imin3, image_out_& imo)
  {
    typedef s_compose_all_3_channels<
      typename image_in_::pixel_type,
      typename image_out_::pixel_type>  operator_type;

    s_apply_fourary_operator op_processor;

    operator_type op;
    return op_processor(imin1, imin2, imin3, imo, op);
  }



  //! Pixel-wise functor for extraction of modulus and argument from complex pixels
  template <class pixel_in_t, class pixel_out_t>
  struct s_split_complex_to_modulus_argument;

  //! We restrict the definition of this functor to complex types
  template <class pixel_in_scalar_t, class pixel_out_t>
  struct s_split_complex_to_modulus_argument<std::complex<pixel_in_scalar_t>, pixel_out_t>
  {
    typedef std::complex<pixel_in_scalar_t> pixel_in_t;
    typedef void result_type;
    void operator()(const pixel_in_t& p, pixel_out_t& mod_, pixel_out_t& arg_) const
    {
      mod_ = std::abs(p);
      arg_ = std::arg(p);
    }
  };

  //! Template function for extracting the modulus and argument of a complex image
  template <class image_in_t, class image_out_t>
  yaRC extract_modulus_argument_t(const image_in_t& imin, image_out_t& im_modulus, image_out_t& im_argument)
  {
    typedef s_split_complex_to_modulus_argument<
      typename image_in_t::pixel_type,
      typename image_out_t::pixel_type>  operator_type;

    s_apply_ternary_operator op_processor;

    operator_type op;
    return op_processor(imin, im_modulus, im_argument, op);
  }


 //! Pixel-wise functor for extraction of modulus and argument from complex pixels
  template <class pixel_in_t, class pixel_out_t>
  struct s_compose_complex_from_modulus_argument;

  //! We restrict the definition of this functor to complex types
  template <class pixel_in_t, class pixel_out_scalar_t>
  struct s_compose_complex_from_modulus_argument<pixel_in_t, std::complex<pixel_out_scalar_t> >
  {
    typedef std::complex<pixel_out_scalar_t> pixel_out_t;
    typedef void result_type;
    void operator()(const pixel_in_t& mod_, const pixel_in_t& arg_, pixel_out_t& p) const
    {
      p = std::polar(mod_, arg_);
    }
  };

  //! Template function for composing a complex image from its modulus and argument representation
  template <class image_in_t, class image_out_t>
  yaRC compose_from_modulus_argument_t(image_in_t const& im_modulus, image_in_t const& im_argument, image_out_t& imout)
  {
    typedef s_compose_complex_from_modulus_argument<
      typename image_in_t::pixel_type,
      typename image_out_t::pixel_type>  operator_type;

    s_apply_ternary_operator op_processor;

    operator_type op;
    return op_processor(im_modulus, im_argument, imout, op);
  }
//! @} doxygroup: pp_channel_details_grp
}

#endif
