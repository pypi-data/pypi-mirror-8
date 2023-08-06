#ifndef MEASUREMENTS_MEAN_VARIANCE_HPP__
#define MEASUREMENTS_MEAN_VARIANCE_HPP__


/*!@file
 * This file defines simple statistic functions over images
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

    //! Returns the mean over the image
    YMeas_ yaRC image_meas_mean(const IImage* imin, variant& out);

    //! Returns the mean on each regions identified as a unique id in imregions
    //! See @ref image_meas_histogram_on_regions for the return type
    YMeas_ yaRC image_meas_mean_on_region(const IImage* imin, const IImage* imregions, variant& out);

    //! Returns the circular mean on each regions identified as a unique id in imregions
    //! See @ref image_meas_histogram_on_regions for the return type
    //! @anchor image_meas_circular_mean_and_concentration_on_region
    YMeas_ yaRC image_meas_circular_mean_and_concentration_on_region(const IImage* imin, const IImage* imregions, variant& out);

    //! Returns the circular mean on first channel linearly weighted by third channel, on each regions identified as a unique id in imregions
    //! See @ref image_meas_histogram_on_regions for the return type
    //! @anchor image_meas_weighted_circular_mean_and_concentration_on_region
    YMeas_ yaRC image_meas_weighted_circular_mean_and_concentration_on_region(const IImage* imin, const IImage* imregions, variant& out);

    //! Same as @ref image_meas_circular_mean_and_concentration_on_region, but operates only on the points of immask of value mask_value
    YMeas_ yaRC image_meas_circular_mean_and_concentration_on_mask(const IImage* imin, const IImage* immask, variant const& mask_value, variant& out);

    //! Same as @ref image_meas_weighted_circular_mean_and_concentration_on_region, but operates only on the points of immask of value mask_value
    YMeas_ yaRC image_meas_weighted_circular_mean_and_concentration_on_mask(const IImage* imin, const IImage* immask, variant const& mask_value, variant& out);

    //! @} doxygroup: meas_mean_variance_grp
  }
}


#endif /* MEASUREMENTS_MEAN_VARIANCE_HPP__ */

