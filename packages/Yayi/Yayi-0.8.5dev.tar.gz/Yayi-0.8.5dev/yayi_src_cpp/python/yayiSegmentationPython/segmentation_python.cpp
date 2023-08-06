#include <yayiSegmentationPython/segmentation_python.hpp>


#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;

void declare_watershed();

BOOST_PYTHON_MODULE( YayiSegmentationPython )
{
  declare_watershed();
}
