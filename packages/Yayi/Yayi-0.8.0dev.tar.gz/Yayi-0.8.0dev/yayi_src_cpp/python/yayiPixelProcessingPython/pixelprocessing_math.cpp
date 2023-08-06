#include <yayiPixelProcessingPython/pixelprocessing_python.hpp>

#include <yayiPixelProcessing/image_math.hpp>

using namespace bpy;

void declare_math() {

  def("Logarithm",  
    &yayi::logarithm, 
    args("im_source", "im_destination"),
    "Computes the logarithm of each pixels of the image");

  def("Exponential",  
    &yayi::exponential, 
    args("im_source", "im_destination"),
    "Computes the exponential of each pixels of the image");

  def("Power",  
    &yayi::power, 
    args("im_source", "gamma", "im_destination"),
    "Computes the power of each pixels of the image");

  def("Square",  
    &yayi::square, 
    args("im_source", "im_destination"),
    "Computes the square of each pixels of the image");

  def("SquareRoot",  
    &yayi::square_root, 
    args("im_source", "im_destination"),
    "Computes the square root of each pixels of the image");

  def("GaussianRandomGenerator",  
    &yayi::generate_gaussian_random, 
    args("im_destination"),
    "Generates the pixels of the image as being drawn from a gaussian distribution");
}
