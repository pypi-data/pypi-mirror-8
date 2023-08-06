

#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;
#include <yayiLabelPython/label_python.hpp>

void declare_label_basic();
void declare_label_extrema();

BOOST_PYTHON_MODULE( YayiLabelPython )
{
  declare_label_basic();
  declare_label_extrema();
}
