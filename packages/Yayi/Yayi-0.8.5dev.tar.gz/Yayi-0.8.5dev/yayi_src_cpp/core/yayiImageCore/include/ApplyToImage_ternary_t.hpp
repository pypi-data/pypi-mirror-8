#ifndef YAYI_APPLY_TO_IMAGE_TERNARY_HPP__
#define YAYI_APPLY_TO_IMAGE_TERNARY_HPP__

/*!@file
 * This file defines the ternary operators on images.
 * @todo: add multithreading
 */

#include <yayiImageCore/include/ApplyToImage_T.hpp>


namespace yayi
{
  /*!
   * @defgroup image_op_ternary_grp Ternary Image Operators 
   * @ingroup image_op_grp 
   * @{
   */  

  //! Ternary operator helper
  //! The images structure is different, and no factorisation of the iterator can be performed.
  //! We iterate over the three images, until one of them ends. 
  template <class it_strategy /* = iterators_independant_tag */>
  struct s_apply_op_range<it_strategy, operator_type_ternary_no_return>
  {
    template <class op_, class iter1, class iter2, class iter3, class image1, class image2, class image3>
    yaRC operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter2 it2, const iter2 it2e, 
      iter3 it3, const iter3 it3e, 
      image1&, image2&, image3&)
    {
      for(; it1 != it1e && it2 != it2e && it3 != it3e; ++it1, ++it2, ++it3){
        op(*it1, *it2, *it3);
      }
      return yaRC_ok;
    }
  };
  
  //! The images structures are different, and no factorisation of the iterator can be performed.
  //! We iterate over the two images, until one of them ends. 
  template <class it_strategy /* = iterators_independant_tag */>
  struct s_apply_op_range<it_strategy, operator_type_ternary>
  {
  
    //! Template for operators of the type result = op(operand1, operand2, operand3) (not necessarilly symetric nor commutative etc.)
    template <class op_, class iter1, class iter2, class iter3, class iter4, class image1, class image2, class image3, class image4>
    yaRC operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter2 it2, const iter2 it2e, 
      iter3 it3, const iter3 it3e, 
      iter4 it4, const iter4 it4e, 
      image1&, image2&, image3&, image4&)
    {
      for(; it1 != it1e && it2 != it2e && it3 != it3e && it4 != it4e; ++it1, ++it2, ++it3, ++it4){
        *it4 = op(*it1, *it2, *it3);
      }
      return yaRC_ok;
    }
  };
  

  template <>
  struct s_apply_op_range<iterators_same_offset_tag, operator_type_ternary_no_return>
  {
    template <class op_, class iter1, class iter2, class iter3, class image1, class image2, class image3>
    yaRC operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter2 it2, const iter2 it2e, 
      iter3 it3, const iter3 it3e, 
      image1& im1, image2& im2, image3& im3)
    {
      for(; it1 != it1e; ++it1){
        const offset o = it1.Offset();
        op(im1.pixel(o), im2.pixel(o), im3.pixel(o));
      }
      return yaRC_ok;
    }
  };

  template <>
  struct s_apply_op_range<iterators_same_offset_tag, operator_type_ternary>
  {
    template <class op_, class iter1, class iter2, class iter3, class iter4, class image1, class image2, class image3, class image4>
    yaRC operator()(
      op_& op, 
      iter1 it1, const iter1 it1e, 
      iter2 , const iter2 , 
      iter3 , const iter3 , 
      iter4 , const iter4 , 
      image1& im1, image2& im2, image3& im3, image4& im4)
    {
      for(; it1 != it1e; ++it1){
        const offset o = it1.Offset();
        im4.pixel(o) = op(im1.pixel(o), im2.pixel(o), im3.pixel(o));
      }
      return yaRC_ok;
    }
  };



  /*! Utility function for operations involving a ternay operator
   *
   */
  struct s_apply_ternary_operator
  {

  private:
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
          typename result2_type::first_type::reference,
          typename result3_type::first_type::reference) >::type range_type_with_potential_return;
      typedef typename s_remove_return<range_type_with_potential_return>::type range_type;

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
    
    

    template <
      class iterator_extractor1_t, class iterator_extractor2_t, class iterator_extractor3_t, class iterator_extractor4_t, 
      class image1, class image2, class image3, class image4, 
      class op_>
      yaRC apply(image1& im1, image2& im2, image3& im3, image4& im4, op_& op) const
    {
      //BOOST_STATIC_ASSERT(is_void<typename op_::result_type>::value);
      typedef s_iterator_extractor<iterator_extractor1_t> extractor1_type;
      typedef s_iterator_extractor<iterator_extractor2_t> extractor2_type;
      typedef s_iterator_extractor<iterator_extractor3_t> extractor3_type;
      typedef s_iterator_extractor<iterator_extractor4_t> extractor4_type;
      
      extractor1_type extractor1;
      extractor2_type extractor2;
      extractor3_type extractor3;
      extractor4_type extractor4;
            
      typedef typename extractor1_type::template result<extractor1_type(image1&)>::type result1_type;
      typedef typename extractor2_type::template result<extractor2_type(image2&)>::type result2_type;
      typedef typename extractor3_type::template result<extractor3_type(image3&)>::type result3_type;
      typedef typename extractor4_type::template result<extractor4_type(image4&)>::type result4_type;
      
      const result1_type iterators1(extractor1(im1));
      const result2_type iterators2(extractor2(im2));
      const result3_type iterators3(extractor3(im3));
      const result4_type iterators4(extractor4(im4));
      
      typename result1_type::first_type        it1 = iterators1.first;
      const typename result1_type::second_type it1e= iterators1.second;
      
      typename result2_type::first_type        it2 = iterators2.first;
      const typename result2_type::second_type it2e= iterators2.second;

      typename result3_type::first_type        it3 = iterators3.first;
      const typename result3_type::second_type it3e= iterators3.second;

      typename result4_type::first_type        it4 = iterators4.first;
      const typename result4_type::second_type it4e= iterators4.second;

      // test the return of op if it exists ??
      typedef typename s_extract_operator_type::template result< 
        op_(
          typename result1_type::first_type::reference, 
          typename result2_type::first_type::reference,
          typename result3_type::first_type::reference
          ) >::type range_type;

      switch(iterator_strategy(im1, im2, im3, im4))
      {
        case eis_window_maximal_same_pointer:
        {
          s_apply_op_range<iterators_same_offset_and_same_images_tag, range_type> op_apply;
          return op_apply(op, it1, it1e, it2, it2e, it3, it3e, it4, it4e, im1, im2, im3, im4);
        }
        case eis_same_offset_same_pointer_type:        
        case eis_same_offset:
        {
          s_apply_op_range<iterators_same_offset_tag, range_type> op_apply;
          return op_apply(op, it1, it1e, it2, it2e, it3, it3e, it4, it4e, im1, im2, im3, im4);
        }
        default: 
        {
          s_apply_op_range<iterators_independant_tag, range_type> op_apply;
          return op_apply(op, it1, it1e, it2, it2e, it3, it3e, it4, it4e, im1, im2, im3, im4); 
        }
    
      }
      
    }



  public:
  
    template <class image_1_t, class image_2_t, class image_3_t, class op_>
    yaRC operator()(image_1_t& im1, image_2_t& im2, image_3_t& im3, op_& op) const
    {
      return apply<
        iterator_choice_strategy_non_windowed_tag, 
        iterator_choice_strategy_non_windowed_tag,
        iterator_choice_strategy_non_windowed_tag>(im1, im2, im3, op);
    }
      
    template <class image_1_t, class image_2_t, class image_3_t, class image_4_t, class op_>
    yaRC operator()(image_1_t& im1, image_2_t& im2, image_3_t& im3, image_4_t& im4, op_& op) const
    {
      return apply<
        iterator_choice_strategy_non_windowed_tag, 
        iterator_choice_strategy_non_windowed_tag,
        iterator_choice_strategy_non_windowed_tag,
        iterator_choice_strategy_non_windowed_tag>(im1, im2, im3, im4, op);
    }
    
  };

//!@} // defgroup 
}



#endif /* YAYI_APPLY_TO_IMAGE_TERNARY_HPP__ */
