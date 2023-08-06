#include <yayiCommonPython/common_python.hpp>
#include <yayiCommon/common_coordinates.hpp>
#include <yayiCommon/common_errors.hpp>
#include <yayiCommon/common_types.hpp>

struct custom_yaRC_to_python
{
  static PyObject* convert(yayi::yaRC const& s)
  {
    using namespace yayi;
    if(s.code != return_code_constants::e_Yr_ok)
      throw yayi::errors::yaException("Error: " + (std::string)s);
    else
      Py_RETURN_NONE;
  }
};


void declare_return() {
  boost::python::to_python_converter<yayi::yaRC, custom_yaRC_to_python>();
}

