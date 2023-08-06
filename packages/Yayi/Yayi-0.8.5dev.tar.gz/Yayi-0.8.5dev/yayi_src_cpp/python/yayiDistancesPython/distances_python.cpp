#include <yayiDistancesPython/distances_python.hpp>


#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;

void declare_quasi_distance();
void declare_binary_distance();

BOOST_PYTHON_MODULE( YayiDistancesPython )
{
  declare_quasi_distance();
  declare_binary_distance();
}
