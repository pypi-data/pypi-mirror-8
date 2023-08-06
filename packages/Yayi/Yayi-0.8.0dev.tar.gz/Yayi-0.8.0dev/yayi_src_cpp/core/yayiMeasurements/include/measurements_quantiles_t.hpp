#ifndef YAYI_MEASUREMENTS_QUANTILES_T_HPP__
#define YAYI_MEASUREMENTS_QUANTILES_T_HPP__

#include <boost/call_traits.hpp>
#include <functional>
#include <boost/accumulators/accumulators.hpp>
#include <boost/accumulators/statistics/stats.hpp>
#include <boost/accumulators/statistics/median.hpp>
#include <boost/numeric/conversion/bounds.hpp>

#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>


namespace yayi
{
  namespace measurements
  {
    /*!@defgroup meas_quantile_details_grp Quantile functions implementation details.
     * @ingroup meas_details_grp
     * @{
     */
    namespace bacc = boost::accumulators;

    /*!@brief Functor for computing the median over a set of values
     *
     * The function object implements the @ref measurement_functor_concepts "Measurement function objects" concept.
     * The accumulation is performed against successive calls to operator(). The result is given by a call to the "result" method
     * @note this is mainly a wrapper over the median computation of boost::accumulators. Some more efficient implementation
     * may exist.
     *
     * @todo implement/specialize a "many channel" version of this accumulator
     * @author Raffi Enficiaud
     */
    template <class T, class result_type_t = T>
    struct s_meas_median: public std::unary_function<T, void>
    {
      typedef bacc::accumulator_set<T, bacc::stats<bacc::tag::median(bacc::with_p_square_quantile) > > acc_t;
      acc_t acc;

      typedef result_type_t result_type;
      s_meas_median() {}
      void operator()(const T& v) throw()
      {
        acc(v);
      }

      result_type const result() const
      {
        return static_cast<result_type>(bacc::median(acc));
      }

      void clear_result()
      {
        acc = acc_t();
      }
    };

    /*! @brief Computes the median value of the image
     *
     *  This function process the image through the functor s_meas_median
     *  @note This can be easily computed also from the histogram
     *  @todo implement the median over regions.
     *  @author Raffi Enficiaud
     */
    template <class image_in_t>
    yaRC image_meas_median_t(const image_in_t& im, variant& out)
    {
      typedef typename image_in_t::pixel_type out_t;
      typedef s_meas_median<out_t> operator_type;

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

    //! @} doxygroup: meas_quantile_details_grp
  }
}


#endif /* YAYI_MEASUREMENTS_QUANTILES_T_HPP__ */
