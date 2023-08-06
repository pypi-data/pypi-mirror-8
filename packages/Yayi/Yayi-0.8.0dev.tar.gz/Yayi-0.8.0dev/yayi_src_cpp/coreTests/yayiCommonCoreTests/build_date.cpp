#include "main.hpp"
#include <yayiCommon/include/current_configuration.hpp>
#include <yayiCommon/include/common_string_utilities.hpp>

#include <ctime>

BOOST_AUTO_TEST_CASE(build_date)
{
  using namespace yayi;
  struct tm null_tm = { 0, 0, 00, 01, 01, 2000 };
  std::string current_configuration = yayi::current_build_version();
  BOOST_CHECK_MESSAGE(!current_configuration.empty(), "Current build version cannot be 0");
  struct tm current_build_date = yayi::current_build_date();
  BOOST_CHECK_MESSAGE(
        current_build_date.tm_year  != null_tm.tm_year
    ||  current_build_date.tm_mon   != null_tm.tm_mon
    ||  current_build_date.tm_mday  != null_tm.tm_mday
    ||  current_build_date.tm_hour  != null_tm.tm_hour
    ||  current_build_date.tm_min   != null_tm.tm_min
    ||  current_build_date.tm_sec   != null_tm.tm_sec ,
    "Current build date cannot be 2000/01/01 00:00:00");


  std::cout << "Version info: " << std::endl;
  std::cout << "\tcurrent version : " << current_configuration << std::endl;
  std::cout << "\tLast commit date: " 
    << int_to_string(current_build_date.tm_year, 4) << "/" << int_to_string(current_build_date.tm_mon, 2) << "/" << int_to_string(current_build_date.tm_mday, 2) << " "
    << int_to_string(current_build_date.tm_hour, 2) << ":" << int_to_string(current_build_date.tm_min, 2) << ":" << int_to_string(current_build_date.tm_sec, 2) << std::endl;
}

