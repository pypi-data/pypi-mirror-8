#ifndef YAYI_CURRENT_CONFIGURATION_HPP__
#define YAYI_CURRENT_CONFIGURATION_HPP__


/*!@file
 * Contains utilities for retrieving the current build version the source were built against.
 * @author Raffi Enficiaud
 */


#include <yayiCommon/yayiCommon.hpp>
#include <ctime>
#include <string>


namespace yayi
{
  /*!@defgroup common_svn_grp Retrieve the repository configuration
   * @ingroup common_grp
   * @{
   */
   
  //! Returns the current revision
  YCom_ std::string current_build_version();


  //! Returns the date of the last change for the current revision
  YCom_ struct tm current_build_date();
  //! @} //common_svn_grp
}



#endif

