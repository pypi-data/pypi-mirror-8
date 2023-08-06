
#include "main.hpp"
#include <yayiImageCore/include/yayiImageOperatorClassification_t.hpp>


struct s_operator_parenthesis_is_not_const {
  int count;
  
  template <class T> struct result;
  
  template <class op, class T> struct result<op(T)> {
    typedef void type;
  };
  template <class op, class T> struct result<op(const T&)> {
    typedef T type;
  };
  
  
  template <class T>
  void operator()(T& x) throw() {
    x *= 2;
    count ++;
  }

  template <class T1, class T2>
  T2 operator()(const T1& x) throw() {
    count ++;
    return x * 2;
  }

};


struct s_operator_parenthesis_is_const {
  typedef yayi::ns_operator_tag::operator_commutative operator_tag;
  typedef void result_type;
  template <class T>
  void operator()(T& x) const throw() {
    x *= 3;
  }
};


// checks the tags are properly extracted

BOOST_MPL_ASSERT_NOT(( yayi::ns_operator_tag::has_operator_tag<s_operator_parenthesis_is_not_const> ));
BOOST_MPL_ASSERT(( yayi::ns_operator_tag::has_operator_tag<s_operator_parenthesis_is_const> ));

//BOOST_STATIC_ASSERT((!boost::is_stateless<s_operator_parenthesis_is_not_const>::value));
//BOOST_MPL_ASSERT_NOT((boost::is_stateless<s_operator_parenthesis_is_not_const>));
BOOST_MPL_ASSERT_NOT((boost::is_empty<s_operator_parenthesis_is_not_const>));
//BOOST_STATIC_ASSERT((!boost::function_types::is_member_function_pointer<s_operator_parenthesis_is_not_const(int&), boost::function_types::const_qualified>::value));
//BOOST_STATIC_ASSERT((!boost::function_types::is_member_function_pointer<s_operator_parenthesis_is_not_const(int const&), boost::function_types::const_qualified>::value));


// Raffi: just to check
//BOOST_STATIC_ASSERT((boost::is_stateless<s_operator_parenthesis_is_not_const>::value));
//BOOST_STATIC_ASSERT((boost::function_types::is_member_function_pointer<s_operator_parenthesis_is_not_const(int&), boost::function_types::const_qualified>::value));
//BOOST_STATIC_ASSERT((boost::function_types::is_member_function_pointer<s_operator_parenthesis_is_not_const(int const&), boost::function_types::const_qualified>::value));
//BOOST_STATIC_ASSERT(false);


BOOST_MPL_ASSERT((boost::is_empty<s_operator_parenthesis_is_const>));

//BOOST_MPL_ASSERT((boost::has_trivial_constructor<s_operator_parenthesis_is_const>));
//BOOST_MPL_ASSERT((boost::has_trivial_copy<s_operator_parenthesis_is_const>));
//BOOST_MPL_ASSERT((boost::has_trivial_destructor<s_operator_parenthesis_is_const>));
BOOST_MPL_ASSERT((boost::is_class<s_operator_parenthesis_is_const>));
BOOST_MPL_ASSERT((boost::is_empty<s_operator_parenthesis_is_const>));

// Raffi: does not work properly under macosx
//BOOST_MPL_ASSERT((boost::is_stateless<s_operator_parenthesis_is_const>));
//BOOST_MPL_ASSERT_NOT((boost::is_stateless<s_operator_parenthesis_is_const>));



BOOST_MPL_ASSERT((yayi::s_operator_is_functor_call_const<boost::mpl::vector<s_operator_parenthesis_is_const, int&> >));
BOOST_MPL_ASSERT_NOT((yayi::s_operator_is_functor_call_const<boost::mpl::vector<s_operator_parenthesis_is_not_const, int&> >));

BOOST_AUTO_TEST_SUITE(operator_classification)

BOOST_AUTO_TEST_CASE(operator_parenthesis_constness_check)
{
  using namespace yayi;
  BOOST_CHECK((boost::function_types::is_callable_builtin<s_operator_parenthesis_is_const(int&)>::value));

  BOOST_CHECK((s_operator_is_functor_call_const<boost::mpl::vector<s_operator_parenthesis_is_const, int&> >::value));
  BOOST_CHECK(!(s_operator_is_functor_call_const<boost::mpl::vector<s_operator_parenthesis_is_not_const, int&> >::value));
}

BOOST_AUTO_TEST_SUITE_END()

