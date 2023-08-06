#ifndef YAYI_APPLY_TO_IMAGE_BINARY_HPP__
#define YAYI_APPLY_TO_IMAGE_BINARY_HPP__

/*!@file
 * This file defines the binary operators on images.
 */

#include <yayiImageCore/include/ApplyToImage_T.hpp>

namespace yayi
{

  /*!@defgroup binary_pixel_processing_functor_concepts Binary (2-ary) pixel functor
    * @ingroup yayiconcepts
    * @{
    * @par Description
    * A binary pixel functor object is used to perform computations given two arguments representing the values of the two input pixels.
    * There is no other restriction on the concept (particular return value, internal state, constness of arguments).
    *
    * @par Notations
    * Let @c F be the type of the function object, and @c f an instance.
    *
    * @par Requirements
    * A measurement function objects should meet the following requirements:
    * - the @c f function object is a <a href="http://www.sgi.com/tech/stl/BinaryFunction.html">binary function object</a>.
    * - the @c F type implements the result_of behaviour.
    * @}
    */


  /*!@defgroup image_op_binary_grp Pixel processors for binary pixel functors
   * @ingroup image_op_grp 
   * @{
   */  


  namespace {
    template <class it1>
    struct s_all1_iterators_random_access :
      boost::is_same<typename std::iterator_traits<it1>::iterator_category, std::random_access_iterator_tag>
    {
    };

    template <class it1, class it2>
    struct s_all2_iterators_random_access :
      mpl::and_<
        boost::is_same<typename std::iterator_traits<it1>::iterator_category, std::random_access_iterator_tag>,
        boost::is_same<typename std::iterator_traits<it2>::iterator_category, std::random_access_iterator_tag>
      >::type
    {
    };

    template <class it1, class it2, class it3>
    struct s_all3_iterators_random_access :
      mpl::and_<
        boost::is_same<typename std::iterator_traits<it1>::iterator_category, std::random_access_iterator_tag>,
        boost::is_same<typename std::iterator_traits<it2>::iterator_category, std::random_access_iterator_tag>,
        boost::is_same<typename std::iterator_traits<it3>::iterator_category, std::random_access_iterator_tag>
      >::type
    {
    };

  }

  //! Binary operator helper
  //! The images structure are different, and the iterators cannot be reused.
  //! The processing is performed until one of the range is exhausted.
  template <class it_strategy /* = iterators_independant_tag*/>
  struct s_apply_op_range<it_strategy, operator_type_binary_no_return>
  {
    template <class op_, class iter1, class iter2, class image1, class image2>
    typename boost::disable_if<
      s_all2_iterators_random_access<iter1, iter2>, 
      yaRC>::type
    operator()(op_& op, iter1 it1, const iter1 it1e, iter2 it2, const iter2 it2e, image1&, image2&)
    {
      for(; it1 != it1e && it2 != it2e; ++it1, ++it2){
        op(*it1, *it2);
      }
      return yaRC_ok;
    }

    template <class op_, class iter1, class iter2, class image1, class image2>
    typename boost::enable_if<
      s_all2_iterators_random_access<iter1, iter2>, 
      yaRC>::type
    operator()(op_& op, iter1 it1, const iter1 it1e, iter2 it2, const iter2 it2e, image1&, image2&)
    {
      for(; it1 < it1e && it2 < it2e; ++it1, ++it2){
        op(*it1, *it2);
      }
      return yaRC_ok;
    }
  };


  //! The images structures are different, and no factorisation of the iterator can be performed.
  //! We iterate over the two images, until one of them ends. 
  template <class it_strategy /* = iterators_independant_tag*/>
  struct s_apply_op_range<it_strategy, operator_type_binary>
  {
  
