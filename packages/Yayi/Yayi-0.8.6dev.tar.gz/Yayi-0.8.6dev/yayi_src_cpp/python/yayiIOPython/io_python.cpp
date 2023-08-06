

#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;

#include <yayiIOPython/io_python.hpp>

void declare_jpg();
void declare_png();
void declare_raw();
void declare_tiff();
#ifdef YAYI_IO_HDF5_ENABLED__
  void declare_hdf5();
#endif
#ifdef YAYI_IO_NUMPY_ENABLED__
  void declare_numpy();
#endif

BOOST_PYTHON_MODULE( YayiIOPython )
{
  bpy::def("writeEPS", &yayi::IO::writeEPS, "(filename, image) : writes the image into the specified EPS file");

  declare_jpg();
  declare_png();
  declare_raw();
  declare_tiff();
  #ifdef YAYI_IO_HDF5_ENABLED__
    declare_hdf5();
  #endif

  #ifdef YAYI_IO_NUMPY_ENABLED__
    declare_numpy();
  #endif
}
