#ifndef YAYI_COMMON_ERRORS_HPP__
#define YAYI_COMMON_ERRORS_HPP__

/*!@file
 * @brief Errors and return codes definitions and helpers
 *
 */


#include <string>
#include <ios>
#include <exception>
#include <cassert>

#include <yayiCommon/common_types.hpp>
#include <yayiCommon/include/common_string_utilities.hpp>

namespace yayi
{

  /*!@namespace errors
   * @brief Contains standard error or warning codes
   */
  namespace errors
  {
    /*!@defgroup errors_grp Errors definitions
     * @brief Definition of errors and functions to handle them.
     * @ingroup general_grp
     *
     * This group defines some facilities in order to handle and log the errors. The @c error_stream_getter
     * defines the abstract class for the structure responsible for returning the error stream. The current 
     * instance can be set by @c set_error_stream_getter. The default implementation logs to @c std::cerr.
     * The function @c yayi_error_stream is a shortcut to @c error_stream_getter::get used in the logging macros.
     * @{
     */


    //! Returns the current error/info stream
    YCom_ std::ostream& yayi_error_stream();
    
    //! Type for the error stream getter.
    struct error_stream_getter
    {
      virtual std::ostream& get() = 0;
    };

    //! Sets the current "error stream getter". 
    YCom_ error_stream_getter* set_error_stream_getter(error_stream_getter* );

    /*!@brief Yayi exception class
     *
     * This type of exception is fired within yayi.
     * @author Raffi Enficiaud
     */
    struct yaException : public std::exception
    {
    private:
      string_type   str_desc;

    public:
      //! Constructs an exception from a C string.
      yaException(const char *str) : str_desc(str){}

      //! Constructs an exception from a string.
      yaException(const string_type &error_description) : str_desc(error_description){}

      //! Constructs an exception from a return code
      //! @warning this implies that the code is linked against yayiCommon.
      yaException(const yaRC& r)
      {
        // to branch to an unit compiled function
        str_desc = static_cast<string_type>(r);
      }

      virtual ~yaException() throw() {}

      //! Returns the message carried by the exception
      virtual const char *what( ) const throw() {return str_desc.c_str();}

      //! Returns the message carried by the exception
      const string_type& message() const {return str_desc;}

    };

#define YAYI_DEBUG_MESSAGE(s)\
  std::string("File :\t\t") + std::string(__FILE__) + std::string("\n" \
  "Line :\t\t") + int_to_string(__LINE__) + std::string("\n" \
  "Message :\t") + std::string(s)

#define YAYI_DEBUG_MESSAG_STREAM(s)\
  "File :\t\t"  __FILE__  "\n" \
  "Line :\t\t" << __LINE__ << "\n" \
  "Message :\t" << s

#define YAYI_ERROR_FORMATER(s)\
  std::string("ASSERTION FAILURE !!!\n") + \
  YAYI_DEBUG_MESSAGE(s)

#define YAYI_THROW(s)\
  {yayi::errors::yayi_error_stream() << YAYI_DEBUG_MESSAG_STREAM(s) << std::endl; \
  throw errors::yaException(YAYI_DEBUG_MESSAGE(s));}

#define YAYI_ASSERT(cond, s)\
  if(!(cond)) {YAYI_THROW(s);}


  //!@internal
  //! Utility function to print demangled names
  YCom_ string_type demangle(const char* name);



#ifndef NDEBUG
  //!@brief A variable that is expanded only in debug mode
  #define DEBUG_ONLY_VARIABLE(x)  x
  //!@brief Simple assert (debug only)
  #define DEBUG_ASSERT(cond, s)   {YAYI_ASSERT(cond, s)}
  //!@brief Exception thrown only in debug mode
  #define DEBUG_THROW(s)          {YAYI_THROW(s);}
  //!@brief Indicates that the flagged function/method may throw only in debug mode,
  //! and no exception is thrown otherwise.
  #define YAYI_THROW_DEBUG_ONLY__
  //!@brief "Logs" an information to the error/information stream (as returned by yayi_error_stream()), in debug mode only.
  #define DEBUG_INFO(s)           {errors::yayi_error_stream() << YAYI_DEBUG_MESSAG_STREAM(s) << std::endl;}
#else
  #define DEBUG_ONLY_VARIABLE(x)
  #define DEBUG_ASSERT(cond, s)   {}
  #define DEBUG_THROW(s)          {}
  #define YAYI_THROW_DEBUG_ONLY__ throw()
  #define DEBUG_INFO(s)           {}
#endif


    //! @} //doxygroup: errors_grp

  } // namespace errors
} // namespace yayi


#endif /* YAYI_COMMON_ERRORS_HPP__ */


