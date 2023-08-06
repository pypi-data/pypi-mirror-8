

#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;

#include <yayiImageCorePython/imagecore_python.hpp>

void declare_image();
void declare_iterators();
void declare_interface_pixel();
void declare_utilities();

BOOST_PYTHON_MODULE( YayiImageCorePython )
{
  declare_image();
  declare_iterators();
  declare_interface_pixel();
  declare_utilities();
}
