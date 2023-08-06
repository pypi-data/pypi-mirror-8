#include <yayiDistancesPython/distances_python.hpp>
#include <yayiDistances/morphological_distance.hpp>
using namespace bpy;


void declare_binary_distance() {

  def("DistanceFromSetsBoundary",
    &yayi::distances::DistanceFromSetsBoundary, 
    "(im_source, SE, im_distance) : Performs the morphological distance transform from the sets boundary");
  
}
