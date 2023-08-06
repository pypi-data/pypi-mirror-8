#ifndef YAYI_COMMON_ORDERS_HPP__
#define YAYI_COMMON_ORDERS_HPP__

/*!@file
 * This file defines several helpers and structures for orders and lattice management
 * @author Raffi Enficiaud
 */

#include <functional>
#include <boost/numeric/conversion/bounds.hpp>

namespace yayi
{
  /*!@defgroup common_order_grp Ordering
   * @ingroup common_grp
   * @brief Manipulating and transforming order relations.
   *
   *
   * @{
   */
  //! Declaration of the traits for order
  template <class order_t>
  struct order_traits;


  //! Helper structure for getting bounds of a type, according to a certain order
  template <class T> struct s_bounds_helper {
    static T max() throw() {
      return boost::numeric::bounds<T>::highest();
    }
    static T min() throw() {
      return boost::numeric::bounds<T>::lowest();
    }
  };
  template <class T> struct s_bounds_helper_reverse
  {
    static T min() throw() {
      return boost::numeric::bounds<T>::highest();
    }
    static T max() throw() {
      return boost::numeric::bounds<T>::lowest();
    }
  };



  /*!@brief This structure handles the bounds of a type "U".
   *
   * This structure handles the bounds according to the order and the type U is the type on which the bounds is required, order_t is an
   * order type, which can be expressed on an other type than U (see
   * specializations)
   */
  template <class U, class order_t = std::less<U> >
  struct s_bounds;
  template <class U, class T> struct s_bounds<U, std::less<T> > : public s_bounds_helper<U> {};
  template <class U, class T> struct s_bounds<U, std::greater<T> > : public s_bounds_helper_reverse<U> {};
  template <class U, class T> struct s_bounds<U, std::less_equal<T> > : public s_bounds_helper<U> {};
  template <class U, class T> struct s_bounds<U, std::greater_equal<T> > : public s_bounds_helper_reverse<U> {};




  /*!@brief Functor on orders returning the reverse order ("<" becomes ">").
   * The concept is the following:
   * - the functor defines a type @c type which indicates the returned order type.
   * - the functor takes as parameter an instance of the type given as template parameter.
   * - the functor returns the instance of the reverse order corresponding the the instance given as parameter.
   * @note See the specializations of this structure, this one is the declaration only
   */
  template <class order_t>
  struct s_reverse_order_helper;

  //! Specializing of s_reverse_order_helper for std::less.
  template <class T> struct s_reverse_order_helper< std::less<T> > {
    typedef std::greater<T> type;
    static type reverse(const std::less<T>& ) throw()
    {
      return type();
    }
  };

  //! Specializing of s_reverse_order_helper for std::greater.
  template <class T> struct s_reverse_order_helper< std::greater<T> > {
    typedef std::less<T> type;
    static type reverse(const std::greater<T>& ) throw()
    {
      return type();
    }
  };

  //! Specializing of s_reverse_order_helper for std::less_equal.
  template <class T> struct s_reverse_order_helper< std::less_equal<T> > {
    typedef std::greater_equal<T> type;
    static type reverse(const std::less_equal<T>& ) throw()
    {
      return type();
    }
  };

  //! Specializing of s_reverse_order_helper for std::greater_equal.
  template <class T> struct s_reverse_order_helper< std::greater_equal<T> > {
    typedef std::less_equal<T> type;
    static type reverse(const std::greater_equal<T>& ) throw()
    {
      return type();
    }
  };


  /*!@brief Helper function that returns the corresponding reversed order instance of the one given in parameter.
   * Most of the returned orders are stateless
   * but can have a state, which will handled according to the
   * structure @c s_reverse_order_helper
   */
  template <class U>
  typename order_traits<U>::reverse reverse_order(U const& c)
  {
    return s_reverse_order_helper<U>::reverse(c);
  }








  /*!@brief Helper class for adding equality to an order ("<" becomes "<=")
   * See the specializations of this structure, this one is the declaration only
   */
  template <class order_t>
  struct s_add_equality_helper;

  template <class T> struct s_add_equality_helper< std::less<T> > {
    typedef std::less_equal<T> type;
    static type add_equality(const std::less<T>& ) throw() {
      return type();
    }
  };
  template <class T> struct s_add_equality_helper< std::less_equal<T> > {
    typedef std::less_equal<T> type;
    static type const& add_equality(type const& c) throw() {
      return c;
    }
  };
  template <class T> struct s_add_equality_helper< std::greater<T> > {
    typedef std::greater_equal<T> type;
    static type add_equality(const std::greater<T>& ) throw() {
      return type();
    }
  };
  template <class T> struct s_add_equality_helper< std::greater_equal<T> > {
    typedef std::greater_equal<T> type;
    static type const& add_equality(type const& c) throw() {
      return c;
    }
  };


/**
 * @brief Helper function that returns an order with equality.
 * Most of the returned equality are stateless but can have a state,
 * which will handled according to the structure @c s_add_equality_helper
*/
  template <class U>
  typename s_add_equality_helper<U>::type add_equality(U const& c)
  {
    return s_add_equality_helper<U>::add_equality(c);
  }



  //! Helper traits for manipulating orders
  template <class order_t>
  struct order_traits
  {
    typedef typename s_reverse_order_helper<order_t>::type  reverse;
    typedef typename s_add_equality_helper<order_t>::type   not_strict;

    template <class U> struct bounds : s_bounds<U, order_t> {};
  };


//! @} // common_order_grp

}

#endif /* YAYI_COMMON_ORDERS_HPP__ */
