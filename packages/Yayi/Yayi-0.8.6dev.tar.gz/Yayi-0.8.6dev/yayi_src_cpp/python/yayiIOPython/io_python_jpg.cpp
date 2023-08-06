#include <yayiIOPython/io_python.hpp>

using namespace yayi::IO;

yayi::IImage* read_jpeg(const std::string & filename) {

  using namespace yayi;
  yayi::IImage* image = 0;
  yaRC ret = yayi::IO::readJPG (filename, image);
  if(ret != yaRC_ok)
    throw errors::yaException(ret);
  
  return image;

}

void declare_jpg() {
  
  bpy::def("readJPG", &read_jpeg, "(filename) : returns the specified Jpeg image", bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("writeJPG",&yayi::IO::writeJPG, "(filename, image) : writes the image into the specified file");


}

