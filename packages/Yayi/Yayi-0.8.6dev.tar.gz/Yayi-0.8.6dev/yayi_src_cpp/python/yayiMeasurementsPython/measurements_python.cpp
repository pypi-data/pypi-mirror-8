#include <yayiMeasurementsPython/measurements_python.hpp>


#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

void declare_min_max();
void declare_histogram();
void declare_stats();

BOOST_PYTHON_MODULE( YayiMeasurementsPython )
{
  declare_min_max();
  declare_histogram();
  declare_stats();
}
