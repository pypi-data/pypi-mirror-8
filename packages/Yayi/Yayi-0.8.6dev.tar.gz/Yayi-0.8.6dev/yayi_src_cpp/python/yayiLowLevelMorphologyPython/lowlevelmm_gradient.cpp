#include <yayiLowLevelMorphologyPython/lowlevelmm_python.hpp>
#include <yayiLowLevelMorphology/lowlevel_morpho_gradient.hpp>

using namespace bpy;

void declare_gradient_functions() {
  def("Gradient",     &yayi::llmm::gradient,      "(im_source, SE, im_destination) : Performs the classical morphological gradient of one image into another with the specified structuring element");
  def("GradientSup",  &yayi::llmm::gradient_sup,  "(im_source, SE, im_destination) : Performs the classical morphological half superior gradient of one image into another with the specified structuring element");
  def("GradientInf",  &yayi::llmm::gradient_inf,  "(im_source, SE, im_destination) : Performs the classical morphological half inferior gradient of one image into another with the specified structuring element");
}
