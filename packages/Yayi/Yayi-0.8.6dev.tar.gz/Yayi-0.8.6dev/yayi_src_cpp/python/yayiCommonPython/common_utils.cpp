
#include <yayiCommonPython/common_python.hpp>
#include <yayiCommon/include/current_configuration.hpp>


#include <boost/python/tuple.hpp>

bpy::tuple build_version() {
  
  tm date = yayi::current_build_date();
  return bpy::make_tuple(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour, date.tm_min, date.tm_sec);

}

void declare_utils()
{

  bpy::def("current_build_version", yayi::current_build_version, "Returns the current build version");
  bpy::def("current_build_date",    build_version, "Returns the date of build as a tuple in the following format: (year, month, day, hour, minutes, seconds)");
  

}

