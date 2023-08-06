
#include <yayiLabelPython/label_python.hpp>
#include <yayiLabel/yayi_label_extrema.hpp>
using namespace yayi::label;

void declare_label_extrema() {
  bpy::def("ImageLabelMinimas", &ImageLabelMinimas, "(imin, se, imout) : labels minimum plateaus of imin into imout with a single id per connected component");
  bpy::def("ImageLabelMaximas", &ImageLabelMaximas, "(imin, se, imout) : labels maximum plateaus of imin into imout with a single id per connected component");
}
