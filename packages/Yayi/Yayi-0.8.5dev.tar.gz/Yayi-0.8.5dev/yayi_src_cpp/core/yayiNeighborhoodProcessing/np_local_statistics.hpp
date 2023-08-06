#ifndef YAYI_NEIGHBORHOOD_PROCESSING_LOCAL_STATS_HPP__
#define YAYI_NEIGHBORHOOD_PROCESSING_LOCAL_STATS_HPP__

#include <yayiNeighborhoodProcessing/yayiNeighborhoodProcessing.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace np
  {
    /*!@addtogroup np_grp
     * @{
     */
    using namespace yayi::se;

    //! Computes the mean for each neighborhood specified by se
    YNPro_ yaRC image_local_mean(IImage const* imin, IStructuringElement const* se, IImage* out);

    //! Computes the circular mean and concentration (channel 0) for each neighborhood specified by se
    YNPro_ yaRC image_local_circular_mean_and_concentration(IImage const* imin, IStructuringElement const* se, IImage* out);

    //! Computes the circular mean and concentration (channel 0) lineary weighted by channel 2 for each neighborhood specified by se
    YNPro_ yaRC image_local_weighted_circular_mean_and_concentration(IImage const* imin, IStructuringElement const* se, IImage* out);

    //! Computes the median of each neighborhood
    YNPro_ yaRC image_local_median(IImage const* imin, IStructuringElement const* se, IImage* imout);

    //! @} doxygroup: np_grp
  }
}

#endif /* YAYI_NEIGHBORHOOD_PROCESSING_LOCAL_STATS_HPP__ */
