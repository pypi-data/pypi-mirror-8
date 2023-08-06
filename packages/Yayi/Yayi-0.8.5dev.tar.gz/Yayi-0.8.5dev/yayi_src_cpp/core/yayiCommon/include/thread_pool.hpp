


//! @file
//! This file contains the thread pool interface
//! @author Raffi Enficiaud

#ifndef YAYI_COMMON_THREAD_POOL_HPP__
#define YAYI_COMMON_THREAD_POOL_HPP__

#include <yayiCommon/common_types.hpp>


namespace yayi
{

  //! Specifies the number of threads in the thread pool
  //! The operation is thread safe
  //! Reducing the number of threads might be blocking the caller, while increasing the number of threads 
  //! should be immediate.
  YCom_ yaRC set_thread_pool_size(int i);

  //! Returns the number of active threads in the thread pool.
  YCom_ std::size_t get_thread_pool_size();
}



#endif /* YAYI_COMMON_THREAD_POOL_HPP__ */