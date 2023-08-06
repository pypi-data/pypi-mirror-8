#ifndef YAYI_COMMON_HISTOGRAM__HPP___
#define YAYI_COMMON_HISTOGRAM__HPP___

/*! @file
 *  @brief Histogram generic definition and manipulation
 */


#include <map>
#include <functional>
#include <vector>
#include <algorithm>
#include <numeric>
#include <boost/numeric/conversion/bounds.hpp>
#include <boost/limits.hpp>

#include <yayiCommon/include/common_types_T.hpp>
#include <boost/lambda/lambda.hpp>
#include <boost/lambda/casts.hpp>
#include <boost/lambda/bind.hpp>
#include <boost/lambda/numeric.hpp>
#include <boost/lambda/algorithm.hpp>

namespace yayi
{
  /*!
   * @defgroup histogram_grp Histogram definitions
   * @ingroup common_grp
   * @{
   */


  /*!@brief Generic histogram structure
   *
   * @author Raffi Enficiaud
   */
  template <typename bin_t = yaF_double, typename count_t = yaUINT32>
  struct s_histogram_t : public std::map<bin_t, count_t>
  {

  public:
    typedef bin_t      bin_type;         //! Representation type of the bins
    typedef count_t    count_type;       //! Representation type of the counted elements
    typedef std::map<bin_t, count_t> representation_type;

    s_histogram_t() : representation_type() {}
    
    //! Returns the maximum non-zero bin
    bin_type max_bin() const throw(){
      if(this->empty())
        return boost::numeric::bounds<bin_t>::lowest();
      return this->rbegin()->first;
    }

    //! Returns the minimum non-zero bin
    bin_type min_bin() const throw(){
      if(this->empty())
        return boost::numeric::bounds<bin_t>::highest();
      return this->begin()->first;
    }

    /*template <class T>
    struct s_plus_second
    {
      T internal;
      s_plus_second(): internal(0){}
      template <class O>
      void operator()(const O& o)
      {
        internal+=o.second;
      }
    };*/
      
    //! Returns the sum of the bins
    typename type_description::s_sum_supertype<count_type>::type sum() const
    {
      typedef typename type_description::s_sum_supertype<count_type>::type type;
      typedef typename representation_type::value_type const aa;
      //typename aa::second_type aa::*p = &aa::second;
      //using boost::lambda::_1;

#if 0
      type ret(0);
      std::for_each(
        this->begin(), 
        this->end(), 
        
#if _MSC_VER >1500
        boost::lambda::var(ret) += (&boost::lambda::_1)->*(&std::pair< bin_t const, count_t >::second)); 
       //TR 19042011 BELOW NOT SUPPORTED 
       // error C2326: 'yayi::type_description::s_sum_supertype<U>::type yayi::s_histogram_t<bin_t,count_t>::sum(void) const' : function cannot access 'std::_Pair_base<_Ty1,_Ty2>::second'
       // boost::lambda::var(ret) += (&boost::lambda::_1)->*(&representation_type::value_type::second));

#else
        //boost::lambda::var(ret) += &boost::lambda::_1->*&representation_type::value_type::second); // does not compile on Visual 2010 SP1 (for instance)
        boost::lambda::var(ret) += &boost::lambda::_1->*&aa::second);
        //boost::lambda::var(ret) += (&_1)->*p);
#endif
      return ret;
      
      /*return std::for_each(
        this->begin(), 
        this->end(), 
        s_plus_second<type>()).internal;*/


      /*typedef std::plus<type> op_type;
      return std::accumulate(
        this->begin(), 
        this->end(), 
        type(0), 
        boost::lambda::bind(op_type(), boost::lambda::bind(&aa::second, boost::lambda::_1) ) );*/
#endif
      
      return std::accumulate(
        this->begin(), 
        this->end(), 
        0, 
        //type(0), 
        &boost::lambda::_2->*&aa::second + boost::lambda::_1);
        //boost::lambda::ll_static_cast<type>(&boost::lambda::_1->*&aa::second) );

        

    }
    
    //! Clears the content of the histogram
    void clear()
    {
      this->clear();
    }
    
    //! Normalizes the histogram in regards to its sum (returns a new histogram)
    s_histogram_t<bin_type, yaF_double> normalise() const
    {
      s_histogram_t<bin_type, yaF_double> out;
      typename type_description::s_sum_supertype<count_type>::type const sum_ = sum();
      
      for(typename representation_type::const_iterator it(this->begin()), ite(this->end());
          it != ite;
          ++it)
      {
        out[it->first] = it->second / sum_;
      }
      return out;
      
    }
  };


  /*!@brief Generic histogram structure (specialization for 8bits unsigned type)
   *
   * @author Raffi Enficiaud
   */
  template <typename count_t>
  struct s_histogram_t<yaUINT8, count_t> : public std::vector<count_t>
  {
  public:
    typedef yaUINT8    bin_type;         //! Representation type of the bins
    typedef count_t    count_type;       //! Representation type of the counted elements
    typedef std::vector<count_t> representation_type;

    s_histogram_t() : representation_type(std::numeric_limits<bin_type>::max()+1, count_t(0)) 
    {}
    
    //! Returns the maximum non-zero bin
    bin_type max_bin() const throw()
    {
      bin_type bin = std::numeric_limits<yaUINT8>::max();
      for(typename representation_type::const_reverse_iterator it(this->rbegin()), ite(this->rend()); 
          it != ite;
          ++it, --bin)
      {
        if(*it)
          return bin;
      }
      return std::numeric_limits<yaUINT8>::min();
    }
    
    //! Returns the minmum non-zero bin
    bin_type min_bin() const throw(){
      bin_type bin = std::numeric_limits<yaUINT8>::min();
      for(typename representation_type::const_iterator it(this->begin()), ite(this->end()); 
          it != ite;
          ++it, ++bin)
      {
        if(*it)
          return bin;
      }
      return std::numeric_limits<yaUINT8>::max();
    }

    //! Returns the total sum of the histogram
    typename type_description::s_sum_supertype<count_type>::type sum() const
    {
      typedef typename type_description::s_sum_supertype<count_type>::type type;
      typedef std::plus<type> op_type;
      return std::accumulate(
        this->begin(), 
        this->end(), 
        type(0), 
        op_type());
    }
    
    //! Clears the content of the histogram
    void clear()
    {
      for(typename representation_type::iterator it(this->begin()), ite(this->end()); it != ite; ++it)
      {
        *it = 0;
      }    
    }
    
    //! Normalizes the histogram with its sum (returns a new histogram with yaF_double type count)
    s_histogram_t<bin_type, yaF_double> normalise() const
    {
      s_histogram_t<bin_type, yaF_double> out;
      typename type_description::s_sum_supertype<count_type>::type const sum_ = sum();
      
      for(typename representation_type::const_iterator it(this->begin()), ite(this->end());
          it != ite;
          ++it)
      {
        out[it->first] = it->second / sum_;
      }
      return out;
      
    }
  };
	//! @} // defgroup 
} // namespace yayi

#endif /* YAYI_COMMON_HISTOGRAM__HPP___ */
