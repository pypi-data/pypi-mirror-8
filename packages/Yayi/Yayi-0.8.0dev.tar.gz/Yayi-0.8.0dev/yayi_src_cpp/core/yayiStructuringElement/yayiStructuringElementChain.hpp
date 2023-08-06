#ifndef YAYI_STRUCTURING_ELEMENT_CHAIN_HPP__
#define YAYI_STRUCTURING_ELEMENT_CHAIN_HPP__

/*!@file
 * Defines the chained structuring elements
 *
 * @author Raffi Enficiaud
 */

#include <yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi {
  namespace se {
 /*!
  * @defgroup se_chained_grp Structuring Element Chained
  * @ingroup se_grp 
  * @{
  */    
    class StructuringElementChained : public IStructuringElement {
      
      std::vector<IStructuringElement*> internal_se;
    
    public:
      virtual ~StructuringElementChained(){}

      //! Returns a new structuring element that is a transposed copy of this one
      virtual IStructuringElement* Transpose() const {
        StructuringElementChained* out = new StructuringElementChained();
        for(unsigned int i = 0; i < internal_se; i++) {
          out->internal_se.push_back(internal_se[i]->Transpose());
        }
        return out;
      }

      //! Returns the runtime type of the structuring element (see @ref structuring_element_type)
      virtual structuring_element_type getType() const
      {
        return e_set_chain;
      }
      
      //! Returns the size of the structuring element in number of neighbors (the center, of marked, is included)
      virtual unsigned int getSize() const {
        return 0;
      }
      
    };
//! @} // se_chained_grp       
  }
}




#endif /* YAYI_STRUCTURING_ELEMENT_CHAIN_HPP__ */

