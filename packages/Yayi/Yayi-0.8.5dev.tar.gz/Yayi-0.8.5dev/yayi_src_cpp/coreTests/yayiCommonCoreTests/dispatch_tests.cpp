#define BOOST_MPL_LIMIT_METAFUNCTION_ARITY 7
#define BOOST_MPL_CFG_NO_PREPROCESSED_HEADERS


#if defined(_WIN32) || defined(_WIN64)
#pragma warning(disable:4512)
#endif


#include "main.hpp"
#include <yayiCommon/include/current_configuration.hpp>
#include <yayiCommon/include/common_dispatch.hpp>
#include <yayiCommon/include/common_string_utilities.hpp>
#include <yayiCommon/include/common_variantDispatch.hpp>

#include <ctime>


// for testing
#include <boost/bind.hpp>

// tuples
#include "boost/tuple/tuple.hpp"

#include <iostream>
using namespace boost;


template <class I> bool function1(const I& v1, const I&v2)
{
  return v1 && v2;
}


struct my_dummy_struct
{
  my_dummy_struct() {
    counter++;
  }


public:
  my_dummy_struct(const my_dummy_struct&) {
    counter++;
  }
  
  my_dummy_struct(bool b, int i) : b_field1(b), i_field2(i) {}

  bool  b_field1;
  int   i_field2;
  static int counter;
};

int my_dummy_struct::counter = 0;



// declaration of personal dispatch mechanism
namespace yayi { namespace dispatcher {
  template <class T> struct s_conversion_policy<my_dummy_struct&, T>
  {
    typedef s_convertible_runtime_time type;
  };
  template <class T> struct s_runtime_conversion<my_dummy_struct&, T>
  {
    typedef boost::true_type type;
    typedef typename remove_const<typename remove_reference<T>::type>::type T_without_const_ref;
    typedef typename add_reference<typename add_const<T_without_const_ref>::type>::type T_const_ref;

    BOOST_MPL_ASSERT((boost::is_fundamental<typename boost::remove_reference<T>::type>));

    typedef mpl::true_  internal_reference;

    static bool is_convertible(const my_dummy_struct& r_) throw()
    {
      //std::cout << "Adress of my_dummy_struct " << (void*)&r_ << std::endl;
      try
      {
        if(r_.i_field2 < 0)
          return false;
      }
      catch(yayi::errors::yaException&)
      {
        return false;
      }
      return true;
    }
    
    static T_const_ref convert(const my_dummy_struct& r_)
    {
      return r_.b_field1;
    }
    static T_without_const_ref convert(my_dummy_struct& r_)
    {
      return r_.b_field1;
    }
  };

}}


BOOST_AUTO_TEST_SUITE(dispatch)


namespace 
{

  static bool function_3(bool b1, bool b2, bool b3)
  {
    return b1 && b2 && !b3;
  }


  static bool function_5(bool b1, bool b2, bool b3)
  {
    return b1 && b2 && !b3;
  }
  static bool function_6(bool b1, bool b2, bool b3)
  {
    return b1 && b2 && !b3;
  }

  static bool function_7(bool b1, bool b2, bool &b3)
  {
    bool b_ret = b1 && b2 && !b3;
    b3 = !b3;
    return b_ret;
  }
  
  struct s_for_dispatch
  {
    bool internal_ok;
    
    s_for_dispatch() : internal_ok(false) {}
    bool function_4(bool b1, bool b2, bool b3)
    {
      internal_ok = b1 && b2 && !b3;
      return internal_ok;
    }
  
  };
}




