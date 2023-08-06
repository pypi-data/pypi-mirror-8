#ifndef YAYI_COMMON_TYPES_HPP__
#define YAYI_COMMON_TYPES_HPP__


/*!@file
 * @brief Common types used across the library
 *
 */

#include <string>
#include <ios>
#include <sstream>
#include <boost/cstdint.hpp>


#include <yayiCommon/yayiCommon.hpp>

#ifdef YAYI_ERROR_FOR_UNSET_PIXELS
#pragma message(" -- unset pixel access detection activated")
#endif


namespace yayi
{
  /*!@defgroup general_grp General definitions
   * @brief Group containing definition of various objects (constants, classes, enumerations
   * typedef...) used accross the library
   * @ingroup common_grp
   * @{
   */

  typedef bool                    yaBool;                                     //!< Classical boolean

  typedef unsigned char           yaUINT8;                                    //!< 8bits unsigned integer
  typedef signed char             yaINT8;                                     //!< 8bits signed integer

  typedef unsigned short int      yaUINT16;                                   //!< 16bits unsigned integer
  typedef signed short int        yaINT16;                                    //!< 16bits signed integer

  typedef boost::uint32_t         yaUINT32;                                   //!< 32bits unsigned integer
  typedef boost::int32_t          yaINT32;                                    //!< 32bits signed integer

  typedef float                   yaF_simple;                                 //!< Floating point, simple precision
  typedef double                  yaF_double;                                 //!< Floating point, double precision

#ifdef _WIN32
  typedef __int64                 yaINT64;                                    //!< 64bits unsigned integer
  typedef unsigned __int64        yaUINT64;                                   //!< 64bits signed integer
#else
  typedef long long int           yaINT64;                                    //!< 64bits unsigned integer
  typedef unsigned long long int  yaUINT64;                                   //!< 64bits signed integer
#endif

  typedef yaINT32                 scalar_coordinate;                          //!< Type used to store coordinates on the pixel grid.
  typedef yaF_simple              scalar_real_coordinate;                     //!< Type used to represent any coordinate (not only on the pixel grid).

#ifdef YAYI_64BITS
  typedef yaINT64                 offset;                                     //!< The type used to encode offsets (generally used for accessing pixels)
#else
  typedef yaINT32                 offset;                                     //!< The type used to encode offsets (generally used for accessing pixels)
#endif

  typedef std::string             string_type;                                //!< String type
  typedef std::wstring            wide_string_type;                           //!< @deprecated Wide string type

  struct s_any_type;              // Forward declaration
  typedef s_any_type              variant;                                    //!< The main variant type


  typedef bool (*order_function_type)(const variant&, const variant&);        //!< @deprecated Generic order function type (not used)



  /*!@brief Type description structure.
   * This type describes the type of the data stored in a @ref variant structure. To describe a type, a compound
   * and scalar enum are used:
   * - The compound enum describes the main type of the data, which means its global organisation (scalar,
   *   collection, pixel, coordinate, image structuring element, ...)
   * - The scalar enum describes, when applicable, the subtype of the data. For scalar or homogeneous aggregation of fields
   *   the scalar data type encodes the width of the fields.
   *
   * For instance, to a 3 channel pixel, where each channel is encoded as a double precision float, will be assigned a compound
   * type @ref c_3 and a scalar type @ref s_double.
   * @anchor type
   */
  struct s_type_description
  {
    //! The scalar definition
    typedef enum e_scalar_type
    {
      s_undefined,                                                //!< Undefined subtype
      s_bool,                                                     //!< Boolean
      s_ui8,                                                      //!< 8 bits unsigned integer
      s_ui16,                                                     //!< 16 bits unsigned integer
      s_ui32,                                                     //!< 32 bits unsigned integer
      s_ui64,                                                     //!< 64 bits unsigned integer
      s_i8,                                                       //!< 8 bits signed integer
      s_i16,                                                      //!< 16 bits signed integer
      s_i32,                                                      //!< 32 bits signed integer
      s_i64,                                                      //!< 64 bits signed integer
      s_float,                                                    //!< Simple precision float
      s_double,                                                   //!< Double precision float
      s_object,                                                   //!< Object type
      s_variant,                                                  //!< Variant type (for nested variants)
      s_string,                                                   //!< String type
      s_wstring,                                                  //!< Wide string type (barely used)
      s_image,                                                    //!< Image type
      s_order_function                                            //!< Order function (not used)
    } scalar_type;

    //! Major type of the data
    typedef enum e_compound_type
    {
      c_unknown,                                                  //!< An unknown type
      c_generic,                                                  //!< A "generic" type (not used)
      c_variant,                                                  //!< An unknown variant type
      c_image,                                                    //!< An image type
      c_iterator,                                                 //!< An iterator over a container
      c_coordinate,                                               //!< A coordinate type
      c_scalar,                                                   //!< A scalar type
      c_complex,                                                  //!< A complex type
      c_3,                                                        //!< 3 channels pixel type
      c_4,                                                        //!< 4 channels pixel type
      c_vector, c_map,                                            //!< stl equivalent
      c_container,                                                //!< generic container
      c_function,                                                 //!< generic function type
      c_structuring_element,                                      //!< structuring element
      c_neighborhood                                              //!< a neighborhood
    } compound_type;

