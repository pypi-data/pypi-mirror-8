
#include <yayiStructuringElementPython/structuringelement_python.hpp>
#include <boost/python/scope.hpp>
#include <yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <boost/bind.hpp>
#include <boost/function.hpp>

template <class V, V* p>
struct getSEPredefined 
{
  static yayi::se::IStructuringElement const* get() 
  {
    static yayi::se::IStructuringElement const* const v = p;
    return v->Clone();
  }
};

typedef boost::function< yayi::se::IStructuringElement const* () > f_type;

void declare_predefined() 
{
  using namespace yayi;
  using namespace yayi::se;
  
  bpy::def("SESquare2D",    &(getSEPredefined<const s_neighborlist_se< s_coordinate<2> >,         &yayi::se::SESquare2D >::get), bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SECross2D",     &(getSEPredefined<const s_neighborlist_se< s_coordinate<2> >,         &yayi::se::SECross2D  >::get), bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SEHex2D",       &(getSEPredefined<const s_neighborlist_se_hexa_x< s_coordinate<2> >,  &yayi::se::SEHex2D    >::get), bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SESquare3D",    &(getSEPredefined<const s_neighborlist_se< s_coordinate<3> >,         &yayi::se::SESquare3D >::get), bpy::return_value_policy<bpy::manage_new_object>());

  bpy::def("SESegmentX2D",  &(getSEPredefined<const s_neighborlist_se< s_coordinate<2> >,         &yayi::se::SESegmentX2D>::get),bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SESegmentY2D",  &(getSEPredefined<const s_neighborlist_se< s_coordinate<2> >,         &yayi::se::SESegmentY2D>::get),bpy::return_value_policy<bpy::manage_new_object>());


  bpy::def("SESegmentX3D",  &(getSEPredefined<const s_neighborlist_se< s_coordinate<3> >,         &yayi::se::SESegmentX3D>::get),bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SESegmentY3D",  &(getSEPredefined<const s_neighborlist_se< s_coordinate<3> >,         &yayi::se::SESegmentY3D>::get),bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SESegmentZ3D",  &(getSEPredefined<const s_neighborlist_se< s_coordinate<3> >,         &yayi::se::SESegmentZ3D>::get),bpy::return_value_policy<bpy::manage_new_object>());
  

  

}

