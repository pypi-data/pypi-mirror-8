#ifndef YAYI_NEIGHBORHOODPROCESSING_MAIN_HPP__
#define YAYI_NEIGHBORHOODPROCESSING_MAIN_HPP__



#include <yayiCommon/common_config.hpp>


#ifdef YAYI_EXPORT_NeighborhoodProcessing_
#define YNPro_ MODULE_EXPORT
#else
#define YNPro_ MODULE_IMPORT
#endif


namespace yayi
{
  /*!@brief Definitions of neighborhood operations on images
   *
   */
  namespace np
  {
    /*!@defgroup np_grp Neighborhood computations
     * @brief (non-morphological) Operations on neighborhoods (mean/median filters, color filters,...)
     *
     *
     */

    /*!@defgroup np_details_grp Neighborhood computations details
     * @ingroup np_grp
     * @brief
     */



  }
}


#endif /* YAYI_NEIGHBORHOODPROCESSING_MAIN_HPP__ */

