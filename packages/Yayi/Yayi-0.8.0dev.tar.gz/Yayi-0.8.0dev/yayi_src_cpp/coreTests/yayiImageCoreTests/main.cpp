#define BOOST_TEST_MAIN
#define BOOST_TEST_MODULE yayi core

#include "main.hpp"
#include <boost/bind.hpp>
#include <yayiCommon/common_errors.hpp>

struct osstream_like : yayi::errors::error_stream_getter, boost::unit_test::test_observer
{
  std::stringstream stream;
  boost::unit_test::test_unit const *current_test;
  
  osstream_like() : current_test(0)
  {}
  
  std::ostream& get()
  {
    return stream;
  }
  
  std::string clean_name(std::string unit_name) const
  {
    std::string::size_type spaces = unit_name.find(" ");
    while(spaces != std::string::npos)
    {
      unit_name.replace(spaces, 1, "_");
      spaces = unit_name.find(" ", spaces);
    }
    return unit_name;
  }
  
  std::string get_parent_path(boost::unit_test::test_unit_id id) const
  {
    std::string ret;
    
    std::list<std::string> reverse_path_names;
    while(id)
    {
      boost::unit_test::test_unit &current_test = boost::unit_test::framework::get(id, boost::unit_test::tut_any);
      reverse_path_names.push_back(current_test.p_name.get());
      id = current_test.p_parent_id.get();
    }
    
    if(reverse_path_names.empty())
    {
      return ret; 
    }
    
    std::list<std::string>::const_reverse_iterator it(reverse_path_names.rbegin());
    ret = clean_name(*it);
    ++it;
    for(; it != reverse_path_names.rend(); ++it)
    {
      ret += "." + clean_name(*it);
    }
    return ret;

  }
  
  void test_unit_start(boost::unit_test::test_unit const& current)
  {
    current_test = &current;
    if(current.p_type == boost::unit_test::tut_case)
    {
      BOOST_MESSAGE("[TEST   ] Log output for [" << get_parent_path(current.p_id) << "]");
    }
  }
  
  void test_unit_finish(boost::unit_test::test_unit const& current, unsigned long /* elapsed */ )
  {
    std::string s(stream.str());
    if(!s.empty())
      BOOST_MESSAGE(s);
    stream.str("");
    stream.clear();
    BOOST_MESSAGE("[TESTEND] Log output for [" << get_parent_path(current.p_id) << "]");
  }
  
};

struct set_yayi_error_stream
{
  yayi::errors::error_stream_getter* previous_stream;
  osstream_like new_stream;
  set_yayi_error_stream()
  {
    previous_stream = yayi::errors::set_error_stream_getter(&new_stream);
    boost::unit_test::framework::register_observer(new_stream);
  }
    
  ~set_yayi_error_stream()
  {
    yayi::errors::set_error_stream_getter(previous_stream);
    boost::unit_test::framework::deregister_observer(new_stream);
  }
};

BOOST_GLOBAL_FIXTURE( set_yayi_error_stream );
