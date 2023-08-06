#ifndef COMMON_TESTS_DATA_PATH_HPP__
#define COMMON_TESTS_DATA_PATH_HPP__

#include <string>
#include <boost/version.hpp>
#include <boost/filesystem.hpp>

inline std::string get_data_from_data_path(const std::string &filename)
{
  using namespace boost::filesystem;
  path current = path(__FILE__).parent_path();
  path data = current / ".." / "yayiTestData" / filename;
#if ( (((BOOST_VERSION  / 100) % 1000) >= 46) && ((BOOST_VERSION /  100000) >= 1) )
  return data.string();
#else
  return data.file_string();
#endif
}

#if 0
std::string get_data_path() {

  using boost::filesystem;
  
  path current = path(__FILE__).remove_filename();
  path data = current / ".." / "yayiTestData";
  return data.external_directory_string();
}
#endif

#endif
