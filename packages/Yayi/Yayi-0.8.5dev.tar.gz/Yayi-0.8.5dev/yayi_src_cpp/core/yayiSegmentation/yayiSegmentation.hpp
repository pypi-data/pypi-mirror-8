#ifndef YAYI_SEGMENTATION_MAIN_HPP__
#define YAYI_SEGMENTATION_MAIN_HPP__

/*!@file
 * Main header for the segmentation module
 *
 */

#include <yayiCommon/common_config.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

#ifdef YAYI_EXPORT_SEGMENTATION_
#define YSeg_ MODULE_EXPORT
#else
#define YSeg_ MODULE_IMPORT
#endif


namespace yayi
{

  namespace segmentation
  {
 /*!
  * @defgroup seg_grp Segmentation
  *
  * @{
  */
  
    //! Performs the watershed transform of the input imin map into the output imout
    YSeg_ yaRC isotropic_watershed(const IImage * imin, const se::IStructuringElement* se, IImage* imout);

    //! Performs the watershed transform of the input imin map into the output imout, starting from the seeds defined in imseeds
    YSeg_ yaRC isotropic_watershed(const IImage * imin, const IImage* imseeds, const se::IStructuringElement* se, IImage* imout);
//! @} // seg_grp
  
  }
}


#endif /* YAYI_SEGMENTATION_MAIN_HPP__ */
