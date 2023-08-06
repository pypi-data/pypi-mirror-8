#include <yayiMeasurementsPython/measurements_python.hpp>
#include <yayiMeasurements/measurements_min_max.hpp>

using namespace yayi;



void declare_min_max()
{
  bpy::def("MeasMinMax", 
    &measurements_function<&measurements::image_meas_min_max>
    );
  
}
