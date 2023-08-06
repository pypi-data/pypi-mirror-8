#ifndef YAYI_MEASUREMENTS_HPP__
#define YAYI_MEASUREMENTS_HPP__

/*!@file
 * @brief Global definition for the measurements library
 *
 */


#include <yayiCommon/common_config.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>


#ifdef YAYI_EXPORT_MEASUREMENTS_
#define YMeas_ MODULE_EXPORT
#else
#define YMeas_ MODULE_IMPORT
#endif

namespace yayi
{
  namespace measurements
  {
    /*!@defgroup meas_grp Measurements
     * @brief Measurements on images.
     *
     * This group of functions is concerned in performing measurements on images or part of images. The measurements may be performed:
     * - on the whole image: The functions implementing such measurements are generally 2-ary, and return the computation in a variant which
     *   format is specific to the measurement.
     * - on one or several regions on images: such functions need an additional image or region, storing for each pixel location the region to which
     *   the pixel belongs. The regions do not need to be connected. The computation is still returned in a variant, which now becomes an associative map
     *   where the key is the id of the region, and the value the corresponding measurement. Note that since an image is used for encoding the regions,
     *   one pixel of the measurement image cannot belong to more than one region.
     * - on a masked area: functions implementing this feature need an additional image which encodes a mask. This is a special case of the measurement
     *   on regions with two regions: a foreground and a background. The measurement is performed on the foreground only. 
     */

    /*!@defgroup meas_details_grp Measurements implementation details.
     * @ingroup meas_grp
     * @brief Details of the template function and functor needed to implement the interface level (and more).
     *
     * The process of measuring a sequence of pixels may be seen as a simple application of an unary functor to each pixel of this sequence.
     * The functors performing the measurements should implement the @ref measurement_functor_concepts "Measurement function objects" concept, which allow them
     * to decouple the accumulating and the final computation of the result.
     *
     */
  }
}
#endif /* YAYI_MEASUREMENTS_HPP__ */
