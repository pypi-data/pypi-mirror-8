#ifndef YAYI_COMMON_TIME_HPP__
#define YAYI_COMMON_TIME_HPP__

/*!@file
 * This file contains functions relative to time measurements (mainly for benchmarking purposes)
 *
 * @author Raffi Enficiaud
 */

#include <yayiCommon/common_types.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <deque>
#include <boost/accumulators/accumulators.hpp>
#include <boost/accumulators/statistics/mean.hpp>
#include <boost/accumulators/statistics/min.hpp>
#include <boost/accumulators/statistics/max.hpp>
#include <boost/accumulators/statistics/stats.hpp>
#include <boost/accumulators/statistics/variance.hpp>
#include <utility>
#include <boost/lambda/lambda.hpp>

namespace yayi
{
  /*!@ingroup common_utilities_grp
   * @{
   */
  namespace time
  {
  
    /*!@brief Utility class for time elapse measurements
     * This class merely wraps some known functions in boost::posix_time
     * @author Raffi Enficiaud
     */
    struct s_time_elapsed
    {
      typedef s_time_elapsed this_type;
      typedef boost::posix_time::ptime time_storage_t;
      time_storage_t time;
      typedef std::vector<time_storage_t> acc_t;
      acc_t acc_;
      typedef std::deque<boost::posix_time::time_duration> duration_t;

      //! Initializes the start point to now
      s_time_elapsed() : time(boost::posix_time::microsec_clock::local_time()) {}
      
      //! Copy-construction
      s_time_elapsed(const s_time_elapsed& r_) : time(r_.time) {}
      
      void reset()
      {
        acc_.clear();
        time = boost::posix_time::microsec_clock::local_time();
      }
      
      //! Returns the time duration in microseconds between now and the start point (time of construction).
      double total_microseconds() const 
      {
        return static_cast<double>((boost::posix_time::microsec_clock::local_time() - time).total_microseconds());
      }

      //! Returns the time duration in microseconds between the argument and the start point (time of construction).
      double total_microseconds(this_type const &r) const 
      {
        return static_cast<double>((r.time - time).total_microseconds());
      }

      //! Returns the time duration in milliseconds between now and the start point (time of construction).
      double total_milliseconds() const 
      {
        return static_cast<double>((boost::posix_time::microsec_clock::local_time() - time).total_milliseconds());
      }

      //! Returns the time duration in milliseconds between the argument and the start point (time of construction).
      double total_milliseconds(this_type const &r) const 
      {
        return static_cast<double>((r.time - time).total_milliseconds());
      }
      
      //! Stacks a time of observation.
      void stack_observation()
      {
        acc_.push_back(boost::posix_time::microsec_clock::local_time());
      }
      
      //! Returns the number of observations seen so far.
      int number_of_observations() const
      {
        return acc_.size();
      }
      
      //! Transforms the previously accumulated elements into duration elements.
      duration_t transform_to_duration() const
      {
        duration_t out;
        if(acc_.size() == 0)
          return out;
        
        for(acc_t::const_reverse_iterator it(acc_.rbegin()), ite(acc_.rend()-1); it < ite; ++it)
        {
          out.push_front(*it - *(it + 1));
        }
        out.push_front(acc_.front() - time);
        return out;
      }
      
      

      //! Returns the min and max durations of the stacked observations, in microseconds.
      std::pair<double, double> min_max() const
      {
        using namespace boost::accumulators;
        using namespace boost::lambda;
        const duration_t & durations = transform_to_duration();
        std::vector<int> microseconds;
        std::transform(durations.begin(), durations.end(), std::back_inserter(microseconds), bind(&duration_t::value_type::total_microseconds, _1));
        accumulator_set< int, features< tag::min, tag::max > > acc; // duration is less-than comparable
        
        acc = std::for_each(microseconds.begin(), microseconds.end(), acc);
        return std::make_pair(min(acc), max(acc));
      }

      //! Returns the min and max durations of the stacked observations, in microseconds.
      std::pair<double, double> mean_variance() const
      {
        using namespace boost::accumulators;
        using namespace boost::lambda;
        const duration_t & durations = transform_to_duration();
        std::vector<double> microseconds;
        std::transform(durations.begin(), durations.end(), std::back_inserter(microseconds), bind(&duration_t::value_type::total_microseconds, _1));
        accumulator_set<double, features< tag::mean, tag::variance > > acc; // duration is less-than comparable, but mean does not work
        
        acc = std::for_each(microseconds.begin(), microseconds.end(), acc);
        return std::make_pair(boost::accumulators::mean(acc), variance(acc));
      }

    };
    
    
  
    //! Returns the string representation of the current date and time.
    string_type current_date_and_time_as_string()
    {
      return boost::posix_time::to_simple_string(boost::posix_time::microsec_clock::local_time());
    }  
  }
  	//! @} // common_utilities_grp
}

#endif /* YAYI_COMMON_TIME_HPP__ */
