#include <yayiPixelProcessingPython/pixelprocessing_python.hpp>


#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;


void declare_unary_pointwise();
void declare_channel_color();
void declare_compare();
void declare_arithmetic();
void declare_logic();
void declare_math();

BOOST_PYTHON_MODULE( YayiPixelProcessingPython )
{
  declare_unary_pointwise();
  declare_channel_color();
  declare_compare();
  declare_arithmetic();
  declare_logic();
  declare_math();
}
