#include <yayiIOPython/io_python.hpp>

using namespace yayi::IO;

yayi::IImage* read_png(const std::string & filename) {

  using namespace yayi;
  yayi::IImage* image = 0;
  yaRC ret = yayi::IO::readPNG (filename, image);
  if(ret != yaRC_ok)
    throw errors::yaException(ret);
  
  return image;

}

void declare_png() {
  
  bpy::def("readPNG", &read_png, "(filename) : returns the specified Jpeg image", bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("writePNG",&yayi::IO::writePNG, "(filename, image) : writes the image into the specified file");


}