    scalar_type         s_type;                                   //!< Scalar definition of the type
    compound_type       c_type;                                   //!< Compound definition of the type

    //! Type equality test
    //! @todo check if we have t == t for unknown type (compound or scalar field).
    bool operator==(const s_type_description& r) const {
      return s_type == r.s_type && c_type == r.c_type;
    }

    //! Type inequality test
    bool operator!=(const s_type_description& r) const {
      return !(*this == r);
    }

    //! Stringifier
    YCom_ operator string_type() const throw();

    //! Type "factory" (from a string)
    YCom_ static s_type_description Create(const string_type&) throw();

    //! Pretty print the type into the output stream.
    friend std::ostream& operator<<(std::ostream& o, const s_type_description& t) {
      o << t.operator string_type(); return o;
    }

    //! Default constructor
    s_type_description() {}

    //! Direct constructor
    s_type_description(compound_type c, scalar_type s) : s_type(s), c_type(c) {}

  };


  //! Alias for s_type_description. Use type instead of s_type_description.
  typedef s_type_description type;

  // Some predefined types
  const static type
    //! The undefined type
    type_undefined(type::c_unknown, type::s_undefined),
    //! scalar unsigned int 8 bit
    type_scalar_uint8(type::c_scalar, type::s_ui8)
  ;







  /*!@brief Return code class offering some functionalities for description
   *
   * Behaves differently according to the YAYI_TRACE_UNCHECKED_ERRORS macro (for debugging purposes).
   * @author Raffi Enficiaud
   */
  struct s_return_code
  {
  public:
    typedef s_return_code   this_type;
    typedef yaINT16         repr_type;
    repr_type               code;

    s_return_code(){}

    s_return_code(repr_type c) :
      code(c)
    {}

    bool operator==(const this_type& r) const throw()
    {
      return code == r.code;
    }

    bool operator!=(const this_type& r) const throw()
    {
      return !this->operator==(r);
    }

    /*!@brief Stringizer operator
     * Returns a string describing the error (if the error is known)
     */
    YCom_ operator string_type() const throw();

    //! Streaming function for return code
    friend std::ostream& operator<< (std::ostream &s, const s_return_code& r)
    {
      s << r.operator string_type(); return s;
    }
  };

  //! Return code type
  typedef s_return_code yaRC;




  /*!@brief Return codes namespace
   * Every error or warning should be described within this namespace
   */
  namespace return_code_constants
  {
    enum e_standard_result
    {
      e_Yr_ok,
      e_Yr_E,
      e_Yr_E_allocation,
      e_Yr_E_already_allocated,
      e_Yr_E_not_allocated,
      e_Yr_E_bad_input_type,
      e_Yr_E_bad_cast,
      e_Yr_E_bad_parameters,
      e_Yr_E_null_pointer,
      e_Yr_E_not_null_pointer,
      e_Yr_E_bad_size,
      e_Yr_E_not_implemented,
      e_Yr_E_file_io_error,
      e_Yr_E_bad_colour,
      e_Yr_E_memory,
      e_Yr_E_overflow,
      e_Yr_E_locked,
      e_Yr_E_unknown
    };

    const s_return_code yaRC_ok                 (e_Yr_ok);                        //!< No error
    const s_return_code yaRC_E_allocation       (e_Yr_E_allocation);              //!< Allocation error
    const s_return_code yaRC_E_already_allocated(e_Yr_E_already_allocated);       //!< The object is already allocated
    const s_return_code yaRC_E_not_allocated    (e_Yr_E_not_allocated);           //!< The object is not allocated
    const s_return_code yaRC_E_not_implemented  (e_Yr_E_not_implemented);         //!< The method is not implemented
    const s_return_code yaRC_E_file_io_error    (e_Yr_E_file_io_error);           //!< An error occured during a file operation
    const s_return_code yaRC_E_bad_parameters   (e_Yr_E_bad_parameters);          //!< Bad parameters provided
    const s_return_code yaRC_E_null_pointer     (e_Yr_E_null_pointer);            //!< A null pointer was given
    const s_return_code yaRC_E_not_null_pointer (e_Yr_E_not_null_pointer);        //!< Indicates a non-null pointer while a null one is expected.
    const s_return_code yaRC_E_unknown          (e_Yr_E_unknown);                 //!< An unknown error occured
    const s_return_code yaRC_E_bad_size         (e_Yr_E_bad_size);
    const s_return_code yaRC_E_memory           (e_Yr_E_memory);
    const s_return_code yaRC_E_overflow         (e_Yr_E_overflow);
    const s_return_code yaRC_E_bad_colour       (e_Yr_E_bad_colour);              //!< Indicates an image of the incorrect color space.
    const s_return_code yaRC_E_locked           (e_Yr_E_locked);                  //!< Indicates that the object has been locked (for reading or writing)

  };

  using namespace return_code_constants;







  //! @} // defgroup general

} // namespace yayi




#endif


