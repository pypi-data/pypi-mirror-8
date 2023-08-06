#include <yayiLowLevelMorphologyPython/lowlevelmm_python.hpp>
#include <yayiLowLevelMorphology/lowlevel_hit_or_miss.hpp>
using namespace bpy;

void declare_hit_or_miss_functions() {
  def("SoillesHitOrMiss",
    &yayi::llmm::hit_or_miss_soille,
    bpy::args("im_source", "foreground_SE", "background_SE", "im_destination"),
    "Performs the hit-or_miss transform for gray level images based on Soilles definition.");

}
