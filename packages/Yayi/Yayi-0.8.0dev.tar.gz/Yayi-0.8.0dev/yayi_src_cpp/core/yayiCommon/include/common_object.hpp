#ifndef YAYI_COMMON_OBJECT_HPP__
#define YAYI_COMMON_OBJECT_HPP__

#include <string>
#include <yayiCommon/common_types.hpp>


namespace yayi
{
  /*!
 	* @addtogroup general_grp
 	* @{
 	*/

  /*!@brief Root object for interfaces
   * 
   * @author Raffi Enficiaud
   */
  class IObject
  {
  public:
    
    //! Destructor
    virtual ~IObject(){}

    //! Returns the current type of the object
    virtual type DynamicType() const              = 0;

    //! Object description
    virtual string_type Description() const       = 0;
  };

 	//! @} // general_grp >>to RE ;qy you need a dedicated grp for IOObject /string ....

}
#endif /* YAYI_COMMON_OBJECT_HPP__ */