    //! Template for operators of the type result = op(operand1, operand2) (not necessarilly symetric)
    template <class op_, class iter1, class iter2, class iter3, class image1, class image2, class image3>
    yaRC operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter2 it2, const iter2 it2e, 
      iter3 it3, const iter3 it3e, 
      image1&, image2&, image3&)
    {
      for(; it1 != it1e && it2 != it2e && it3 != it3e; ++it1, ++it2, ++it3){
        *it3 = op(*it1, *it2);
      }
      return yaRC_ok;
    }

  };



  //! Images share the same offset structure
  //! It is hence possible to use one iterator instead of two, if the ranges allow to do so.
  template <>
  struct s_apply_op_range<iterators_same_offset_tag, operator_type_binary_no_return>
  {

    //! Template for operators of the type op(operand1, operand2) (not necessarilly symetric)
    template <class op_, class iter1, class iter2, class image1, class image2>
    typename boost::disable_if<
      s_all2_iterators_random_access<iter1, iter2>, 
      yaRC>::type
    operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter2, const iter2, 
      image1& im1, 
      image2& im2)
    {
      for(; it1 != it1e; ++it1){
        const offset o = it1.Offset();
        op(im1.pixel(o), im2.pixel(o)); //!@todo bench against op(*it1, im2.pixel(o))
      }
      return yaRC_ok;
    }

    template <class op_, class iter1, class iter2, class image1, class image2>
    typename boost::enable_if<
      s_all2_iterators_random_access<iter1, iter2>, 
      yaRC>::type
    operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter2, const iter2, 
      image1& im1, 
      image2& im2)
    {
      for(; it1 < it1e; ++it1)
      {
        const offset o = it1.Offset();
        op(im1.pixel(o), im2.pixel(o)); //!@todo bench against op(*it1, im2.pixel(o))
      }
      return yaRC_ok;
    }
  };

  //! Images share the same offset structure
  //! It is hence possible to use one iterator instead of two, if the ranges allow to do so.
  template <>
  struct s_apply_op_range<iterators_same_offset_tag, operator_type_binary>
  {

    //! Template for operators of the type result = op(operand1, operand2) (not necessarilly symetric)
    template <class op_, class iter1, class iter2, class iter3, class image1, class image2, class image3>
    typename boost::disable_if<
      s_all3_iterators_random_access<iter1, iter2, iter3>, 
      yaRC>::type
    operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter2 , const iter2 , 
      iter3 , const iter3 , 
      image1& im1, image2& im2, image3& im3)
    {
      for(; it1 != it1e; ++it1){
        const offset o = it1.Offset();
        im3.pixel(o) = op(im1.pixel(o), im2.pixel(o)); //!@todo bench against op(*it1, im2.pixel(o))
      }
      return yaRC_ok;
    }  

    template <class op_, class iter1, class iter2, class iter3, class image1, class image2, class image3>
    typename boost::enable_if<
      s_all3_iterators_random_access<iter1, iter2, iter3>, 
      yaRC>::type
    operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter2 , const iter2 , 
      iter3 , const iter3 , 
      image1& im1, image2& im2, image3& im3)
    {
      for(; it1 < it1e; ++it1){
        const offset o = it1.Offset();
        im3.pixel(o) = op(im1.pixel(o), im2.pixel(o)); //!@todo bench against op(*it1, im2.pixel(o))
      }
      return yaRC_ok;
    }  

    template <class op_, class iter1, class image1>
    typename boost::enable_if<
      s_all1_iterators_random_access<iter1>,
      yaRC>::type
    operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter1 , const iter1 ,
      iter1 , const iter1 ,
      image1& im1, image1& im2, image1& im3)
    {
      for(; it1 < it1e; ++it1){
        const offset o = it1.Offset();
        im3.pixel(o) = op(im1.pixel(o), im2.pixel(o)); //!@todo bench against op(*it1, im2.pixel(o))
      }
      return yaRC_ok;
    }  


  };
  
  //! Images share the same offset structure
  //! It is hence possible to use one iterator instead of two, if the ranges allow to do so.
  template <>
  struct s_apply_op_range<iterators_same_offset_shifted_tag, operator_type_binary_no_return>
  {

    //! Template for operators of the type op(operand1, operand2) (not necessarilly symetric)
    template <class op_, class iter1, class iter2, class image1, class image2>
    yaRC operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter2 it2, const iter2 it2e, 
      image1& im1, 
      image2& im2)
    {
      if(it1 != it1e && it2 != it2e)
      {
        const offset shift = it2.Offset() - it1.Offset();
        for(; it1 != it1e; ++it1){
          const offset o = it1.Offset();
          op(im1.pixel(o), im2.pixel(o + shift)); //!@todo bench against op(*it1, im2.pixel(o+shift))
        }
      }
      return yaRC_ok;
    }
  };

  //! Images share the same offset structure
  //! It is hence possible to use one iterator instead of two, if the ranges allow to do so.
  template <>
  struct s_apply_op_range<iterators_same_offset_shifted_tag, operator_type_binary>
  {

    //! Template for operators of the type result = op(operand1, operand2) (not necessarilly symetric)
    template <class op_, class iter1, class iter2, class iter3, class image1, class image2, class image3>
    yaRC operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter2 it2, const iter2 it2e, 
      iter3 it3, const iter3 it3e, 
      image1& im1, image2& im2, image3& im3)
    {
      if(it1 != it1e && it2 != it2e && it3 != it3e)
      {
        const offset shift1 = it2.Offset() - it1.Offset();
        const offset shift2 = it3.Offset() - it1.Offset();
        for(; it1 != it1e; ++it1){
          const offset o = it1.Offset();
          im3.pixel(o + shift2) = op(im1.pixel(o), im2.pixel(o + shift1));
        }
      }
      return yaRC_ok;
    }  

  };
  



  //! Specializing of s_apply_op_range for iterators on the same images and same range
  template <>
  struct s_apply_op_range<iterators_same_offset_and_same_images_tag, operator_type_binary_no_return>
  {

    //! Template for operators of the type op(operand1, operand2) (not necessarilly symetric)
    template <class op_, class iter1, class iter2, class image1, class image2>
    typename enable_if<
      typename boost::is_same<
        typename boost::remove_const<image1>::type, 
        typename boost::remove_const<image2>::type
      >::type,
      yaRC>::type 
    operator()(
      op_& op, 
      iter1, iter1, 
      iter2 it2, const iter2 it2e, 
      image1& im1, 
      image2& )
    {
      typedef typename mpl::if_<
        mpl::and_<is_const<image1>, is_const<image2> >,
        typename image2::const_reference,
        typename image2::reference>::type ref_t;
      
      //TODO: We can improve here if the arguments of op are const and small
      for(; it2 != it2e; ++it2){
        ref_t p = *it2;
        op(p, p);
      }
      return yaRC_ok;
    }

    //! Template for operators of the type op(operand1, operand2). 
    //! Should be the other specializing of the class, so triggers an error if called (types image1 and image2 are different in this case)
    template <class op_, class iter1, class iter2, class image1, class image2>
    typename disable_if<
      typename boost::is_same<
        typename boost::remove_const<image1>::type, 
        typename boost::remove_const<image2>::type
      >::type,
      yaRC>::type 
    operator()(op_&, iter1, const iter1, iter2, const iter2, image1&, image2&)
    {
      YAYI_THROW("This function should never be called : the program is ill-formed !");
    }
  };

  //! Specializing of s_apply_op_range for iterators on the same images and same range
  template <>
  struct s_apply_op_range<iterators_same_offset_and_same_images_tag, operator_type_binary>
  {
    //! Template for operators of the type result = op(operand1, operand2) (not necessarilly symetric)
    template <class op_, class iter1, class iter3, class image1, class image2, class image3>
    typename enable_if<
      typename mpl::and_<
        typename boost::is_same<
          typename boost::remove_const<image1>::type, 
          typename boost::remove_const<image2>::type
        >::type,
        typename boost::is_same<
          typename boost::remove_const<image1>::type, 
          typename boost::remove_const<image3>::type
        >::type
      >::type,
      yaRC>::type 
    operator()(op_& op, iter1, iter1, iter1, iter1, iter3 it3, const iter3 it3e, image1&, image2&, image3&)
    {
      // Raffi: leave it3/it3e here, as it constrains the compilation types to more correct combinations
      typedef typename iter3::reference ref_t; // c'était image1::reference, voir si ça ne met pas le bordel
      /*typedef typename mpl::if_<
        is_const<image1>,
        typename image1::const_reference,
        typename image1::reference>::type ref_t;*/
      for(; it3 != it3e; ++it3){
        ref_t p = *it3;
        p = op(p, p);
      }
      return yaRC_ok;
    }

    template <class op_, class iter1, class iter2, class iter3, class image1, class image2, class image3>
    typename disable_if<
      typename mpl::and_<
        typename boost::is_same<
          typename boost::remove_const<image1>::type, 
          typename boost::remove_const<image2>::type
        >::type,
        typename boost::is_same<
          typename boost::remove_const<image1>::type, 
          typename boost::remove_const<image3>::type
        >::type
      >::type,
      yaRC>::type 
    operator()(op_&, iter1, const iter1, iter2, const iter2, iter3, const iter3, image1&, image2&, image3&)
    {
      YAYI_THROW("This function should never be called : the program is ill-formed !");
    }

  };



  /*!@brief Pixel processor for binary pixel operations on images.
   *
   */
  struct s_apply_binary_operator
  {

  private:
    template <class iterator_extractor1_t, class iterator_extractor2_t, class image1, class image2, class op_>
      yaRC apply(image1& im1, image2& im2, op_& op) const
    {
      typedef s_iterator_extractor<iterator_extractor1_t> extractor1_type;
      typedef s_iterator_extractor<iterator_extractor2_t> extractor2_type;
      
      extractor1_type extractor1;
      extractor2_type extractor2;
      
      typedef typename extractor1_type::template result<extractor1_type(image1&)>::type result1_type;
      typedef typename extractor2_type::template result<extractor2_type(image2&)>::type result2_type;
      
      const result1_type iterators1(extractor1(im1));
      const result2_type iterators2(extractor2(im2));
      
      typename result1_type::first_type        it1 = iterators1.first;
      const typename result1_type::second_type it1e= iterators1.second;

      typename result2_type::first_type        it2 = iterators2.first;
      const typename result2_type::second_type it2e= iterators2.second;

      // test the return of op if it exists ??
      typedef typename s_extract_operator_type::template result< 
        op_(
          typename result1_type::first_type::reference, 
          typename result2_type::first_type::reference) >::type range_type_with_potential_return;
      typedef typename s_remove_return<range_type_with_potential_return>::type range_type;
      
      switch(iterator_strategy(im1, im2))
      {
        case eis_window_maximal_same_pointer:
        {
          s_apply_op_range<iterators_same_offset_and_same_images_tag, range_type> op_apply;
          return op_apply(op, it1, it1e, it2, it2e, im1, im2);      
        }
        case eis_same_offset_same_pointer_type:        
        case eis_same_offset:
        {
          s_apply_op_range<iterators_same_offset_tag, range_type> op_apply;
          return op_apply(op, it1, it1e, it2, it2e, im1, im2);          
        }      
        default: 
        {
          s_apply_op_range<iterators_independant_tag, range_type> op_apply;
          return op_apply(op, it1, it1e, it2, it2e, im1, im2);  
        }
    
      }
      
    }

    template <
      class iterator_extractor1_t, class iterator_extractor2_t, class iterator_extractor3_t, 
      class image1, class image2, class image3, 
      class op_>
      yaRC apply(image1& im1, image2& im2, image3& im3, op_& op) const
    {
      //BOOST_STATIC_ASSERT(is_void<typename op_::result_type>::value);
      typedef s_iterator_extractor<iterator_extractor1_t> extractor1_type;
      typedef s_iterator_extractor<iterator_extractor2_t> extractor2_type;
      typedef s_iterator_extractor<iterator_extractor3_t> extractor3_type;
      
      extractor1_type extractor1;
      extractor2_type extractor2;
      extractor3_type extractor3;
            
      typedef typename extractor1_type::template result<extractor1_type(image1&)>::type result1_type;
      typedef typename extractor2_type::template result<extractor2_type(image2&)>::type result2_type;
      typedef typename extractor3_type::template result<extractor3_type(image3&)>::type result3_type;
      
      const result1_type iterators1(extractor1(im1));
      const result2_type iterators2(extractor2(im2));
      const result3_type iterators3(extractor3(im3));
      
      typename result1_type::first_type        it1 = iterators1.first;
      const typename result1_type::second_type it1e= iterators1.second;
      
      typename result2_type::first_type        it2 = iterators2.first;
      const typename result2_type::second_type it2e= iterators2.second;

      typename result3_type::first_type        it3 = iterators3.first;
      const typename result3_type::second_type it3e= iterators3.second;



      // test the return of op if it exists ??
      typedef typename s_extract_operator_type::template result< 
        op_(
          typename result1_type::first_type::reference, 
          typename result2_type::first_type::reference
          ) >::type range_type;

      switch(iterator_strategy(im1, im2, im3))
      {
        case eis_window_maximal_same_pointer:
        {
          s_apply_op_range<iterators_same_offset_and_same_images_tag, range_type> op_apply;
          return op_apply(op, it1, it1e, it2, it2e, it3, it3e, im1, im2, im3);      
        }
        case eis_same_offset_same_pointer_type:        
        case eis_same_offset:
        {
          s_apply_op_range<iterators_same_offset_tag, range_type> op_apply;
          return op_apply(op, it1, it1e, it2, it2e, it3, it3e, im1, im2, im3);          
        }
        
        default: 
        {
          s_apply_op_range<iterators_independant_tag, range_type> op_apply;
          return op_apply(op, it1, it1e, it2, it2e, it3, it3e, im1, im2, im3);  
        }
    
      }
      
    }



  public:
  
    template <class image_in1_t, class image_in2_t, class op_>
    yaRC operator()(image_in1_t& in1, image_in2_t& in2, op_& op) const
    {
      return apply<
        iterator_choice_strategy_non_windowed_tag, 
        iterator_choice_strategy_non_windowed_tag>(in1, in2, op);
    }    
    
    template <class image_in1_t, class image_in2_t, class image_out1_t, class op_>
    yaRC operator()(image_in1_t& in1, image_in2_t& in2, image_out1_t& o, op_& op) const
    {
      return apply<
        iterator_choice_strategy_non_windowed_tag, 
        iterator_choice_strategy_non_windowed_tag,
        iterator_choice_strategy_non_windowed_tag>(in1, in2, o, op);
    }
    
  };


  //!@} //defgroup 


}


#endif /* YAYI_APPLY_TO_IMAGE_BINARY_HPP__ */ 
