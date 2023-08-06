#include <yayiCommonPython/common_python.hpp>
#include <yayiCommon/common_colorspace.hpp>
#include <boost/python/copy_const_reference.hpp>
#include <boost/python/enum.hpp>


void declare_colorspace() {
  
  using namespace yayi;

  
  bpy::enum_<yayi::yaColorSpace::yaColorSpaceMajor>("colorspace_major")
  .value("cs_undefined",   yayi::s_yaColorSpace::ecd_undefined)
  .value("cs_rgb",   yayi::s_yaColorSpace::ecd_rgb)
  .value("cs_hls",   yayi::s_yaColorSpace::ecd_hls)
  .value("cs_xyz",   yayi::s_yaColorSpace::ecd_xyz)
  .value("cs_xyY",   yayi::s_yaColorSpace::ecd_xyY)
  .value("cs_yuv",   yayi::s_yaColorSpace::ecd_yuv)
  .export_values()
  ;
  
  
  bpy::enum_<yayi::yaColorSpace::yaColorSpaceMinor>("colorspace_minor")
  .value("csm_undefined",   yayi::yaColorSpace::ecdm_undefined)
  .value("csm_hls_l1",      yayi::yaColorSpace::ecdm_hls_l1)
  .value("csm_hls_trig",    yayi::yaColorSpace::ecdm_hls_trig)
  .export_values()
  ;
  
  bpy::enum_<yayi::yaColorSpace::yaIlluminant>("illuminant")
  .value("ill_undefined",   yayi::yaColorSpace::ei_undefined)
  .value("ill_d50",         yayi::yaColorSpace::ei_d50)
  .value("ill_d55",         yayi::yaColorSpace::ei_d55)
  .value("ill_d65",         yayi::yaColorSpace::ei_d65)
  .value("ill_d75",         yayi::yaColorSpace::ei_d75)
  .value("ill_A",           yayi::yaColorSpace::ei_A)
  .value("ill_B",           yayi::yaColorSpace::ei_B)
  .value("ill_C",           yayi::yaColorSpace::ei_C)
  .value("ill_E",           yayi::yaColorSpace::ei_E)
  .value("ill_blackbody",   yayi::yaColorSpace::ei_blackbody)
  .export_values()
  ;

  bpy::enum_<yayi::yaColorSpace::yaRGBPrimary>("primaries")
  .value("prim_undefined",   yayi::yaColorSpace::ergbp_undefined)
  .value("prim_CIE",         yayi::yaColorSpace::ergbp_CIE)
  .value("prim_sRGB",        yayi::yaColorSpace::ergbp_sRGB)
  .value("prim_AdobeRGB",    yayi::yaColorSpace::ergbp_AdobeRGB)
  .value("prim_AppleRGB",    yayi::yaColorSpace::ergbp_AppleRGB)
  .value("prim_NTSCRGB",     yayi::yaColorSpace::ergbp_NTSCRGB)
  .value("prim_SecamRGB",    yayi::yaColorSpace::ergbp_SecamRGB)
  .export_values()
  ;
  
    
    
  bpy::class_<yayi::yaColorSpace>("colorspace", bpy::init<>())
  .def(bpy::init<yaColorSpace::yaColorSpaceMajor,bpy::optional<yaColorSpace::yaIlluminant, yaColorSpace::yaRGBPrimary, yaColorSpace::yaColorSpaceMinor> >())
  .def_readwrite("major",       &yayi::yaColorSpace::cs_major)
  .def_readwrite("minor",       &yayi::yaColorSpace::cs_minor)
  .def_readwrite("illuminant",  &yayi::yaColorSpace::illuminant)
  .def_readwrite("primary",     &yayi::yaColorSpace::primary)
  .def(bpy::self == bpy::self)                                      // __eq__
  .def("__str__",               &yayi::yaColorSpace::operator string_type)//&yayi::type::operator string_type)
  ;
 
  bpy::def(
    "blackbody_radiation", 
    yayi::blackbody_radiation, 
    "Returns the value of the black body radiator at the specified wavelength and temperature");
  bpy::def(
    "blackbody_radiation_normalized", 
    yayi::blackbody_radiation_normalized, 
    "Returns the value of the black body radiator at the specified wavelength and temperature, normalized"
    "by the black body radiation value at the same wavelength and specified normalization temperature");
  
}
