
#include <yayiLabelPython/label_python.hpp>
#include <yayiLabel/yayi_label_binary_with_measure.hpp>
using namespace yayi::label;

namespace 
{

  yayi::variant image_label_binary_components_with_area_python(
    const yayi::IImage* imin, 
    const yayi::se::IStructuringElement* se, 
    yayi::IImage* imout) 
  {
    using namespace yayi;
    variant out;
    yaRC ret = image_label_binary_components_with_area(imin, se, imout, out);
    if(ret != yaRC_ok)
      throw errors::yaException(ret);
    
    return out;
  }

  yayi::variant image_label_non_black_to_offset_python(
    const yayi::IImage* imin, 
    const yayi::se::IStructuringElement* se) 
  {

    using namespace yayi;
    variant out;
    yaRC ret = image_label_non_black_to_offset(imin, se, out);
    if(ret != yaRC_ok)
      throw errors::yaException(ret);
    
    return out;
  }

}



void declare_label_basic() 
{
  bpy::def("image_label", 
    &image_label, 
    bpy::args("imin", "se", "imout"),
    "Labels the connected components of imin in imout. Each connected component is "
    "identified in imout with a unique value. The connectivity used for the connected components "
    "is given by se. \n\n"
    ":param image imin: input image\n"
    ":param SE se: connectivity in imin for discovering the connection between two pixels\n"
    ":param image imout: output image\n"
    ":returns: None on success, throws an error otherwise"
    );

  bpy::def("image_label_binary_components_with_area", 
    &image_label_binary_components_with_area_python, 
    bpy::args("imin", "se", "imout"), 
    "Labels components formed of non \"black\" pixels and extracts their area\n"
    "  :returns: a \"dictionary\" which key is the id of the connected component, and the value is its area."
    );

  bpy::def("image_label_non_black_to_offset", 
    &image_label_non_black_to_offset_python, 
    bpy::args("imin", "se"), 
    "returns a list of list containing the offsets of the points of each connected component");


}


