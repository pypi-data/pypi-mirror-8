#include <yayiImageCorePython/imagecore_python.hpp>
#include <yayiImageCore/include/yayiImageUtilities_T.hpp>
#include <yayiCommon/common_coordinates.hpp>
#include <boost/python/stl_iterator.hpp>


template <class coordinate>
bpy::list from_offsets_to_coordinate_python(const coordinate &size, bpy::object o)
{
  bpy::stl_input_iterator<yayi::offset> it(o), ite;
  typedef std::vector<coordinate> coord_cont_t;
  coord_cont_t const& ret = yayi::from_offsets_to_coordinate(size, it, ite);

  bpy::list l;
  for(typename coord_cont_t::const_iterator i(ret.begin()), ie(ret.end()); i != ie; ++i)
    l.append(*i);
  return l;
}

namespace yayi
{
  size_t total_number_of_points_python(const IImage* im)
  {
    if(!im)
    {
      throw errors::yaException(yaRC_E_null_pointer);
    }

    return static_cast<size_t>(total_number_of_points(im->GetSize()));
  }
}





void declare_utilities()
{
  using namespace yayi;

  bpy::def("FromOffsetToCoordinate", 
    (s_coordinate<0> (*)(const s_coordinate<0> &, offset))&from_offset_to_coordinate,
    bpy::args("size", "offset"), "returns the coordinate associated to an offset");

  bpy::def("FromOffsetsToCoordinates", 
    &/*from_offsets_to_coordinate*/from_offsets_to_coordinate_python< s_coordinate<0> >, 
    bpy::args("size", "v_offset"), "returns the list of coordinates associated to the list of offsets");

  bpy::def("total_number_of_points",
    &total_number_of_points_python,
    bpy::args("im"),
    "returns the total number of points contained inside an image");

}
