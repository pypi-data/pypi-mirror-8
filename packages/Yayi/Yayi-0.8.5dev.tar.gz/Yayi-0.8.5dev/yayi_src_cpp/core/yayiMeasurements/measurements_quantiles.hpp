#ifndef YAYI_MEASUREMENTS_QUANTILES_HPP__
#define YAYI_MEASUREMENTS_QUANTILES_HPP__

/*!@file
 * This file defines the quantiles functions
 */

#include <yayiMeasurements/yayiMeasurements.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>

namespace yayi
{
  namespace measurements
  {
    /*!@addtogroup meas_grp
     * @{
     */

    /*!Median value of the image.
     *
     * @note the median may be computed directly from the histogram.
     */
    YMeas_ yaRC image_meas_median(const IImage* imin, variant& out);

    //! @} doxygroup: meas_quantile_grp


  }
}


#endif /* YAYI_MEASUREMENTS_QUANTILES_HPP__ */
