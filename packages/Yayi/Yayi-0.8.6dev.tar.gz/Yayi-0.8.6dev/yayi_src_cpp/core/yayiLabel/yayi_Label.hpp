#ifndef YAYI_LABEL_HPP__
#define YAYI_LABEL_HPP__


#include <yayiCommon/common_config.hpp>

#ifdef YAYI_EXPORT_LABEL_
#define YLab_ MODULE_EXPORT
#else
#define YLab_ MODULE_IMPORT
#endif

#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace label
  {
    /*!@defgroup label_grp Label
     * @brief Labelling part of images. 
     *
     * Labelling exposes functions and classes in order to create partition of images, based on predicates (or relationship between
     * neighboring pixels). 
     * 
     * @{
     */
   
    //! Connected components labelling with a single "id" per connected component in the output image
    YLab_ yaRC image_label(const IImage* imin, const se::IStructuringElement* se, IImage* imout);
    
    //! Returns the offsets of the points of each non-black connected components (no output image)
    YLab_ yaRC image_label_non_black_to_offset(const IImage* imin, const se::IStructuringElement* se, variant &out);
    //! @} //label_grp    
  }

}

#endif /* YAYI_LABEL_HPP__ */ 
