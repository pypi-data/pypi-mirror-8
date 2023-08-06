#include <yayiMeasurementsPython/measurements_python.hpp>
#include <yayiMeasurements/measurements_histogram.hpp>

using namespace yayi;



void declare_histogram()
{
  bpy::def("MeasHistogram",
    &measurements_function<&measurements::image_meas_histogram>,
    bpy::args("imin"),
    "Returns the histogram of the image");
  bpy::def("MeasHistogramOnRegions", 
    &measurements_on_regions_function<&measurements::image_meas_histogram_on_regions>,
    bpy::args("imin", "imregions"),
    "Returns the histogram for each region of the image. The regions are non-overlapping and defined by imregions");
}
