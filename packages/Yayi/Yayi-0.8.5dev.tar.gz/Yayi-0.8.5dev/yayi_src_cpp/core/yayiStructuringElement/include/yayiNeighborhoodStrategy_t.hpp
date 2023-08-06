#ifndef YAYI_NEIGHBOR_STRATEGY_T_HPP__
#define YAYI_NEIGHBOR_STRATEGY_T_HPP__

/*!@file
 * This file contains structures allowing the proper selection of the neighborhood type 
 * in regards to the structuring element type
 * @author Raffi Enficiaud
 */

#include <yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>

namespace yayi
{
  namespace se
  {
/*!
 * @addtogroup se_details_grp
 *
 *@{
 */
  
  
    //! Main template definition. See partial specialisations
    template <class image_t, class se_t>
    struct s_neighborhood_dispatch
    {
      typedef s_runtime_neighborhood<image_t const, se_t> type;
    };
    
//! @} // se_details_grp              
    
  
  
  
  }
}



#endif /*  */
