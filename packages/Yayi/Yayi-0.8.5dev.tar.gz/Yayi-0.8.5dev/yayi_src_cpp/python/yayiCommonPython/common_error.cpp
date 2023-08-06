

#include <yayiCommonPython/common_python.hpp>
#include <yayiCommon/common_types.hpp>
#include <yayiCommon/common_errors.hpp>

using namespace yayi;
using namespace yayi::errors;

void yayi_except_translator(yaException const& x) {
  PyErr_SetString(PyExc_RuntimeError, ("Exception caught : " + x.message()).c_str());
  boost::python::throw_error_already_set();
}


void declare_errors() {
  bpy::register_exception_translator<yaException>(yayi_except_translator);
}

