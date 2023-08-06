#ifndef YAYI_COMMON_MAIN_HPP__
#define YAYI_COMMON_MAIN_HPP__

#include <yayiCommon/common_config.hpp>

#ifdef YAYI_EXPORT_COMMON_
  #define YCom_ MODULE_EXPORT
#else
  #define YCom_ MODULE_IMPORT
#endif

namespace yayi
{
  /*!@defgroup common_grp Common 
   * 
   * @brief Common definitions, functions, types and structures used in oder modules of Yayi.
   *
   * The common group contains definitions that do not depend on images, but are related to algorithms.
   * @{
   */  

  //! Returns the number of processor units, which is used for parallelization of the computings
  YCom_ unsigned int& NbProcessorUnit();

  //! Returns whether the current architecture is little or big endian
  YCom_ extern const bool is_big_endian;

  //! @} //common_grp 

}


#endif

