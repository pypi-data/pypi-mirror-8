#include <yayiStructuringElementPython/structuringelement_python.hpp>

// reference to an internal structure of yayiImageCorePython
#include <yayiImageCorePython/imagecore_python.hpp>

using namespace yayi;
using namespace yayi::se;

namespace yayi
{
  IConstIteratorWrapper neighbor_range(IConstNeighborhood*n) {
    return IConstIteratorWrapper(n->BeginConst(), n->EndConst());
  }
}

void declare_neighbor_factory() {
 
      
  bpy::class_<IConstNeighborhood, bpy::bases<IObject>, boost::noncopyable >(
    "ConstNeighborhood", 
    "Main const neighborhood class. This class does not allow any writing into the image", bpy::no_init)
    
    // size
    .def(
      "Center",
      (yaRC (IConstNeighborhood::*)(const IConstNeighborhood::coordinate_type&))&IConstNeighborhood::Center,
      "(coordinate): centers the structuring element at the specified coordinate")
    .def(
      "Center",
      (yaRC (IConstNeighborhood::*)(const IConstNeighborhood::const_iterator&))&IConstNeighborhood::Center,
      "(iterator): centers the structuring element at the specified iterator position")
    .def(
      "Center",
      (yaRC (IConstNeighborhood::*)(const offset))&IConstNeighborhood::Center,
      "(offset): centers the structuring element at the specified offset")

    .def(
      "SetShift",
      &IConstNeighborhood::SetShift,
      "specifies the shift that will be later applied to the center")
    .def(
      "ShiftCenter",
      &IConstNeighborhood::ShiftCenter,
      "shifts the center by a shift previously defined")
    
    .add_property(
      "pixels",
      bpy::make_function(
        &yayi::neighbor_range,
        bpy::with_custodian_and_ward_postcall<0,1>()
      ),
      "returns an iterator on the pixels in the neighborhood previously centered")
  ;
  
  bpy::def("NeighborhoodFactory",
    &IConstNeighborhood::Create,
    "(image, structuring element): factory for the neighborhood. Returns a neighborhood instance on the image "
    "based on the provided structuring element. Returns None on error.",
    bpy::return_value_policy<bpy::manage_new_object>());
}

