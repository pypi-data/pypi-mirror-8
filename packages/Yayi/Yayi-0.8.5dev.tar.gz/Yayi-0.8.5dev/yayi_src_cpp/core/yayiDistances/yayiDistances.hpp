#ifndef YAYI_DISTANCES_MAIN_HPP__
#define YAYI_DISTANCES_MAIN_HPP__



#include <yayiCommon/common_config.hpp>


#ifdef YAYI_EXPORT_DISTANCES_
#define YDist_ MODULE_EXPORT
#else
#define YDist_ MODULE_IMPORT
#endif


namespace yayi
{
  namespace distances
  {
    /*!@defgroup distances_grp Distances
     * @brief Spatial or value distance computation.
     *
     * This group defines a set of function that compute distances, either relying on the coordinate space of the image (which we call
     * spatial distances) or on the value space of the image (eg. color distances).
     */

  }
  //! @} //distances_grp
}
#endif /* YAYI_DISTANCES_MAIN_HPP__ */
