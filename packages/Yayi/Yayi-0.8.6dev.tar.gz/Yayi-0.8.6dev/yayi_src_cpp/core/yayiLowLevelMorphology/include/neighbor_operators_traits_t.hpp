#ifndef YAYI_LLMM_NEIGHBOR_OPERATORS_TRAITS_T_HPP__
#define YAYI_LLMM_NEIGHBOR_OPERATORS_TRAITS_T_HPP__

/*!@file
 * This file defines the traits for "local" operators (on neighborhoods)
 * These traits should help the neighborhood processor to select the most
 * appropriate neighborhood algorithm
 *
 * @author Raffi Enficiaud
 */

#include <boost/mpl/has_xxx.hpp>
#include <boost/mpl/if.hpp>

namespace yayi
{

  namespace neighborhood_operator_traits
  {
    struct classical_operator {};
    struct shiftable_operator {};
  }

  BOOST_MPL_HAS_XXX_TRAIT_NAMED_DEF(operator_has_neighborhood_traits_member_tag, operator_traits, false);

  template <class S, bool B = false>
  struct s_neighborhood_operator_traits_helper
  {
    typedef neighborhood_operator_traits::classical_operator type;
  };
  template <class S>
  struct s_neighborhood_operator_traits_helper<S, true>
  {
    typedef typename S::operator_traits type;
  };


  template <class S>
  struct s_neighborhood_operator_traits
  {
    typedef typename s_neighborhood_operator_traits_helper<
      S,
      operator_has_neighborhood_traits_member_tag<S>::type::value
      >::type type;
  };
  //! @} // llm_details_grp
}

#endif /* YAYI_LLMM_NEIGHBOR_OPERATORS_TRAITS_T_HPP__ */
