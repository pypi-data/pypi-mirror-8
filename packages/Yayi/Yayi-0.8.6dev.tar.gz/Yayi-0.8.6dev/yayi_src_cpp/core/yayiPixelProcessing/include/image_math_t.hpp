#ifndef YAYI_PIXEL_IMAGE_MATH_T_HPP__
#define YAYI_PIXEL_IMAGE_MATH_T_HPP__

#include <yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiCommon/include/common_types_T.hpp>

#include <yayiImageCore/include/ApplyToImage_zeroary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiPixelProcessing/include/image_compare_T.hpp> //look up table

#include <boost/math/distributions/normal.hpp>
#include <boost/random/uniform_01.hpp>
#include <boost/random/mersenne_twister.hpp>
#include <boost/numeric/conversion/bounds.hpp>
#include <boost/numeric/conversion/conversion_traits.hpp>

#include <cmath>


/*!@file
 * This file contains the implementation of several mathematical function (log, power, sqrt, random...)
 */

namespace yayi
{
  /*!@defgroup pp_maths_details_grp Mathematical functions details
   * @ingroup pp_maths_grp
   * @brief Implements some basic mathematic functions (log, power, square root, etc).
   * @{
   */

  /*! Natural logarithm functor.
   * @tparam U input pixels type
   * @tparam V output pixels type
   */
  template <class U, class V = U>
  struct s_log : public std::unary_function<U, V>
  {
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      return std::log(u);
    }
  };

  /*!@brief Specializing of logarithm for yaUINT8 type.
   * This implementation uses a look-up table.
   * @tparam V output pixels type
   */
  template <class V>
  struct s_log<yaUINT8, V> : public std::unary_function<yaUINT8, V>
  {
    typedef yaUINT8 U;
    typedef std::vector<V> value_type;
    static const value_type values;

    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      return values[u];
    }

    //!@internal
    //!Generates the look-up table
    static value_type generate()
    {
      std::vector<V> out(boost::numeric::bounds<U>::highest() + 1);
      out.push_back(-std::numeric_limits<V>::infinity());
      for(U i = 1; i < boost::numeric::bounds<U>::highest(); i++)
        out.push_back(std::log(float(i)));

      return out;
    }
  };
  template <class V>
  typename s_log<yaUINT8, V>::value_type const s_log<yaUINT8, V>::values = s_log<yaUINT8, V>::generate();


  //! Computes the logarithm of each pixels of the image
  template <class imin_t, class imout_t>
  yaRC logarithm_t(const imin_t &imin, imout_t &imout)
  {
    typedef s_log<
      typename imin_t::pixel_type,
      typename imout_t::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op;
    return op_processor(imin, imout, op);
  }




  //! Exponential of the input image.
  template <class U, class V = U, bool B = false>
  struct s_exp : public std::unary_function<U, V>
  {
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      typedef boost::numeric::conversion_traits<U,V> t_to_v_traits;

      return static_cast<result_type>(std::exp(typename t_to_v_traits::supertype(u))); // Raffi: check here !
    }
  };

  //! Specializing of the exponential using look-up table.
  //! @tparam U input pixel type
  //! @tparam V output pixel type
  template <class U, class V>
  struct s_exp<U, V, true> : public std::unary_function<U, V>
  {
    typedef std::vector<V> value_type;
    static const value_type values;

    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      return values[u];
    }

    //!@internal
    //!Generates the look-up table, according to the properties of type U.
    static value_type generate()
    {
      value_type out(boost::numeric::bounds<U>::highest() - boost::numeric::bounds<U>::lowest() + 1);
      for(U i = boost::numeric::bounds<U>::lowest(); i < boost::numeric::bounds<U>::highest(); i++)
        out.push_back(::exp(i));

      return out;
    }
  };

  template <class U, class V>
  typename s_exp<U, V, true>::value_type const s_exp<U, V, true>::values = s_exp<U, V, true>::generate();





  //! Computes the exponential of each pixels of the image
  template <class imin_t, class imout_t>
  yaRC exponential_t(const imin_t &imin, imout_t &imout)
  {
    typedef s_exp<
      typename imin_t::pixel_type,
      typename imout_t::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op;
    return op_processor(imin, imout, op);
  }



  /*! Computes the power of a pixel.
   *
   * A specializing of this class uses a look-up table.
   * @tparam U input pixel type
   * @tparam V output pixel type
   * @warning overflows are not handled.
   */
  template <class U, class V = U>
  struct s_power : public std::unary_function<U, V>
  {
    typedef typename std::unary_function<U, V>::result_type result_type;
    double const value;
    s_power(double value_) : value(value_){}
    s_power(const s_power& r_) : value(r_.value){}
    result_type operator()(const U &u) const
    {
      typedef boost::numeric::conversion_traits<U,double> t_to_v_traits;
      return static_cast<result_type>(std::pow(typename t_to_v_traits::supertype(u), value));// Raffi: check here !
    }
  };

  //FIXME to raffi i fix compilation but i don't think i follow the semantic
  //! Specializing of s_power for the special case of yaUINT8.
  template <class output_t>
  struct s_power<yaUINT8, output_t> : public s_lookup_table_transform_op<yaUINT8, output_t>
  {

    typedef yaUINT8 input_t;
    typedef s_lookup_table_transform_op<input_t, output_t> op_lookup_t;
    typedef typename op_lookup_t::result_type result_type;
    typedef typename op_lookup_t::argument_type argument_type;

    s_power(double value_) : op_lookup_t()
    {
      typedef boost::numeric::conversion_traits<input_t,double> t_to_v_traits;
      for(unsigned int i = 0; i < static_cast<unsigned int>(std::numeric_limits<input_t>::max() - std::numeric_limits<input_t>::min()); i++)
      {
        this->table[i] = static_cast<result_type>(std::pow(typename t_to_v_traits::supertype(i), value_));
      }
    }
    s_power(const s_power& r_) : op_lookup_t()
    {
      for(unsigned int i = 0; i < std::numeric_limits<input_t>::max() - std::numeric_limits<input_t>::min(); i++)
      {
        this->table[i] = r_->table[i];
      }
    }
    result_type operator()(argument_type val) const throw()
    {
      return this->op_lookup_t::operator ()(val);
    }
  };


  /*! Specializing of s_power for the case of pixel_3.
   *
   * Raises each component of the pixel to the same power.
   */
  template <class U, class V>
  struct s_power<s_compound_pixel_t<U, mpl::int_<3> >, s_compound_pixel_t<V, mpl::int_<3> > > :
    public std::unary_function<s_compound_pixel_t<U, mpl::int_<3> >, s_compound_pixel_t<V, mpl::int_<3> > >
  {
    typedef s_power<s_compound_pixel_t<U, mpl::int_<3> >, s_compound_pixel_t<V, mpl::int_<3> > > this_type;
    typedef s_compound_pixel_t<U, mpl::int_<3> > pixel_in_t;
    typedef s_compound_pixel_t<V, mpl::int_<3> > pixel_out_t;

    s_power<typename pixel_in_t::value_type, typename pixel_out_t::value_type> intern_power;

    s_power(double value_) : intern_power(value_){}
    s_power(const s_power& r_) : intern_power(r_.intern_power){}
    typename this_type::result_type operator()(const typename this_type::argument_type &u) const
    {
      return typename this_type::result_type(intern_power(u.a), intern_power(u.b), intern_power(u.c));
    }
  };

  //! Computes the power of each pixels of the image
  template <class imin_t, class imout_t>
  yaRC power_t(const imin_t &imin, const double var, imout_t &imout)
  {
    typedef s_power<
      typename imin_t::pixel_type,
      typename imout_t::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(var);
    return op_processor(imin, imout, op);
  }


  /*! Squares the value of a pixel.
   *
   * This is a special case of s_power.
   * @warning overflow are not handled.
   */
  template <class U, class V = U>
  struct s_square : public std::unary_function<U, V>
  {
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      return u*u;
    }
  };

  //! Computes the square of each pixels of the image
  template <class imin_t, class imout_t>
  yaRC square_t(const imin_t &imin, imout_t &imout)
  {
    typedef s_square<
      typename imin_t::pixel_type,
      typename imout_t::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op;
    return op_processor(imin, imout, op);
  }


  //@todo make internal tables
  template <class U, class V = U>
  struct s_square_root : public std::unary_function<U, V>
  {
    typedef typename std::unary_function<U, V>::result_type result_type;
    result_type operator()(const U &u) const
    {
      typedef boost::numeric::conversion_traits<U,V> t_to_v_traits;
      return static_cast<result_type>(std::sqrt(typename t_to_v_traits::supertype(u)));
    }
  };

  //! Computes the square root of each pixels of the image
  template <class imin_t, class imout_t>
  yaRC square_root_t(const imin_t &imin, imout_t &imout)
  {
    typedef s_square_root<
      typename imin_t::pixel_type,
      typename imout_t::pixel_type>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op;
    return op_processor(imin, imout, op);
  }


  //! Returns a random value between 0 and 1
  inline yaF_double random_value_double()
  {
    typedef boost::mt19937 random_generator_type;
    //typedef boost::uniform_01<yaF_double> distribution_type;
    typedef boost::uniform_01<random_generator_type, yaF_double> distribution_generator_t;
    static distribution_generator_t generator = distribution_generator_t(random_generator_type());  // add time there ?

    return generator();
  }


  //! Generic distribution generator functor
  template <class T = yaF_double, class distribution = boost::math::normal >
  struct s_generic_distribution
  {
    typedef T result_type;
    distribution dist;
    s_generic_distribution() : dist(){}
    s_generic_distribution(const distribution& dist_) : dist(dist_){}
    result_type operator()() const
    {
      return static_cast<result_type>(boost::math::quantile(dist, random_value_double()));
    }
  };

  //! Generates the pixels of the image as being drawn from a gaussian distribution
  template <class iminout_t>
  yaRC generate_gaussian_random_t(iminout_t &imin, yaF_double mean = 0., yaF_double std_deviation = 1.)
  {
    typedef boost::math::normal distribution_t;
    typedef s_generic_distribution<
      typename iminout_t::pixel_type,
      distribution_t>  operator_type;

    s_apply_zeroary_operator op_processor;

    operator_type op(distribution_t(mean, std_deviation));
    return op_processor(imin, op);
  }




  /*! Matrix (linear) transformation of a multichannel pixel.
   *
   * @note the current implementation supposes the matrix square, which does not change the dimension of the pixel.
   * Relaxing this contraint may be considered in order to have for instance, a subspace projection.
   */
  template <class input_t, class output_t, class matrix_t >
  struct s_apply_matrix : public std::unary_function<input_t, output_t>
  {
    typedef output_t result_type;
    typedef input_t input_type;

    typedef typename output_t::scalar_value_type scalar_value_type;
    matrix_t const m;

    s_apply_matrix(const matrix_t& m_) : m(m_)
    {
      YAYI_ASSERT(m.size1() == m.size2() && m.size1() > 0, "The provided matrix is not square");
    }
    result_type operator()(const input_type& v) const
    {
      // copying locally the data may be faster ?
      result_type out;
      for(typename matrix_t::size_type i(0); i < m.size1(); i++)
      {
        typename type_description::s_sum_supertype<typename input_t::scalar_value_type>::type sum(0);
        for(typename matrix_t::size_type j(0); j < m.size1(); j++)
          sum += m(i,j) * v[j];
        out[i] = static_cast<scalar_value_type>(sum);
      }
      return out;
    }
  };

  /*! Specializing of s_apply_matrix for pixel_3.
   *
   * This implementation is slightly faster since the internal loop is developped, the size of the matrix
   * and the working vectors (pixels) being known at compilation time.
   */
  template <class input_scalar_t, class output_scalar_t, class matrix_t >
  struct s_apply_matrix<
    s_compound_pixel_t<input_scalar_t, mpl::int_<3> >,
    s_compound_pixel_t<output_scalar_t, mpl::int_<3> >,
    matrix_t>
    : public std::unary_function<
        s_compound_pixel_t<input_scalar_t, mpl::int_<3> >,
        s_compound_pixel_t<output_scalar_t, mpl::int_<3> >
      >
  {
    //typedef output_t result_type;
    typedef s_compound_pixel_t<input_scalar_t, mpl::int_<3> > input_type;
    typedef s_compound_pixel_t<output_scalar_t, mpl::int_<3> > result_type;
    typedef output_scalar_t scalar_value_type;
    matrix_t const m;

    s_apply_matrix(const matrix_t& m_) : m(m_)
    {
      YAYI_ASSERT(m.size1() == m.size2() && m.size2() == 3, "The provided matrix is not square or not of dimension 3");
    }
    result_type operator()(const input_type& v) const
    {
      return result_type(
        static_cast<scalar_value_type>(m(0,0) * v.a + m(0,1) * v.b + m(0,2) * v.c),
        static_cast<scalar_value_type>(m(1,0) * v.a + m(1,1) * v.b + m(1,2) * v.c),
        static_cast<scalar_value_type>(m(2,0) * v.a + m(2,1) * v.b + m(2,2) * v.c) );
    }
  };



  //! Applies a matrix transformation to every pixels of the image. The input and output images should
  //! have the same number of channels.
  template <class imin_t, class imout_t, class matrix_t>
  yaRC apply_matrix_t(imin_t const &imin, matrix_t const &m, imout_t const &imout)
  {
    typedef s_apply_matrix<
      typename imin_t::pixel_type,
      typename imout_t::pixel_type,
      matrix_t>  operator_type;

    s_apply_unary_operator op_processor;

    operator_type op(m);
    return op_processor(imin, imout, op);
  }

  //! @} doxygroup: pp_maths_details_grp
}

#endif

