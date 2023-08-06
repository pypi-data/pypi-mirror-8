
#include <yayiReconstructionPython/reconstruction_python.hpp>


#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;

void declare_morphological_reconstructions();
void declare_morphological_fill_holes();
void declare_highlevel_minima_maxima();

BOOST_PYTHON_MODULE( YayiReconstructionPython )
{
  declare_morphological_reconstructions();
  declare_morphological_fill_holes();
  declare_highlevel_minima_maxima();
}
