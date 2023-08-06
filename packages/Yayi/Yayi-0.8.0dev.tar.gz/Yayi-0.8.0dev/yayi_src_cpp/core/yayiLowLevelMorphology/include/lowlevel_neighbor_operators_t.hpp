#ifndef YAYI_LOWLEVEL_MORPHOLOGY_NEIGHBOR_OPERATORS_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_NEIGHBOR_OPERATORS_HPP__

/*!@file
 * This file defines some neighbor operators
 */
 
#include <boost/circular_buffer.hpp>
#include <boost/call_traits.hpp>
#include <boost/algorithm/minmax_element.hpp>
#include <boost/tuple/tuple.hpp>
#include <algorithm>
#include <yayiLowLevelMorphology/include/neighbor_operators_traits_t.hpp>
#include <yayiCommon/common_orders.hpp>


namespace yayi { namespace llmm {

/*!
 * @addtogroup llm_details_grp
 *
 *@{
 */      


  /*!@brief Min element over a range
   * The functor returns a reference to the min element over the provided range
   * @author Raffi Enficiaud
   */
  template <class in_t, class order_t = std::less<in_t> >
  struct s_min_element_subset {
  
    typedef neighborhood_operator_traits::shiftable_operator operator_traits;
    
    order_t order;
    s_min_element_subset() : order() {}
    s_min_element_subset(order_t const& o) : order(o) {}
  
    template <class it>
    typename it::const_reference operator()(it beg, const it e) const {
      //DEBUG_ASSERT(beg != e, "Empty neighborhood");
      return beg != e ? *std::min_element(beg, e, order) : s_bounds<in_t, order_t>::max();
    }
    
    #if 0
    // for future use
    template <class it>
    struct s_shifter {
      typedef it iterator_t;
      typedef typename iterator_t::value_type value_type;
      
      //std::vector<value_type> vect_values;
      boost::circular_buffer<value_type> values;

      
      template <class neigh_t>
      s_shifter(const neigh_t& n) : values(n.get_shift()) {
      
      }
      
      // Initialize the internals
      void init() {
        values.clear();
      }
      
      // 
      const in_t& step(it beg, const it e) {
        values.push_back(*std::min_element(beg, e));
        return *std::min_element(values.begin(), values.end());
      }
      
    
    };
    #endif
  
  };
  
  //! Specializing of s_min_element_subset for natural order '<' on in_t type
  template <class in_t> struct s_min_element_subset<in_t, std::less<in_t> > {
    typedef neighborhood_operator_traits::shiftable_operator operator_traits;
    template <class it> typename it::value_type operator()(it beg, const it e) const {
      return beg != e ? *std::min_element(beg, e) : s_bounds<in_t, std::less<in_t> >::max();
    }
  };

  //! Specializing of s_min_element_subset for natural order '>' on in_t type
  template <class in_t> struct s_min_element_subset<in_t, std::greater<in_t> > {
    typedef neighborhood_operator_traits::shiftable_operator operator_traits;
    template <class it> typename it::value_type operator()(it beg, const it e) const {
      return beg != e ? *std::max_element(beg, e) : s_bounds<in_t, std::greater<in_t> >::max();
    }
  };
  
  
  /*!@brief Propagate the minimum information of the center to the neighbors
   */
  template <class in_t, class order_t = std::less<in_t> >
  struct s_min_element_to_subset {
  
    order_t order;
    s_min_element_to_subset() : order() {}
    s_min_element_to_subset(order_t const &o) : order(o) {}
  
    template <class it>
    void operator()(it beg, const it e, typename it::reference v_center) const {
      //DEBUG_ASSERT(beg != e, "Empty neighborhood"); // non relevant here
      for(; beg != e; ++beg)
        *beg = std::min(*beg, v_center, order);
      return;
    }
  };
  
  //! Specializing of s_min_element_to_subset for natural order < on in_t type
  template <class in_t> struct s_min_element_to_subset<in_t, std::less<in_t> >  {
    template <class it> void operator()(it beg, const it e, typename it::reference v_center) const {
      //DEBUG_ASSERT(beg != e, "Empty neighborhood");
      for(; beg != e; ++beg)
        *beg = std::min(*beg, v_center);
      return;
    }
  };  

  //! Specializing of s_min_element_to_subset for natural order > on in_t type
  template <class in_t> struct s_min_element_to_subset<in_t, std::greater<in_t> >  {
    template <class it> void operator()(it beg, const it e, typename it::reference v_center) const {
      //DEBUG_ASSERT(beg != e, "Empty neighborhood");
      for(; beg != e; ++beg)
        *beg = std::max(*beg, v_center);
      return;
    }
  };  


  /*!@brief Max element over a range
   * The functor returns a reference to the max element over the provided range
   * @author Raffi Enficiaud
   */
  template <class in_t, class order_t = std::less<in_t> >
  struct s_max_element_subset {
  
    typedef neighborhood_operator_traits::shiftable_operator operator_traits;

    order_t order;
    s_max_element_subset() : order() {}
    s_max_element_subset(order_t const &o) : order(o) {}
  
