#include <yayiReconstructionPython/reconstruction_python.hpp>
#include <yayiReconstruction/morphological_fill_holes.hpp>

void declare_morphological_fill_holes()
{
  using namespace bpy;
  def("FillHoles",
    &yayi::reconstructions::fill_holes, 
    bpy::args("imin", "SE", "imout"),
    "Fills the holes of imin using SE as neighboring graph. Stores the output in imout"
  );


}
