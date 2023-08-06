#ifndef YAYI_COMMON_TYPES_T_HPP__
#define YAYI_COMMON_TYPES_T_HPP__



#include <boost/mpl/bool.hpp>
#include <boost/type_traits.hpp>
#include <boost/mpl/comparison.hpp>
#include <boost/mpl/sizeof.hpp>
#include <boost/mpl/eval_if.hpp>
#include <boost/mpl/logical.hpp>
#include <boost/mpl/identity.hpp>
#include <boost/numeric/conversion/conversion_traits.hpp>
#include <boost/static_assert.hpp>


#include <yayiCommon/common_types.hpp>
#include <yayiCommon/common_errors.hpp>



namespace yayi
{


  /*!@brief Mechanisms for describing/processing/transforming types at compilation time.
   * @anchor type_description
   */
  namespace type_description
  {

    /*!@defgroup meta_utility_grp Metaprogramming utilities
     * @brief Definitions/classes for manipulating types at compilation time.
     *
     * Since many operators in Yayi do manipulate types, this group of functions/definitions provides
     * some utilities to ease the
     * @ingroup general_grp
     * @{
     */

    /*!@brief Meta-utility class : always throws
     * Utility to prevent the instance creation of the daughter classes.
     *
     * @author Raffi Enficiaud
     */
    template <class T>
    struct s_always_throw
    {
      BOOST_STATIC_ASSERT(sizeof(T) == 0);
      s_always_throw()
      {
        YAYI_THROW("s_always_throw invoked");
      }
    };

    /*!@brief Meta-utility class : never throws
     *
     * This class does nothing particular (to oppose to s_always_throw)
     *
     * @author Raffi Enficiaud
     */
    struct s_never_throw{};


    /*!@brief Meta-utility class for carrying information about a type.
     * @tparam U the described type
     *
     * This class contains the general definitions contained in all specializations (for a given type U).
     * Its purpose is to describe U with enums contained in @ref type, as well as providing a human readable
     * string defining U.
     *
     * In order U to be supported, the specializing should inherit from boost::mpl::true_, otherwise type_desc
     * will generate a compilation-time error.
     *
     * @author Raffi Enficiaud
     */
    template <class U> struct type_support : public boost::mpl::false_
    {
      static const yayi::type::scalar_type scalar     = yayi::type::s_undefined;      //!< The scalar type of U
      static const yayi::type::compound_type compound = yayi::type::c_unknown;        //!< The compound type of U

      //! Returns the human readable name of the type U.
      static const string_type& name() {
        static const string_type s = "";
        return s;
      }
    };


    /*!@brief Utility transforming a template type to a @ref type object instance.
     *
     * @code
     * yayi::type t = to_type< std::map<yaUINT32, std::string> >();
     * @endcode
     * @see type
     */
    template <class T> type to_type() {
      return type(type_support<T>::compound, type_support<T>::scalar);
    }


    /*!@brief Meta-function transforming a combination of compound and scalar type into the correspinding "classical" type.
     *
     * @code
     * typedef from_type<type::c_scalar, type::s_ui8>::type current_type;
     * BOOST_MPL_ASSERT((boost::is_same<current_type, yaUINT8>));
     * @endcode
     *
     * The idea behind is to be able to transform several level of switches:
     * @code
     * // the compound type has already been determined at compilation time
     * template <enum type::compound_type e> my_function(type const& t, IImage* im)
     * {
     *   switch(t.s_type)
     *   {
     *     case type::s_ui8:
     *     {
     *       typedef typename from_type<e, type::s_ui8>::type current_type; // e defined at the instanciation of this function
     *       Image<current_type> *im_t = dynamic_cast< Image<current_type> *>(im);
     *       //...
     *       break;
     *     }
     *   //...
     *   }
     * }
     * @endcode
     * @see type, to_type
     */
    template <enum type::e_compound_type, enum type::e_scalar_type>
    struct from_type;






    /*!@brief Type description and support check
     * @tparam U the type to describe/transform
     *
     * The purpose of this class is to prevent the use of unsupported types in the library. Each new supported type should be enquired by a
     * specializing of this class.
     *
     * The class U should be specialized by a specific @ref type_support
     * @note Any attempt to compile unsupported types generates a compilation-time error (see @ref YAYI_COMPILER_ERROR_FOR_UNSUPPORTED_TYPES__)
     * @author Raffi Enficiaud
     */
    template <class U>
    struct type_desc :
      public boost::mpl::if_<
        typename type_support<U>::type,
        s_never_throw,
        s_always_throw<bool>
      >::type,
      public type_support<U>
    {
#ifdef YAYI_COMPILER_ERROR_FOR_UNSUPPORTED_TYPES__
    private:
      //! The following typedef generates a compiler error for unsupported types instantiation
      typedef typename type_support<U>::support_value_type    generate_error;
#endif

    public:
      //! Compilation boolean indicating U is POD.
      typedef boost::is_pod<U>                                is_pod;

      //! The type U without const/volatile qualifications
      typedef typename boost::remove_cv<U>::type              type_remove_cv;

      //! The type U
      typedef U                                               type;
    };


    //!@brief Returns the types that may be able to encode both types.
    //!@note a poor version of conversion traits contained in boost.
    template <class U, class V> struct s_supertype :
      public boost::mpl::if_<
        typename boost::mpl::and_<
          typename boost::is_scalar<U>::type,
          typename boost::is_scalar<V>::type
          >::type,
        s_always_throw<bool>,
        s_never_throw
        >::type
    {
      typedef typename boost::numeric::conversion_traits<U,V>::supertype type;
    };


    /*!@brief Returns an appropriate representation for summing a sequence of type U
     * @todo have a correct accumulator dependant on the type (eg if types are integer, yaInt64 may be more appropriate)
     * @note the accumulation depends both on the type to be accumulated and the number of elements to accumulate. So this is intrinsically
     *       a bad idea...
     */
    template <typename U>
    struct s_sum_supertype
    {
      typedef yaF_double type;
    };


    //!@} // meta_utility_grp
  } // namespace type_description
} // namespace yayi

#endif /* YAYI_COMMON_TYPES_T_HPP__ */


