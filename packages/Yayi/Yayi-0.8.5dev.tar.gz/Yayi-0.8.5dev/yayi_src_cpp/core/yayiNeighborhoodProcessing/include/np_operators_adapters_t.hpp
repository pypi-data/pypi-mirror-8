#ifndef YAYI_NEIGHBORHOOD_PROCESSING_OPERATORS_ADAPTERS_HPP__
#define YAYI_NEIGHBORHOOD_PROCESSING_OPERATORS_ADAPTERS_HPP__

#include <yayiLowLevelMorphology/include/neighbor_operators_traits_t.hpp>

namespace yayi
{

  namespace np
  {
    /*!@ingroup np_details_grp
     * @{
     */

    /*!@brief Adaptor of a measurement operator for performing measurements on neighborhoods.
     *
     * @tparam op_t an operator of measurements that will be applied locally in the image
     * @tparam op_trait_t the processing tag used to compute the local values
     *
     * @note This version shares an instance of @c op_t over all possible threads (to make it short, it is not possible
     *  to use the current implementation in multithread).
     * @note @c op_t should implement the @ref measurement_functor_concepts concept.
     */
    template <class op_t, class op_trait_t = struct neighborhood_operator_traits::classical_operator>
    struct s_operator_adapter_to_neighborhood_op
    {

      typedef op_trait_t operator_traits;
      typedef typename op_t::result_type result_type;

      op_t op;

      s_operator_adapter_to_neighborhood_op() : op() {}
      s_operator_adapter_to_neighborhood_op(op_t const & op_) : op(op_) {}

      template <class iter_t>
      result_type operator()(iter_t it, iter_t const ite)
      {
        op.clear_result();
        for(; it != ite; ++it)
        {
          op(*it);
        }
        return op.result();
      }

    };

    //!@}

  }
}


#endif /* YAYI_NEIGHBORHOOD_PROCESSING_OPERATORS_ADAPTERS_HPP__ */
