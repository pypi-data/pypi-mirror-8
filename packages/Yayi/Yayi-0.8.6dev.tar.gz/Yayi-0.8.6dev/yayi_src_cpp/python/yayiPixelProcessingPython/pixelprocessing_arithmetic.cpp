#include <yayiPixelProcessingPython/pixelprocessing_python.hpp>

#include <yayiPixelProcessing/image_arithmetics.hpp>

using namespace bpy;

void declare_arithmetic() {

  def("Add",  
    &yayi::image_add, 
    args("im_source1", "im_source2", "im_destination"),
    "Adds two images");

  def("Subtract",
    &yayi::image_subtract, 
    args("im_source1", "im_source2", "im_destination"),
    "Subtracts two images");

  def("SubtractLowerBound",
    &yayi::image_subtract_with_lower_bound, 
    args("im_source1", "im_source2", "lower_bound", "im_destination"),
    "Subtracts two images with a lower bound, in case pixel_left < pixel_right");



  def("AbsSubtract",
    &yayi::image_abssubtract, 
    args("im_source1", "im_source2", "im_destination"),
    "Pixel-wise absolute difference of two images");
  
  def("Multiply",  
    &yayi::image_multiply, 
    args("im_source1", "im_source2", "im_destination"),
    "Pixel-wise multiplication of two images");

  def("AddConstant",  
    &yayi::image_add_constant, 
    args("im_source", "value", "im_destination"),
    "Pixel-wise addition of a constant value");

  def("AddConstantUpperBound",  
    &yayi::image_add_constant_upper_bound, 
    args("im_source", "value", "im_destination"),
    "Adds a constant value to the image, with an upper-bound on the addition (such as the output value is never greater than the upper-bound)");
  

  def("SubtractConstant",  
    &yayi::image_subtract_constant, 
    args("im_source", "value", "im_destination"),
    "Subtract a constant value from the image");

  def("SubtractConstantLowerBound",  
    &yayi::image_subtract_constant_lower_bound, 
    args("im_source", "value", "im_destination"),
    "Subtract a constant value from the image, with an lower-bound on the subtraction (such as the output value is never lower than the lower-bound).");

  def("MultiplyConstant",  
    &yayi::image_multiply_constant, 
    args("im_source", "value", "im_destination"),
    "Multiplies an image by a constant value");
  
  def("Intersection",  
    &yayi::image_infimum, 
    args("im_source1", "im_source2", "im_destination"),
    "Intersection (infimum) of two images");

  def("Union",  
    &yayi::image_supremum, 
    args("im_source1", "im_source2", "im_destination"),
    "Union (supremum) of two images");
  

}
