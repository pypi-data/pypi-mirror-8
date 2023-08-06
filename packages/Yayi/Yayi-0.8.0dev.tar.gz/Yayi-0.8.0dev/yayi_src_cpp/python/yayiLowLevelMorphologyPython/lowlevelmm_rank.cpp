#include <yayiLowLevelMorphologyPython/lowlevelmm_python.hpp>
#include <yayiLowLevelMorphology/lowlevel_erosion_dilation.hpp>
#include <yayiLowLevelMorphology/lowlevel_opening_closing.hpp>

using namespace bpy;

void declare_rank_functions() {
  def("Erosion",     &yayi::llmm::erosion,      "(im_source, SE, im_destination) : Performs the erosion of one image into another with the specified structuring element");
  def("Dilation",    &yayi::llmm::dilation,     "(im_source, SE, im_destination) : Performs the dilation of one image into another with the specified structuring element");

  def("MinkowskiAddition",     &yayi::llmm::minkowski_addition,
      "(im_source, SE, im_destination) : Performs the Minkowski addition of one image into another with the specified structuring element "
      "(basically dilation with the implicitely transposed structuring element)");
  def("MinkowskiSubtraction",  &yayi::llmm::minkowski_subtraction,
      "(im_source, SE, im_destination) : Performs the Minkowski subtraction of one image into another with the specified structuring element "
      "(basically erosion with the implicitely transposed structuring element)");


  def("Open",        &yayi::llmm::open,      "(im_source, SE, im_destination) : Performs the opening of one image into another with the specified structuring element");
  def("Close",       &yayi::llmm::close,     "(im_source, SE, im_destination) : Performs the closing/closure of one image into another with the specified structuring element");


}

