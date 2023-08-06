#include <yayiIOPython/io_python.hpp>

using namespace yayi::IO;

yayi::IImage* read_tiff(const std::string & filename, int index = 0) {

  using namespace yayi;
  yayi::IImage* image = 0;
  yaRC ret = yayi::IO::readTIFF (filename, index, image);
  if(ret != yaRC_ok)
    throw errors::yaException(ret);

  return image;

}

void declare_tiff() {

  bpy::def("readTIFF", &read_tiff, "(filename) : reads the specified TIFF image", bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("writeTIFF",&yayi::IO::writeTIFF, "(filename, image) : writes the image into the specified file in TIFF format");

}

