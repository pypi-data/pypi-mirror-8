#ifndef YAYI_NEIGHBORHOOD_PROCESSING_LOCAL_STATS_T_HPP__
#define YAYI_NEIGHBORHOOD_PROCESSING_LOCAL_STATS_T_HPP__


#include <yayiCommon/common_types.hpp>
#include <yayiLowLevelMorphology/include/lowlevel_neighborhoodProcessing_t.hpp>
#include <yayiMeasurements/include/measurements_mean_variance_t.hpp>
#include <yayiMeasurements/include/measurements_quantiles_t.hpp>
#include <yayiNeighborhoodProcessing/include/np_operators_adapters_t.hpp>

namespace yayi
{
  namespace np
  {
    /*!@addtogroup np_details_grp
     * @{
     */

    /*!@brief Mean filter
     *
     * This function computes locally the mean. It hence acts as a mean filter. The "locallity" is encoded in the provided structuring element.
     * Let @f$\mathcal{N}@f$ be the structuring element, the transformation performs:
     * @f[
     * \forall p \in \mathcal{D}(\mathcal{I}_{in}) \cap \mathcal{D}(\mathcal{I}_{out}), \
     *   \mathcal{I}_{out}(p) = \mathds{E}\left(\mathcal{I}_{in}(\mathcal{N}_p)\right)
     * @f]
     * @author Raffi Enficiaud
     */
    template <class image_in_t, class se_t, class image_out_t>
    yaRC image_local_mean_t(image_in_t const& imin, se_t const& se, image_out_t& imout)
    {
      typedef s_operator_adapter_to_neighborhood_op<
        measurements::s_meas_mean<typename image_in_t::pixel_type, typename image_out_t::pixel_type> > neighbor_operator_t;

      typedef typename llmm::neighborhood_processing_strategy<
        typename se_t::se_tag,
        typename neighbor_operator_t::operator_traits>::processor_t processor_t;

      processor_t op_processor;

      neighbor_operator_t op;
      return op_processor(imin, se, op, imout);
    }


    template <class image_in_t, class se_t, class image_out_t>
    yaRC image_local_circular_mean_and_concentration_t(image_in_t const& imin, se_t const& se, image_out_t& imout)
    {
      typedef s_operator_adapter_to_neighborhood_op<
        measurements::s_meas_circular_mean_and_concentration<typename image_in_t::pixel_type> > neighbor_operator_t;

      typedef typename llmm::neighborhood_processing_strategy<
        typename se_t::se_tag,
        typename neighbor_operator_t::operator_traits>::processor_t processor_t;

      processor_t op_processor;

      neighbor_operator_t op;
      return op_processor(imin, se, op, imout);
    }

    template <class image_in_t, class se_t, class image_out_t>
    yaRC image_local_weighted_circular_mean_and_concentration_t(image_in_t const& imin, se_t const& se, image_out_t& imout)
    {
      typedef s_operator_adapter_to_neighborhood_op<
        measurements::s_meas_weighted_circular_mean_and_concentration<typename image_in_t::pixel_type> > neighbor_operator_t;

      typedef typename llmm::neighborhood_processing_strategy<
        typename se_t::se_tag,
        typename neighbor_operator_t::operator_traits>::processor_t processor_t;

      processor_t op_processor;

      neighbor_operator_t op;
      return op_processor(imin, se, op, imout);
    }


    template <class image_in_t, class se_t, class image_out_t>
    yaRC image_local_median_t(image_in_t const& imin, se_t const& se, image_out_t& imout)
    {
      typedef s_operator_adapter_to_neighborhood_op<
        measurements::s_meas_median<typename image_in_t::pixel_type, typename image_out_t::pixel_type> > neighbor_operator_t;

      typedef typename llmm::neighborhood_processing_strategy<
        typename se_t::se_tag,
        typename neighbor_operator_t::operator_traits>::processor_t processor_t;

      processor_t op_processor;

      neighbor_operator_t op;
      return op_processor(imin, se, op, imout);
    }

    //!@}

  }

}


#endif /* YAYI_NEIGHBORHOOD_PROCESSING_LOCAL_STATS_T_HPP__ */
