#include <yayiPixelProcessingPython/pixelprocessing_python.hpp>

#include <yayiPixelProcessing/image_constant.hpp>
#include <yayiPixelProcessing/image_copy.hpp>
#include <yayiPixelProcessing/image_channels_process.hpp>



using namespace bpy;

void declare_unary_pointwise() {

  def("Copy",
      (yayi::yaRC (*)(const yayi::IImage*, yayi::IImage* ))&yayi::copy,
      bpy::args("im_source", "im_destination"), 
      "Copy one image onto another");

  def("Constant", 
      (yayi::yaRC (*)(const yayi::variant &, yayi::IImage* ))&yayi::constant, 
      bpy::args("value", "im"),
      "Sets all the pixels of the image to value \"value\"");

  def("CopyWindow", 
      (yayi::yaRC (*)(const yayi::IImage*, const yayi::variant &, const yayi::variant &, yayi::IImage* ))&yayi::copy,
       bpy::args("im_source", "window_source", "window_destination", "im_destination"), 
       "Copy a window of an image onto a window of another image");

  def("ConstantWindow", 
      (yayi::yaRC (*)(const yayi::variant &, const yayi::variant &, yayi::IImage* ))&yayi::constant,
       bpy::args("value", "window", "im"), 
       "Sets all the pixels of the image's window to the constant value");

}

