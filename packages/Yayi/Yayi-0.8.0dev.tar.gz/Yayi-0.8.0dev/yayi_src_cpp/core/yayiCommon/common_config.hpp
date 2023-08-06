#ifndef YAYI_COMMON_CONFIG__HPP__
#define YAYI_COMMON_CONFIG__HPP__


/*!@file
 * Common configuration definitions. This file should not depend on any other file.
 */

namespace yayi
{

#if defined(_WIN32) || defined(_WIN64)
  #define yayiDeprecated __declspec(deprecated)
  #define yayiDeprecatedM(x) __declspec(deprecated(x))
  
  #if defined(_M_X64) || defined(_WIN64)
    #define YAYI_64BITS
  #endif
  
#else
	#define yayiDeprecated __attribute__((deprecated))
  #define yayiDeprecatedM(x) yayiDeprecated

  #if defined(__LP64__)
    #define YAYI_64BITS
  #endif

#endif


	/*! Should be defined if the modules are intended for dynamic linking
	 */
#ifdef YAYI_DYNAMIC

  // Raffi: too verbose !
  // #pragma message("YAYI_DYNAMIC activated")
	// decorators for dynamic libraries
#	if defined(_WIN32) && defined(_MSC_VER)
#		define MODULE_IMPORT __declspec(dllimport)
#		define MODULE_EXPORT __declspec(dllexport)
# else
#		define MODULE_IMPORT
#		define MODULE_EXPORT
#	endif



	// simple basic check
//#	if defined(_WIN32) || defined(_WIN64)
//#	if !defined(_DLL) && !defined(_SO)
//#		error One of these two macro should be present
//#	endif
//#	endif

#else

	// no decorators for static libraries
#		define MODULE_IMPORT 
#		define MODULE_EXPORT 

#endif

#define PROJECT_NAME__ Yayi


// plateform specific section
#if defined(_WIN32) || defined (_WIN64)
	
#	ifndef _CPPRTTI
#		error You should activate the RTTI for PROJECT_NAME__ to make it run correctly
#	endif

#	ifndef _CPPUNWIND
#		error You should activate the exception handling for PROJECT_NAME__ to make it run correcly
#	endif

#endif



//!@def YAYI_COMPILER_ERROR_FOR_UNSUPPORTED_TYPES__
//! Define this macro to raise a compilation error when trying to instanciate Image classes (or pixels) with types that are unsupported by the variants
#define YAYI_COMPILER_ERROR_FOR_UNSUPPORTED_TYPES__


}


#endif


