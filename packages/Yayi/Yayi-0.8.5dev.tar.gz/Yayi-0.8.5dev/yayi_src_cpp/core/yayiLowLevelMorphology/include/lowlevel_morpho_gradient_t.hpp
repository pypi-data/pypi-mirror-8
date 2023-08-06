#ifndef YAYI_LOWLEVEL_MORPHOLOGY_GRADIENT_T_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_GRADIENT_T_HPP__

/*!@file
 *
 */

#include <yayiLowLevelMorphology/lowlevel_erosion_dilation.hpp>
#include <yayiLowLevelMorphology/include/lowlevel_neighborhoodProcessing_t.hpp>
#include <yayiLowLevelMorphology/include/lowlevel_neighbor_operators_t.hpp>



namespace yayi { namespace llmm {
/*!
 * @addtogroup llm_details_grp
 *
 *@{
 */

  /*!@brief Template function for generic gradient
   *
   * @author Raffi Enficiaud
   */
  template <class image_in, class se_t, class image_out>
  yaRC gradient_image_t(const image_in& imin, const se_t& se, image_out& imout)
  {
    typedef s_max_minus_min_element_subset<typename image_out::pixel_type> neighbor_operator_t;

    typedef typename neighborhood_processing_strategy<
      typename se_t::se_tag,
      typename neighbor_operator_t::operator_traits>::processor_t processor_t;

    processor_t op_processor;

    neighbor_operator_t op;
    return op_processor(imin, se, op, imout);
  }

  /*!@brief Half superior gradient
   *
   * @author Raffi Enficiaud
   */
  template <class image_in, class se_t, class image_out>
  yaRC gradient_sup_image_t(const image_in& imin, const se_t& se, image_out& imout)
  {
    typedef s_max_minus_center_element_subset<typename image_out::pixel_type> neighbor_operator_t;

    typedef typename neighborhood_processing_strategy<
      typename se_t::se_tag,
      typename neighbor_operator_t::operator_traits>::processor_t processor_t;

    processor_t op_processor;

    neighbor_operator_t op;
    return op_processor.neighbor_op_with_center(imin, se, op, imout);
  }

  /*!@brief Half inferior gradient
   *
   *The half inferior gradient is a gradient on the image using the following definition: given an input and
   * output images, and a neighborhood @f$\mathcal{N}@f$:
   * @f[
   * \forall p \in \mathcal{D}(\mathcal{I}_{in}) \cap \mathcal{D}(\mathcal{I}_{out}),
   *   \mathcal{I}_{out}(p) \leftarrow \mathcal{I}_{in}(p) - \bigwedge_{n \in \mathcal{N}_p} \mathcal{I}_{in}(n)
   * @f]
   * The definitions of the half superior and inferior gradients are given by Beucher @cite beucher_watershed_1990.
   * @see s_center_minus_min_element_subset
   * @see gradient_sup_image_t
   * @author Raffi Enficiaud
   */
  template <class image_in, class se_t, class image_out>
  yaRC gradient_inf_image_t(const image_in& imin, const se_t& se, image_out& imout)
  {
    typedef s_center_minus_min_element_subset<typename image_out::pixel_type> neighbor_operator_t;

    typedef typename neighborhood_processing_strategy<
      typename se_t::se_tag,
      typename neighbor_operator_t::operator_traits>::processor_t processor_t;

    processor_t op_processor;

    neighbor_operator_t op;
    return op_processor.neighbor_op_with_center(imin, se, op, imout);
  }
  //! @} doxygroup: llm_details_grp
}}

#endif /* YAYI_LOWLEVEL_MORPHOLOGY_GRADIENT_T_HPP__ */
