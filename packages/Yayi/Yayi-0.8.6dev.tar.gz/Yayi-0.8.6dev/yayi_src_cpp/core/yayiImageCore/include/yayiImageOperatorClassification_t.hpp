#ifndef YAYI_YAYIIMAGEOPERATORCLASSIFICATION_T_HPP__
#define YAYI_YAYIIMAGEOPERATORCLASSIFICATION_T_HPP__

/*!@file
 * Contains mechanisms to classify the operators applied on images.
 */

#include <boost/function_types/parameter_types.hpp>
#include <boost/function_types/is_member_function_pointer.hpp>
#include <boost/function_types/is_member_object_pointer.hpp>
#include <boost/function_types/member_function_pointer.hpp>
#include <boost/function_types/property_tags.hpp>
#include <boost/function_types/components.hpp>
#include <boost/function_types/result_type.hpp>

#include <boost/mpl/push_front.hpp>

namespace yayi
{
  namespace ns_operator_tag {
  
    /*!@brief The operator tags define some properties of the operators
     *  These properties would allow optimization at run time by splitting (or not) the pixel set into smaller ones,
     *  distributed on different computational units (threads, cpu or machines).
     */
    struct operator_no_tag;
    
    
    /*!@brief This tag means that the underlying operator is insensitive to the order of the points on which it is applied to
     * @f[
     *  T(a_1, a_2, ..., a_n) = T({a_i}_{i \in \N^*_n}) = T(a_2, a_1, ..., a_n) = ...
     * @f]
     */
    struct operator_commutative {};

    /*!@brief The used operator is a "partition set morphism". This means
     *  that the processing can be split into smaller processings, for instance (T stands for the operator, + is the operator 
     *  in the destination monoid):
     * @f[
     * \forall j \in \N^*_n, T(a_1, a_2, ..., a_n) = T(a_1, ..., a_j) + T(a_{j+1}, ..., a_n)
     * @f]
     */
    struct operator_partition_set_morphism;
  
  
    BOOST_MPL_HAS_XXX_TRAIT_NAMED_DEF(has_operator_tag, operator_tag, false);

  
  }




  namespace operator_classification_details
  {
    /*! Returns the result type of a function.
     *  The argument sequence is given as an mpl sequence. This sequence contains both the function type (first element) and the arguments passed to the
     *  function (the other arguments). The purpose is to be able to reconstruct the complete sequence of a function call 
     *  from a sequence @c "<function, arg1, arg2, ...>", the return type being in that case @c "result_of<function(arg1, arg2...)>::type". 
     *  @tparam Seq the sequence of types (return, arguments) of the function
     *  @tparam AR the arity of the function.
     * 
     *  @note there is currently only 3 specialisations on the arity. 
     */
    template <class Seq, int AR = 0>
    struct result_of_helper
    {
      typedef typename boost::result_of<typename boost::mpl::at_c<Seq, 0>::type()>::type type;
    };

    template <class Seq>
    struct result_of_helper<Seq, 1>
    {
      typedef typename boost::result_of<
        typename boost::mpl::at_c<Seq, 0>::type(
          typename boost::mpl::at_c<Seq, 1>::type
        )>::type type;
    };

    template <class Seq>
    struct result_of_helper<Seq, 2>
    {
      typedef typename boost::result_of<
        typename boost::mpl::at_c<Seq, 0>::type(
          typename boost::mpl::at_c<Seq, 1>::type,
          typename boost::mpl::at_c<Seq, 2>::type
        )>::type type;
    };

    /*! Main implementation of the yayi::s_operator_functor_call_const.
     * 
     *  See yayi::s_operator_functor_call_const for details.
     */
    template <class Seq>
    struct s_operator_functor_call_const
    {
      typedef typename boost::mpl::at_c<Seq, 0>::type S_;
      typedef typename result_of_helper<Seq, boost::mpl::size<Seq>::value - 1>::type R_;

      typedef typename mpl::push_front<Seq, R_>::type complete_seq;

      typedef typename
        boost::function_types::member_function_pointer< 
          complete_seq ,
          boost::function_types::const_qualified
        >::type fc_type;

      typedef typename
        boost::function_types::member_function_pointer< 
          complete_seq,
          boost::function_types::non_const
        >::type f_type;

      typedef char                     yes;
      typedef struct { yes array[2]; } no;

      static yes  sfinae2(fc_type f);
      static no   sfinae2(f_type f);

