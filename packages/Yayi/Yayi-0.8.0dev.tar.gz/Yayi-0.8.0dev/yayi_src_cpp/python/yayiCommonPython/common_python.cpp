

#include <yayiCommonPython/common_python.hpp>

#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;



#if !defined(_MSC_VER) && !defined(__MINGW32__)
#include <dlfcn.h>
#endif


void declare_variants();
void declare_enums();
void declare_utils();
void declare_errors();
void declare_object();
void declare_coordinate();
void declare_return();
void declare_graph();
void declare_colorspace();

BOOST_PYTHON_MODULE( YayiCommonPython )
{
  #if !defined(_MSC_VER) && !defined(__MINGW32__)
  bpy::object sys_mod((bpy::handle<>(PyImport_ImportModule("sys"))));
  sys_mod.attr("setdlopenflags")(RTLD_NOW|RTLD_GLOBAL);
  #endif
  
  
  declare_enums();
  declare_utils();
  declare_variants();
  declare_errors();
  declare_object();
  declare_coordinate();
  declare_return();
  declare_graph();
  declare_colorspace();
}
