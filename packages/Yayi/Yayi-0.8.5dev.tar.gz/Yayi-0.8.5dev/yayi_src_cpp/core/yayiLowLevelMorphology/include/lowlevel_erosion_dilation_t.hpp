#ifndef YAYI_LOWLEVEL_MORPHOLOGY_ERODIL_T_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_ERODIL_T_HPP__

#include <yayiLowLevelMorphology/lowlevel_erosion_dilation.hpp>
#include <yayiLowLevelMorphology/include/lowlevel_neighborhoodProcessing_t.hpp>
#include <yayiLowLevelMorphology/include/lowlevel_neighbor_operators_t.hpp>
#include <yayiCommon/common_errors.hpp>
#include <yayiPixelProcessing/include/image_copy_T.hpp>


namespace yayi { namespace llmm {

  /*!@addtogroup llm_details_grp
   *
   *@{
   */

  /*!@brief Erosion (template).
   *
   *
   * @author Raffi Enficiaud
   */
  template <class image_in, class se_t, class image_out>
  yaRC erode_image_t(const image_in& imin, const se_t& se, image_out& imout)
  {
    typedef s_min_element_subset<typename image_in::pixel_type> neighbor_operator_t;

    typedef typename neighborhood_processing_strategy<
      typename se_t::se_tag,
      typename neighbor_operator_t::operator_traits>::processor_t processor_t;

    processor_t op_processor;

    neighbor_operator_t op;
    return op_processor(imin, se, op, imout);
  }

  /*!@brief Dilation (template).
   *
   * @author Raffi Enficiaud
   */
  template <class image_in, class se_t, class image_out>
  yaRC dilate_image_t(const image_in& imin, const se_t& se, image_out& imout)
  {
    typedef s_max_element_subset<typename image_in::pixel_type> neighbor_operator_t;

    typedef typename neighborhood_processing_strategy<
      typename se_t::se_tag,
      typename neighbor_operator_t::operator_traits>::processor_t processor_t;

    processor_t op_processor;

    neighbor_operator_t op;
    return op_processor(imin, se, op, imout);
  }


  /*!@brief Template function for generic Minkowski subtraction.
   * Costs one copy + O(N*S), where N is the number of pixels and S the size of the SE.
   *
   * @author Raffi Enficiaud
   * @anchor minkowski_subtraction_t
   */
  template <class image_in, class se_t, class image_out>
  yaRC minkowski_subtraction_t(const image_in& imin, const se_t& se, image_out& imout)
  {
    typedef s_min_element_to_subset<typename image_out::pixel_type> neighbor_operator_t;

    typedef typename neighborhood_processing_strategy<
      typename se_t::se_tag,
      typename s_neighborhood_operator_traits<neighbor_operator_t>::type>::processor_t processor_t;

    processor_t op_processor;
    neighbor_operator_t op;

    yaRC res = copy_image_t(imin, imout);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error during the copy: " << res);
      return res;
    }

    return op_processor.neighbor_op_with_center_to_neighborhood(se, op, imout);
  }

  /*!@brief Template function for generic Minkowski addition.
   * This function has the same cost as the Minkowski subtraction (@ref minkowski_subtraction_t)
   *
   * @author Raffi Enficiaud
   */
  template <class image_in, class se_t, class image_out>
  yaRC minkowski_addition_t(const image_in& imin, const se_t& se, image_out& imout)
  {
    typedef s_max_element_to_subset<typename image_out::pixel_type> neighbor_operator_t;

    typedef typename neighborhood_processing_strategy<
      typename se_t::se_tag,
      typename s_neighborhood_operator_traits<neighbor_operator_t>::type>::processor_t processor_t;

    processor_t op_processor;
    neighbor_operator_t op;

    yaRC res = copy_image_t(imin, imout);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error during the copy: " << res);
      return res;
    }

    return op_processor.neighbor_op_with_center_to_neighborhood(se, op, imout);
  }
//! @} doxygroup: llm_details_grp
}}

#endif /* YAYI_LOWLEVEL_MORPHOLOGY_ERODIL_T_HPP__ */
