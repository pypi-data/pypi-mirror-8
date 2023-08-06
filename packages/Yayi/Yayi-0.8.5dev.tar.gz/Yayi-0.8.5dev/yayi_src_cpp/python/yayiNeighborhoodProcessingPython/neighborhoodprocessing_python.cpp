
#include <yayiNeighborhoodProcessingPython/neighborhoodprocessing_python.hpp>


#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;

void declare_local_statistics();

BOOST_PYTHON_MODULE( YayiNeighborhoodProcessingPython )
{
  declare_local_statistics();
}
