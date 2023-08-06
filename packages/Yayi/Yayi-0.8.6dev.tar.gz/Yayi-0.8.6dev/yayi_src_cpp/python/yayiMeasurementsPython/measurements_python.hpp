#ifndef MEASUREMENTS_PYTHON_HPP__
#define MEASUREMENTS_PYTHON_HPP__

#include <boost/python.hpp>
#include <boost/python/object.hpp>
#include <boost/python/def.hpp>

namespace bpy = boost::python;

#include <yayiCommon/common_types.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiMeasurements/yayiMeasurements.hpp>

namespace yayi
{
  typedef yaRC (*measurements_function_t)(IImage const*, variant&);
  typedef yaRC (*measurements_on_regions_function_t)(IImage const*, IImage const*, variant&);
  typedef yaRC (*measurements_on_mask_function_t)(IImage const*, IImage const*, variant const&, variant&);


  template <measurements_function_t p>
  variant measurements_function(IImage const* imin)
  {
    variant out;
    yaRC res = p(imin, out);
    if(res != yaRC_ok)
      throw errors::yaException(res);
    
    return out;
    
  }
  
  template <measurements_on_regions_function_t p>
  variant measurements_on_regions_function(const IImage* imin, IImage const* imregions)
  {
    variant out;
    yaRC res = p(imin, imregions, out);
    if(res != yaRC_ok)
      throw errors::yaException(res);
    
    return out;
    
  }  

  template <measurements_on_mask_function_t p>
  variant measurements_on_mask_function(const IImage* imin, IImage const* immask, variant const& mask_value)
  {
    variant out;
    yaRC res = p(imin, immask, mask_value, out);
    if(res != yaRC_ok)
      throw errors::yaException(res);

    return out;
  }
}



#endif
