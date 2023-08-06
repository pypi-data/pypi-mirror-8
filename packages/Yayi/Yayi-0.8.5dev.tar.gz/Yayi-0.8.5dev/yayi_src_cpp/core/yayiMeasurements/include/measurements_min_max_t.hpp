#ifndef YAYI_MEASUREMENTS_MIN_MAX_T_HPP__
#define YAYI_MEASUREMENTS_MIN_MAX_T_HPP__

#include <boost/call_traits.hpp>
#include <functional>
//#include <boost/limits.hpp>
#include <boost/numeric/conversion/bounds.hpp>

#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>


namespace yayi
{
  namespace measurements
  {
    /*!@defgroup meas_min_max_details_grp Min/max template functions
     * @ingroup meas_details_grp
     * @{
     */

    //!@concept{measurement_functor_concepts}
    template <class T>
    struct s_meas_min_max: public std::unary_function<T, void>
    {
      typedef std::pair<T, T> result_type;

      T min_, max_;
      s_meas_min_max() : min_(boost::numeric::bounds<T>::highest()), max_(boost::numeric::bounds<T>::lowest()) {}
      void operator()(const T& v) throw()
      {
        min_ = std::min(v, min_);
        max_ = std::max(v, max_);
      }

      result_type result() const throw()
      {
        return std::make_pair(min_, max_);
      }

      void clear_result() throw()
      {
        min_ = boost::numeric::bounds<T>::highest();
        max_ = boost::numeric::bounds<T>::lowest();
      }
    };

    //!@todo get rid of the variant
    template <class image_in_t>
    yaRC image_meas_min_max_t(const image_in_t& im, variant& out)
    {
      typedef typename image_in_t::pixel_type out_t;
      typedef s_meas_min_max<out_t> operator_type;

      s_apply_unary_operator op_processor;

      operator_type op;
      yaRC res = op_processor(im, op);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured during the computation of the min/max: " << res);
        return res;
      }

      out = op.result();
      return yaRC_ok;
    }
    //! @}

  }
}


#endif /* YAYI_MEASUREMENTS_MIN_MAX_T_HPP__ */
