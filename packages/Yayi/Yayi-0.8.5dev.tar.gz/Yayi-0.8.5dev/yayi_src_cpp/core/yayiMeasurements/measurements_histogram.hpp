#ifndef YAYI_MEASUREMENTS_HISTOGRAM_HPP__
#define YAYI_MEASUREMENTS_HISTOGRAM_HPP__

/*!@file
 * This file defines the histogram functions
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

    /*!@brief Histogram of the image.
     *
     * This function computes the histogram of the image. The histogram is returned in the
     * out variant as sequence of pairs (key, value).
     */
    YMeas_ yaRC image_meas_histogram(const IImage* imin, variant& out);

    /*!@brief Histogram on each regions of an image.
     *
     * This function computes the histogram of each region of an image `imin`. The regions are identified by a value in the provided image imregions.
     * The result is stored in the variant `out` as a sequence of pairs (region_id, histogram), where histogram is also a sequence
     * of pairs (key, value), and region_id is the corresponding region value (from imregions).
     * @note the regions are not necessarilly connected.
     * @author Raffi Enficiaud
     * @anchor image_meas_histogram_on_regions
     */
    YMeas_ yaRC image_meas_histogram_on_regions(const IImage* imin, const IImage* imregions, variant& out);

    //! @} 
  }
}

#endif /* YAYI_MEASUREMENTS_HISTOGRAM_HPP__ */
