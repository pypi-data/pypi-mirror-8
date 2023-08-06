
#include <iostream>
#include <yayiCommon/common_errors.hpp>
#include <yayiCommon/include/common_types_T.hpp>

#ifndef NDEBUG
  #if defined(__APPLE__) || defined(__unix__)
    // demangle GCC
    #include <cxxabi.h>
  #endif
#endif

namespace yayi
{




	namespace errors
	{

    // default logger getter
    struct default_stderr_error_stream_getter : error_stream_getter
    {
      virtual std::ostream& get()
      {
        return std::cerr;
      }
    };
    static default_stderr_error_stream_getter default_error_stream_handler = default_stderr_error_stream_getter();
		static error_stream_getter *yayi_error_stream_current = &default_error_stream_handler;

		std::ostream& yayi_error_stream()
		{
			return yayi_error_stream_current->get();
		}
    
    error_stream_getter* set_error_stream_getter(error_stream_getter* new_stream)
    {
      std::swap(yayi_error_stream_current, new_stream);
      return new_stream;
    }
    
    #ifndef NDEBUG
         
    #if defined(__APPLE__) || defined(__unix__)
    string_type demangle(const char* name)
    {
      // need to demangle C++ symbols
      std::size_t len; 
      int         stat;
      char* realname = __cxxabiv1::__cxa_demangle(name,NULL,&len,&stat);
      
      if (realname != NULL)
      {
        std::string out(realname);
        std::free(realname);
        return out;
      }
      return name;
    }
    
    #elif defined(_WIN32) && defined(_MSC_VER)

    // on visual
    //extern "C" char * _unDName(char * outputString, const char * name, int maxStringLength, void * (* pAlloc )(size_t), void (* pFree )(void *), unsigned short disableFlags);
    
    string_type demangle(const char* name) 
    {
      return name;
      // not needed, already demangled
#if 0
      char * const pTmpUndName = _unDName(0, name, 0, malloc, free, 0); // last '0' for complete information
      if (pTmpUndName) 
      {
        std::string out(pTmpUndName);
        free(pTmpUndName);
        return out;
      }
      return name;
#endif
    }
    #endif
    
    #else
    string_type demangle(const char* name)
    {
      return name;
    }
    
    #endif
		


	}
}


