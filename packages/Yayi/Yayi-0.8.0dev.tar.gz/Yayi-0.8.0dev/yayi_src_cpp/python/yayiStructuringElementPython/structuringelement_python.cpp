#include <yayiStructuringElementPython/structuringelement_python.hpp>

#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;


void declare_se();
void declare_neighbor_factory();
void declare_predefined();

BOOST_PYTHON_MODULE( YayiStructuringElementPython )
{
  declare_se();
  declare_neighbor_factory();
  declare_predefined();
}
