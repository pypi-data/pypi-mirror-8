#include <yayiMeasurementsPython/measurements_python.hpp>
#include <yayiMeasurements/measurements_mean_variance.hpp>
#include <yayiMeasurements/measurements_quantiles.hpp>

using namespace yayi;

void declare_stats()
{
  bpy::def("MeasMean",
    &measurements_function<&measurements::image_meas_mean>,
    bpy::args("imin"),
    "Returns the mean of the image");
    
  bpy::def("MeasMeanOnRegions", 
    &measurements_on_regions_function<&measurements::image_meas_mean_on_region>,
    bpy::args("imin", "imregions"),
    "Returns the mean for each region of the image. The regions are non-overlapping and defined by imregions");

  bpy::def("MeasCircularMeanAndConcentrationOnRegions", 
    &measurements_on_regions_function<&measurements::image_meas_circular_mean_and_concentration_on_region>,
    bpy::args("imin", "imregions"),
    "Returns the circular mean and concentration for each region of the image. "
    "The regions are non-overlapping and defined by imregions. "
    "The return type is a map of complex elements");

  bpy::def("MeasWeightedCircularMeanAndConcentrationOnRegion", 
    &measurements_on_regions_function<&measurements::image_meas_weighted_circular_mean_and_concentration_on_region>,
    bpy::args("imin", "imregions"),
    "Returns the circular mean and concentration of channel 0 weighted by channel 2 for each region of the image. "
    "The regions are non-overlapping and defined by imregions. "
    "The return type is a map of complex elements.");

  bpy::def("MeasCircularMeanAndConcentrationOnMask",
    &measurements_on_mask_function<&measurements::image_meas_circular_mean_and_concentration_on_mask>,
    bpy::args("imin", "immask", "mask_value"),
    "Returns the circular mean and concentration for each region of the image. "
    "The regions are non-overlapping and defined by immask. "
    "The return type is a map of complex elements");

  bpy::def("MeasWeightedCircularMeanAndConcentrationOnMask",
    &measurements_on_mask_function<&measurements::image_meas_weighted_circular_mean_and_concentration_on_mask>,
    bpy::args("imin", "immask", "mask_value"),
    "Returns the circular mean and concentration of channel 0 weighted by channel 2 for each region of the image. "
    "The regions are non-overlapping and defined by immask. "
    "The return type is a map of complex elements.");





  bpy::def("meas_median",
    &measurements_function<&measurements::image_meas_median>,
    bpy::args("imin"),
    "Returns the median of the image");
    

}