BOOST_AUTO_TEST_CASE(dispatch_custom_structure)
{
  using namespace yayi;
  using namespace yayi::dispatcher;

  my_dummy_struct s1(true, -1), s2(true, 1), s3(false, 1);


  bool b_ret;

  // pour des tests

  typedef bool function_type(bool, bool, bool);
  typedef boost::function_types::result_type<function_type>::type  toto_type;

  BOOST_MPL_ASSERT((mpl::not_<boost::is_void<toto_type> >));
  BOOST_MPL_ASSERT((boost::is_same<toto_type, bool> ));

  
  //std::cout << "Adress of s2 = " << (void*)&s2 << std::endl;

  typedef yayi::dispatcher::s_dispatcher<bool&, const my_dummy_struct&, const my_dummy_struct&, const my_dummy_struct&> dispatcher_type_new1;
  int count = my_dummy_struct::counter;
  dispatcher_type_new1 dispatcher_new(b_ret, s2, s2, s2);

  // no modification of return in case no conversion occurs
  b_ret = true;
  BOOST_CHECK(dispatcher_new(function_3) == yayi::yaRC_ok);
  BOOST_CHECK(!b_ret);
  BOOST_CHECK_MESSAGE(my_dummy_struct::counter == count, "The class has been constructed during the dispatch : this is an error since only reference should be passed");

  b_ret = false;
  dispatcher_type_new1 dispatcher_new2(b_ret, s2, s2, s3);
  BOOST_CHECK(dispatcher_new2(function_3) == yayi::yaRC_ok);
  BOOST_CHECK(b_ret);
  BOOST_CHECK_MESSAGE(my_dummy_struct::counter == count, "The class has been constructed during the dispatch : this is an error since only reference should be passed");

  b_ret = false;
  s_for_dispatch internal_instance;
  internal_instance.internal_ok = false;
  BOOST_CHECK(dispatcher_new2(&s_for_dispatch::function_4, internal_instance) == yayi::yaRC_ok);
  BOOST_CHECK(b_ret);
  BOOST_CHECK(internal_instance.internal_ok);
  BOOST_CHECK_MESSAGE(my_dummy_struct::counter == count, "The class has been constructed during the dispatch : this is an error since only reference should be passed");

}


BOOST_AUTO_TEST_CASE(dispatch_on_several_functions)
{
  // TODO : to be completed
  using namespace yayi;
  using namespace yayi::dispatcher;
  my_dummy_struct s1(true, -1), s2(true, 1), s3(false, 1);

  bool b_ret;

  typedef yayi::dispatcher::s_dispatcher<bool, const my_dummy_struct&, const my_dummy_struct&, const my_dummy_struct&> dispatcher_type_new1;
  dispatcher_type_new1 dispatcher_new(b_ret, s2, s2, s2);

  int count = my_dummy_struct::counter;

  // no modification of return in case no conversion occurs
  b_ret = true;
  BOOST_CHECK(dispatcher_new.calls_first_suitable(
    boost::fusion::make_vector(
      &function_3, &function_5, &function_6
    )) == yayi::yaRC_ok);
    
  BOOST_CHECK(!b_ret);
  BOOST_CHECK_MESSAGE(my_dummy_struct::counter == count, "The class has been constructed during the dispatch : this is an error since only reference should be passed");


}
  
BOOST_AUTO_TEST_CASE(dispatch_with_variant)
{
  using namespace yayi;
  using namespace yayi::dispatcher;

  // test for holder need
  BOOST_STATIC_ASSERT((need_temporary_holder_tag< s_runtime_conversion<yayi::variant&, double> >::value));
  BOOST_STATIC_ASSERT((!need_temporary_holder_tag< s_compile_time_conversion<double, double> >::value));  

  variant v1(true), v2(false), v3(false), vret;

  typedef yayi::dispatcher::s_dispatcher<variant&, const variant&, variant&, variant&> dispatcher_type_variants;
  dispatcher_type_variants dispatcher_new(vret, v1, v2, v3);


  BOOST_CHECK(dispatcher_new(function_3) == yayi::yaRC_ok);
  BOOST_CHECK(!static_cast<bool>(vret));
  
  v2 = true;
  BOOST_CHECK(dispatcher_new(function_3) == yayi::yaRC_ok);
  BOOST_CHECK(static_cast<bool>(vret));
  
  BOOST_CHECK(dispatcher_new(function_7) == yayi::yaRC_ok);
  BOOST_CHECK(static_cast<bool>(v3));
  BOOST_CHECK(static_cast<bool>(vret));

  BOOST_CHECK(dispatcher_new(function_7) == yayi::yaRC_ok);
  BOOST_CHECK(!static_cast<bool>(v3));
  BOOST_CHECK(!static_cast<bool>(vret));  


  BOOST_STATIC_ASSERT((need_temporary_holder_tag< s_runtime_conversion<variant &, double> >::type::value));

}

BOOST_AUTO_TEST_SUITE_END()



