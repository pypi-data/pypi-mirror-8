
#include <yayiCommonPython/common_python.hpp>
#include <yayiCommon/include/common_object.hpp>


void declare_object() {
  using namespace yayi;

  bpy::class_<IObject, boost::noncopyable>("Object", "An abstract object", bpy::no_init)
    .def("DynamicType", &IObject::DynamicType, "type of the object")
    .def("Description", &IObject::Description, "description of the object") 
    .def("__str__",     &IObject::Description)
    ;

}

