
#include <yayiImageCorePython/imagecore_python.hpp>

#include <boost/python/class.hpp>
#include <boost/python/manage_new_object.hpp>
#include <boost/python/return_value_policy.hpp>



void declare_interface_pixel() {

  using namespace yayi;
  
  bpy::class_<IVariantProxy, std::auto_ptr<IVariantProxy>, boost::noncopyable >("ImagePixel", "Pointer to a pixel on an image", bpy::no_init)
    .add_property("value", &IVariantProxy::getPixel, &IVariantProxy::setPixel)
    .def(bpy::self == IVariantProxy::pixel_value_type())
    .def(bpy::self != IVariantProxy::pixel_value_type())
    .def(bpy::self == bpy::other<IVariantProxy>())
    .def(bpy::self != bpy::other<IVariantProxy>())
//    virtual bool    IVariantProxy::isEqual           (const pixel_value_type &) const = 0;
//    virtual bool    IVariantProxy::isDifferent       (const pixel_value_type &) const = 0;

  ;

  
  

}

