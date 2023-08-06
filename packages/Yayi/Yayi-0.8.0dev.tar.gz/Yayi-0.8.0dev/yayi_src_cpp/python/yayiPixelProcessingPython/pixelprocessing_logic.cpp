#include <yayiPixelProcessingPython/pixelprocessing_python.hpp>

#include <yayiPixelProcessing/image_logics.hpp>

using namespace bpy;

void declare_logic() {

  def("BitwiseNot",  
    &yayi::image_bitwise_not, 
    args("im_source", "im_destination"),
    "Logical not of the input image");
  def("BitwiseAnd",  
    &yayi::image_bitwise_and, 
    args("im_source1", "im_source2", "im_destination"),
    "Logical and between two images");
  def("BitwiseOr",  
    &yayi::image_bitwise_or, 
    args("im_source1", "im_source2", "im_destination"),
    "Logical or between two images");
}