      typedef typename 
        boost::mpl::if_c<
          sizeof(sfinae2(&S_::operator())) == sizeof(yes), 
          boost::true_type, 
          boost::false_type>::type 
        type;
    };


  }

  /*! Determines the constness of a call to operator() of a specific functor.
   * 
   *  The idea is to check if the functor call to operator() leaves the functor unchanged, and guides the multithreading strategy.
   *  @tparam Seq a sequence containing the function object type as first argument, and the argument of the call to its operator().
   */
  template <class Seq>
  struct s_operator_is_functor_call_const : operator_classification_details::s_operator_functor_call_const<Seq>::type
  {
  };




  struct operator_type_zero_ary               {};     //!< No input, but an output (eg. a generator)
  struct operator_type_zero_ary_no_return     {};     //!< No input, no output (eg. a counter)
  
  struct operator_type_unary                  {};     //!< An input and an output (eg. a transformer)
  struct operator_type_unary_no_return        {};     //!< An input but not output (eg. an applyier)
  
  struct operator_type_binary                 {};     //!< Tag for binary operators with return
  struct operator_type_binary_no_return       {};     //!< Tag for binary operators without return

  struct operator_type_ternary                {};     //!< Tag for ternary operators with return
  struct operator_type_ternary_no_return      {};     //!< Tag for ternary operators without return

  struct operator_type_fourary                {};     //!< Tag for 4-ary operators with return
  struct operator_type_fourary_no_return      {};     //!< Tag for 4-ary operators without return

  BOOST_MPL_HAS_XXX_TRAIT_NAMED_DEF(operator_has_result_member_tag, result, false);

  
  namespace
  {
  
    /*! Operator transforming an image operator with return to its corresponding operator without return.
     *
     * This is used to limit the number of cases of compilation-time dispatching
     */
    template <class T> struct s_remove_return                   {typedef T type;};
    
    template <> struct s_remove_return<operator_type_zero_ary>  {typedef operator_type_zero_ary_no_return type; };
    template <> struct s_remove_return<operator_type_unary>     {typedef operator_type_unary_no_return type;    };
    template <> struct s_remove_return<operator_type_binary>    {typedef operator_type_binary_no_return type;   };
    template <> struct s_remove_return<operator_type_ternary>   {typedef operator_type_ternary_no_return type;  };
    template <> struct s_remove_return<operator_type_fourary>   {typedef operator_type_fourary_no_return type;  };
  
  }
  
  

  /*!@brief Utility structure for extracting the type of the supplied operator
   *
   * @author Raffi Enficiaud
   */
  struct s_extract_operator_type
  {
    template <class op_> struct result;
    
    // Revoir l'utilité de cette fonction ici. Grosso modo: on ne cherche pas à savoir le nombre de paramètres avec lequel
    // on appelle cette fonction, mais plutôt de connaitre le type de la fonction.
    template <class op_> 
    struct result< op_() > {
      typedef typename boost::result_of< op_() >::type result_type;
      typedef typename mpl::if_<
        typename is_void<result_type>::type, 
        operator_type_zero_ary_no_return, 
        operator_type_zero_ary>::type type;
    };

    template <class op_, class T> 
    struct result< op_(T) > {
      typedef typename boost::result_of< op_(T) >::type result_type;
      typedef typename mpl::if_<
        typename is_void<result_type>::type, 
        operator_type_unary_no_return, 
        operator_type_unary>::type type;
    };

    template <class op_, class T, class U> 
    struct result< op_(T, U)> {
      typedef typename boost::result_of< op_(T, U) >::type result_type;
      typedef typename mpl::if_<
        typename is_void<result_type>::type, 
        operator_type_binary_no_return, 
        operator_type_binary>::type type;
    };

    template <class op_, class T, class U, class V> 
    struct result< op_(T, U, V)> {
      typedef typename boost::result_of< op_(T, U, V) >::type result_type;
      typedef typename mpl::if_<
        typename is_void<result_type>::type, 
        operator_type_ternary_no_return, 
        operator_type_ternary>::type type;
    };

    template <class op_, class T, class U, class V, class W> 
    struct result< op_(T, U, V, W)> {
      typedef typename boost::result_of< op_(T, U, V, W) >::type result_type;
      typedef typename mpl::if_<
        typename is_void<result_type>::type, 
        operator_type_fourary_no_return, 
        operator_type_fourary>::type type;
    };

  };
  
  //!@todo check if this thing is used.
  typedef s_extract_operator_type operator_traits;
  
  
  
}


#endif /* YAYI_YAYIIMAGEOPERATORCLASSIFICATION_T_HPP__ */

