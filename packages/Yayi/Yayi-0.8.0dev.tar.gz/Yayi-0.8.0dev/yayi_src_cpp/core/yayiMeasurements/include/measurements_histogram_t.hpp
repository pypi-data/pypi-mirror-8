#ifndef YAYI_MEASUREMENTS_HISTOGRAM_T_HPP__
#define YAYI_MEASUREMENTS_HISTOGRAM_T_HPP__

#include <boost/call_traits.hpp>
#include <functional>
#include <boost/numeric/conversion/bounds.hpp>
#include <yayiCommon/common_histogram.hpp>
#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_binary_t.hpp>
#include <yayiMeasurements/include/measurements_t.hpp>
#include <yayiCommon/common_variant.hpp>

namespace yayi
{
  namespace measurements
  {
    /*!@defgroup meas_histo_details_grp Histogram measurements implementation details.
     * @ingroup meas_details_grp
     *
     * @{
     */

    /*!@brief Histogram functor on a sequence/set of pixels.
     *
     * The histogram is computed through the sequence of calls of @c operator().
     * The sequence can obviously be in any order, the histogram being equivalent up to a permutation
     * of the input points.
     *
     * @see s_histogram_t
     * @concept{measurement_functor_concepts} 
     */
    template <class T>
    struct s_meas_histogram: public std::unary_function<T, void>
    {
      typedef s_histogram_t<T> result_type;
      result_type h;
      s_meas_histogram() : h() {}

      //! Update of the histogram with a new value `v`.
      void operator()(const T& v) throw()
      {
        h[v]++;
      }

      //! Returns the resulting histogram.
      result_type const& result() const
      {
        return h;
      }

      //! Clears the internal state.
      void clear_result() throw()
      {
        h.clear();
      }
    };



    /*!@brief Computes the histogram of an image
     *
     */
    template <class image_in_t>
    yaRC image_meas_histogram_t(const image_in_t& im, s_histogram_t<typename image_in_t::pixel_type>& out)
    {
      typedef typename image_in_t::pixel_type out_t;
      typedef s_meas_histogram<out_t> operator_type;

      s_apply_unary_operator op_processor;

      operator_type op;
      yaRC res = op_processor(im, op);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured during the computation of the histogram: " << res);
        return res;
      }

      out = op.result();
      return yaRC_ok;
    }


    /*!@brief Computes the histogram on each region of an image
     * 
     * The histogram is computed by taking the values of image @c im. 
     * The regions are given by an auxiliary image @c regions. These regions cannot overlap.
     * The output is an associative map that associates each id of the regions (eg. their grey level value)
     * to an histogram.
     */
    template <class image_in_t, class image_regions_t>
    yaRC image_meas_histogram_on_region_t(
      const image_in_t& im,
      const image_regions_t& regions,
      std::map<typename image_regions_t::pixel_type, s_histogram_t<typename image_in_t::pixel_type> > & out)
    {
      typedef s_meas_histogram<typename image_in_t::pixel_type> region_operator_type;
      typedef s_measurement_on_regions<
        typename image_in_t::pixel_type,
        typename image_regions_t::pixel_type,
        region_operator_type> operator_type;

      s_apply_binary_operator op_processor;

      operator_type op;
      yaRC res = op_processor(im, regions, op);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured during the computation of the histogram: " << res);
        return res;
      }

      out = op.result();
      return yaRC_ok;
    }
    
    //! @}

  }
}


#endif /* YAYI_MEASUREMENTS_HISTOGRAM_T_HPP__ */