    template <class it>
    typename it::const_reference operator()(it beg, const it e) const YAYI_THROW_DEBUG_ONLY__ {
      //DEBUG_ASSERT(beg != e, "Empty neighborhood");
      return beg != e ? *std::max_element(beg, e, order) : s_bounds<in_t, std::less<in_t> >::min();
    }
      
  };
  
  //! Specializing of s_max_element_subset for natural order '<' on in_t type
  template <class in_t> struct s_max_element_subset<in_t, std::less<in_t> > {
    typedef neighborhood_operator_traits::shiftable_operator operator_traits;
    template <class it> typename it::value_type operator()(it beg, const it e) const YAYI_THROW_DEBUG_ONLY__ {
      return beg != e ? *std::max_element(beg, e) : s_bounds<in_t, std::less<in_t> >::min();
    }
  };

  //! Specializing of s_max_element_subset for natural order '>' on in_t type
  template <class in_t> struct s_max_element_subset<in_t, std::greater<in_t> > {
    typedef neighborhood_operator_traits::shiftable_operator operator_traits;
    template <class it> typename it::value_type operator()(it beg, const it e) const YAYI_THROW_DEBUG_ONLY__ {
      return beg != e ? *std::min_element(beg, e) : s_bounds<in_t, std::greater<in_t> >::min();
    }
  };  
  
  
  /*!@brief Propagate the minimum information of the center to the neighbors
   */
  template <class in_t, class order_t = std::less<in_t> >
  struct s_max_element_to_subset {
  
    order_t order;
    s_max_element_to_subset() : order() {}
    s_max_element_to_subset(order_t const &o) : order(o) {}
  
    template <class it>
    void operator()(it beg, const it e, typename it::reference v_center) const YAYI_THROW_DEBUG_ONLY__ {
      //DEBUG_ASSERT(beg != e, "Empty neighborhood"); this is not a problem for this case
      for(; beg != e; ++beg)
        *beg = std::max(*beg, v_center, order);
      return;
    }
  };

  //! Specializing of s_max_element_to_subset for < order on in_t type (lighter structure)
  template <class in_t> struct s_max_element_to_subset<in_t, std::less<in_t> > {
    template <class it> void operator()(it beg, const it e, typename it::reference v_center) const YAYI_THROW_DEBUG_ONLY__ {
      //DEBUG_ASSERT(beg != e, "Empty neighborhood");
      for(; beg != e; ++beg)
        *beg = std::max(*beg, v_center);
      return;
    }
  };

  //! Specializing of s_max_element_to_subset for > order on in_t type
  template <class in_t> struct s_max_element_to_subset<in_t, std::greater<in_t> > {
    template <class it> void operator()(it beg, const it e, typename it::reference v_center) const YAYI_THROW_DEBUG_ONLY__ {
      //DEBUG_ASSERT(beg != e, "Empty neighborhood");
      for(; beg != e; ++beg)
        *beg = std::min(*beg, v_center);
      return;
    }
  };

  /*!@brief Max minus min value over a range
   * The functor returns the value of the maximum minus minimum over the provided range
   * @author Raffi Enficiaud
   */
  template <class in_t>
  struct s_max_minus_min_element_subset {
  
    typedef neighborhood_operator_traits::shiftable_operator operator_traits;
  
    template <class it>
    typename it::value_type operator()(it const &beg, it const &e) const YAYI_THROW_DEBUG_ONLY__ {
      DEBUG_ASSERT(beg != e, "Empty neighborhood");
      std::pair<it, it> min_max_it = boost::minmax_element(beg, e);
      /*typename it::value_type max_e = *beg, min_e = *beg;
      for(++beg; beg != e; ++beg)
      {
        typename it::value_type val = *beg;
        max_e = std::max(val, max_e);
        min_e = std::min(val, min_e);
      }*/
      return *min_max_it.second - *min_max_it.first;
    }
      
  };

  /*!@brief Max minus min value over a range
   * The functor returns the value of the maximum minus minimum over the provided range
   * @author Raffi Enficiaud
   */
  template <class in_t>
  struct s_max_minus_center_element_subset {
  
    typedef neighborhood_operator_traits::shiftable_operator operator_traits;
  
    template <class it>
    typename it::value_type operator()(it beg, const it e, typename boost::call_traits<typename it::value_type>::param_type center_value) const YAYI_THROW_DEBUG_ONLY__ {
      static const s_max_element_subset<in_t> elem = s_max_element_subset<in_t>();
      return elem(beg,e) - center_value;
    }
      
  };


  /*!@brief Max minus min value over a range
   * The functor returns the value of the maximum minus minimum over the provided range
   * @author Raffi Enficiaud
   */
  template <class in_t>
  struct s_center_minus_min_element_subset {
  
    typedef neighborhood_operator_traits::shiftable_operator operator_traits;
  
    template <class it>
    typename it::value_type operator()(it beg, const it e, typename boost::call_traits<typename it::value_type>::param_type center_value) const YAYI_THROW_DEBUG_ONLY__ {
      static const s_min_element_subset<in_t> elem = s_min_element_subset<in_t>();
      return center_value - elem(beg,e);
    }
      
  };
//! @} doxygroup: llm_details_grp
}}



#endif /* YAYI_LOWLEVEL_MORPHOLOGY_NEIGHBOR_OPERATORS_HPP__ */
