#ifndef YAYI_LABEL_BINARY_WITH_MEASURES_HPP__
#define YAYI_LABEL_BINARY_WITH_MEASURES_HPP__


#include <yayiLabel/yayi_Label.hpp>


namespace yayi
{
  namespace label
  {
    /*!@defgroup label_meas_grp Labelling with measurements
     * @ingroup label_grp 
     * @brief Performs a labelling and computes some measurements on the extracted connected components
     *
     * The functions in this group extract the connected components of the image and compute some 
     * measurements on each of the connected components, in the same time without any additional pass
     * over the input image.
     * @{
     */   
    
    /*!@brief Binary connected components extraction and computation of their area
     * 
     * In this setting, two neighboring pixels are considered as being part of the same connected component
     * if they are both non-black, according to the value type of the input image @c imin (eg. 0 for integers, (0,0,0) for 3
     * channel integer images, ...). 
     * The returned area is an associative map, whose keys are the id of the connected component and whose values are the corresponding area. 
     * 
     * @param[in] imin input image
     * @param[in] se structuring element indicating the neighboring scheme
     * @param[out] imout label image, where each grey value corresponds to a connected component
     * @param[out] areas associative map between the id of the connected component in imout and its area
     *
     * @note Running the function with imout taken as input image should yield the same result.
     */
    YLab_ yaRC image_label_binary_components_with_area(
      const IImage* imin, 
      const se::IStructuringElement* se, 
      IImage* imout, 
      variant& areas);
  
    //! @}
     
  }

}

#endif /* YAYI_LABEL_BINARY_WITH_MEASURES_HPP__ */ 
