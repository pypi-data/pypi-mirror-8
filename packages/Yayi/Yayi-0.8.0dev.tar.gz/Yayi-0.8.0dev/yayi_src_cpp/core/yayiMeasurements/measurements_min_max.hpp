#ifndef YAYI_MEASUREMENTS_MIN_MAX_HPP__
#define YAYI_MEASUREMENTS_MIN_MAX_HPP__

/*!@file
 * This file defines the min/max function
 */

#include <yayiMeasurements/yayiMeasurements.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>

namespace yayi
{
  namespace measurements
  {
    /*!@brief Minimum and maximum values in an image.
     * @ingroup meas_grp
     *
     *This function computes the minimum and maximum values of an image. The result is saved into the output variant as a pair
     * of values (min, max) of the same type as the image.
     *
     */
    YMeas_ yaRC image_meas_min_max(const IImage* imin, variant& out);

  }
}


#endif /* YAYI_MEASUREMENTS_MIN_MAX_HPP__ */
