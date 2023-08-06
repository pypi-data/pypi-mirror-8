#ifndef YAYI_LOWLEVEL_MORPHOLOGY_NEIGHBOR_PROC_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_NEIGHBOR_PROC_HPP__

/*!@file
 * This file defines several operators for neighborhood processing.
 * The following processing methods are implemented:
 * - generic algorithm
 * 
 */

#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>
#include <algorithm>

namespace yayi { namespace llmm {
/*!
 * @addtogroup llm_details_grp
 *
 *@{
 */  

  /*!@brief This class defines a generic process on the neighborhoods of an image
   *
   * The neighborhood is centered at each point of the image, without using any redundancy between two successive neighborhood.
   * Only two functionalities of the neighborhoods are used: centering and iteration. This neighbor processor is hence applicable
   * on the most general neighborhood/se concept.
   *
   * @author Raffi Enficiaud
   */
  struct s_generic_processor {
  

#if 0
    template <class image_t, class se_t, class op_t>
    yaRC operator()(const image_t& im, const se_t& se, op_t& op) {
    
      typedef se::s_runtime_neighborhood<image_t const, se_t> neighborhood_t; // to be delegated to another structure
      
      neighborhood_t neighbor(im, se);
    
      for(typename image_t::const_iterator it(im.begin()), ite(im.end()); it != ite; ++it) {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(it);
        #endif
        
        op(neighbor.begin(), neighbor.end());
      }
      
      return yaRC_ok;
    }
#endif
    
    /*! Processor for operators returning void (computation over the neighborhoods)
     */
    template <class image_t, class se_t, class op_t>
    yaRC operator()(image_t& im, const se_t& se, op_t& op) {

      typedef typename mpl::if_<boost::is_const<image_t>, typename image_t::const_iterator, typename image_t::iterator>::type image_iterator_t;
      typedef se::s_runtime_neighborhood<image_t, se_t> neighborhood_t;// to be delegated to another structure
      
      neighborhood_t neighbor(im, se);
    
      for(image_iterator_t it(im.begin()), ite(im.end()); it != ite; ++it) {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(it);
        #endif
        
        op(neighbor.begin(), neighbor.end());
      }
      
      return yaRC_ok;
    }


    /*! Processor for operators with returning value (computation over the neighborhoods)
     *  This processor is aimed at simulating the Minkowski subtraction
     */
    template <class image_in_t, class se_t, class op_t, class image_out_t>
    yaRC operator()(const image_in_t& im, const se_t& se, op_t& op, image_out_t& imout) {
    
      typedef se::s_runtime_neighborhood<image_in_t const, se_t> neighborhood_t;// to be delegated to another structure
      
      neighborhood_t neighbor(im, se);
      typename image_in_t::const_iterator it(im.begin_block()), ite(im.end_block());
      typename image_out_t::iterator ito(imout.begin_block()), itoe(imout.end_block());
      
      // here check the size of the blocks and use only one iterator if possible
      for(; it != ite && ito != itoe; ++it, ++ito) {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(it);
        #endif
        
        *ito = op(neighbor.begin(), neighbor.end());
      }
      
      return yaRC_ok;
    }



    /*! Neighborhood processor with the center value
     *  The operator should model a ternary functor, with a return value.
     *  This is used for instance for inf-sup half morphological gradients.
     */
    template <class image_in_t, class se_t, class op_t, class image_out_t>
    yaRC neighbor_op_with_center(const image_in_t& im, const se_t& se, op_t& op, image_out_t& imout) {
    
      typedef se::s_runtime_neighborhood<image_in_t const, se_t> neighborhood_t;// to be delegated to another structure
      
      neighborhood_t neighbor(im, se);
      typename image_in_t::const_iterator it(im.begin_block()), ite(im.end_block());
      typename image_out_t::iterator ito(imout.begin_block()), itoe(imout.end_block());
      
      // here check the size of the blocks and use only one iterator if possible
      for(; it != ite && ito != itoe; ++it, ++ito) {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(it);
        #endif
        
        *ito = op(neighbor.begin(), neighbor.end(), *it);
      }

      return yaRC_ok;
    }



    /*! Processor for operators with returning value (computation over the neighborhoods)
     *  This processor is aimed at simulating the Minkowski subtraction/addition. 
     *  op_t should be a model of ternary functor. Its return value is ignored.
     *  We cannot remove the center directly in this function. In case op is a idempotent operator,
     *  the center of the structuring element can be safely removed by the caller. 
     */
    template <class se_t, class op_t, class image_out_t>
    yaRC neighbor_op_with_center_to_neighborhood(const se_t& se, op_t& op, image_out_t& imout) {
    
      typedef se::s_runtime_neighborhood<image_out_t, se_t> neighborhood_t;// to be delegated to another structure
      
      neighborhood_t neighbor(imout, se);
      typename image_out_t::iterator ito(imout.begin_block()), itoe(imout.end_block());
      for(; ito != itoe; ++ito) {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(ito) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(ito);
        #endif
        
        op(neighbor.begin(), neighbor.end(), *ito);
      }
           
      return yaRC_ok;
    }


  };
  



  
  /*!@brief This class defines a generic process on the neighborhoods of an image
   *
   * The neighborhood is centered at each point of the image, without using any redundancy between two successive neighborhood.
   * Only two functionalities of the neighborhoods are used: centering and iteration. This neighbor processor is hence applicable
   * on the most general neighborhood/se concept.
   *
   * @author Raffi Enficiaud
   */
  struct s_generic_processor_constant_on_x {
  
  
    /*! Processor for operators returning void (computation over the neighborhoods)
     */
    template <class image_t, class se_t, class op_t>
    yaRC operator()(image_t& im, const se_t& se, op_t& op) {

      typedef typename mpl::if_<boost::is_const<image_t>, typename image_t::const_iterator, typename image_t::iterator>::type image_iterator_t;      
      BOOST_STATIC_ASSERT((boost::is_same<typename image_iterator_t::iterator_category, std::random_access_iterator_tag>::value)); // main iterator should implement random access concept
      

      const offset o1(se.maximum_extension(0, false) + 1), o2(se.maximum_extension(0, true));
      const offset line_size = im.Size()[0];
      const offset to_add = std::max<offset>(0, line_size - o1 - o2);

      typedef se::s_runtime_neighborhood<image_t const, se_t> neighborhood_t;// to be delegated to another structure
      neighborhood_t neighbor(im, se);
      neighbor.set_shift(1); // here we supppose iterator goes on x
      

      typename image_t::const_iterator it(im.begin_block()), ite(im.end_block());
      
      // here check the size of the blocks and use only one iterator if possible
      for(; it < ite;) {

        for(offset o(0); o < o1; o++, ++it)
        {
          #ifndef NDEBUG
          DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
          #else
          neighbor.center(it);
          #endif
          op(neighbor.begin(), neighbor.end());

        }

        DEBUG_ASSERT(it < ite, "Error on adding the main iterator");

        for(offset o(0); o < to_add; o++)
        {
          #ifndef NDEBUG
          DEBUG_ASSERT(neighbor.shift_center() == yaRC_ok, "Error on shifting the SE");
          #else
          neighbor.shift_center();
          #endif
          op(neighbor.begin(), neighbor.end());
        }

        it += to_add;
        DEBUG_ASSERT(it < ite || (it == ite && o2 == 0), "Error on adding the main iterator");

        for(offset o(0); o < o2; o++, ++it)
        {
          #ifndef NDEBUG
          DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
          #else
          neighbor.center(it);
          #endif
          op(neighbor.begin(), neighbor.end());

        }
                
      }
      
      return yaRC_ok;
    }


    /*! Processor for operators with returning value (computation over the neighborhoods)
     *  This processor is aimed at simulating the Minkowski subtraction
     */
    template <class image_in_t, class se_t, class op_t, class image_out_t>
    yaRC operator()(const image_in_t& im, const se_t& se, op_t& op, image_out_t& imout) {
    
      BOOST_STATIC_ASSERT((boost::is_same<typename image_in_t::const_iterator::iterator_category, std::random_access_iterator_tag>::value)); // main iterator should implement random access concept
      BOOST_STATIC_ASSERT((boost::is_same<typename image_out_t::iterator::iterator_category, std::random_access_iterator_tag>::value)); // main iterator should implement random access concept


      YAYI_ASSERT(im.Size() == imout.Size(), "images of different size currently not supported");

      
      typename image_in_t::const_iterator it(im.begin_block()), ite(im.end_block());
      typename image_out_t::iterator ito(imout.begin_block()), itoe(imout.end_block());

      typedef se::s_runtime_neighborhood<image_in_t const, se_t> neighborhood_t;// to be delegated to another structure
      neighborhood_t neighbor(im, se);
      neighbor.set_shift(1); // here we supppose iterator goes on x
      
      const offset o1(se.maximum_extension(0, false) + 1), o2(se.maximum_extension(0, true));
      const offset line_size = im.Size()[0];
      const offset to_add = std::max<offset>(0, line_size - o1 - o2);


      for(offset o(0); o < o1; o++, ++it, ++ito)
      {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(it);
        #endif
        *ito = op(neighbor.begin(), neighbor.end());

      }
      
      // here check the size of the blocks and use only one iterator if possible
      while((it.Offset() + to_add + o1+o2 < ite.Offset()) && (ito.Offset() + to_add + o1+o2 < itoe.Offset())) {

        DEBUG_ASSERT(it < ite, "Error on adding the main iterator");
        DEBUG_ASSERT(ito < itoe, "Error on adding the main iterator");

        for(offset o(0), o_line(ito.Offset()); o < to_add; o++)
        {
          #ifndef NDEBUG
          DEBUG_ASSERT(neighbor.shift_center() == yaRC_ok, "Error on shifting the SE");
          #else
          neighbor.shift_center();
          #endif
          imout.pixel(o+o_line) = op(neighbor.begin(), neighbor.end());
        }

        it += to_add;
        ito += to_add;
        DEBUG_ASSERT(it < ite || (it == ite && o2 == 0), "Error on adding the main iterator");
        DEBUG_ASSERT(ito < itoe || (ito == itoe && o2 == 0), "Error on adding the main iterator");

        for(offset o(0); o < o1+o2; o++, ++it, ++ito)
        {
          #ifndef NDEBUG
          DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
          #else
          neighbor.center(it);
          #endif
          *ito = op(neighbor.begin(), neighbor.end());

        }
                
      }

      for(offset o(0), o_line(ito.Offset()); o < to_add; o++)
      {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.shift_center() == yaRC_ok, "Error on shifting the SE");
        #else
        neighbor.shift_center();
        #endif
        imout.pixel(o+o_line) = op(neighbor.begin(), neighbor.end());
      }
      it += to_add;
      ito += to_add;

      for(offset o(0); o < o2; o++, ++it, ++ito)
      {
        #ifndef NDEBUG
        DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
        #else
        neighbor.center(it);
        #endif
        *ito = op(neighbor.begin(), neighbor.end());

      }
      
      return yaRC_ok;
    }



    /*! Neighborhood processor with the center value
     *  The operator should model a ternary functor, with a return value.
     *  This is used for instance for inf-sup half morphological gradients.
     */
    template <class image_in_t, class se_t, class op_t, class image_out_t>
    yaRC neighbor_op_with_center(const image_in_t& im, const se_t& se, op_t& op, image_out_t& imout) {
    
      BOOST_STATIC_ASSERT((boost::is_same<typename image_in_t::const_iterator::iterator_category, std::random_access_iterator_tag>::value)); // main iterator should implement random access concept
      BOOST_STATIC_ASSERT((boost::is_same<typename image_out_t::iterator::iterator_category, std::random_access_iterator_tag>::value)); // main iterator should implement random access concept


      YAYI_ASSERT(im.Size() == imout.Size(), "images of different size currently not supported");

      
      typename image_in_t::const_iterator it(im.begin_block()), ite(im.end_block());
      typename image_out_t::iterator ito(imout.begin_block()), itoe(imout.end_block());

      typedef se::s_runtime_neighborhood<image_in_t const, se_t> neighborhood_t;// to be delegated to another structure
      neighborhood_t neighbor(im, se);
      neighbor.set_shift(1); // here we supppose iterator goes on x
      
      const offset o1(se.maximum_extension(0, false) + 1), o2(se.maximum_extension(0, true));
      const offset line_size = im.Size()[0];
      const offset to_add = std::max<offset>(0, line_size - o1 - o2);
      
      // here check the size of the blocks and use only one iterator if possible
      for(; it < ite && ito < itoe;) {

        for(offset o(0); o < o1; o++, ++it, ++ito)
        {
          #ifndef NDEBUG
          DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
          #else
          neighbor.center(it);
          #endif
          *ito = op(neighbor.begin(), neighbor.end(), *it);

        }

        DEBUG_ASSERT(it < ite, "Error on adding the main iterator");
        DEBUG_ASSERT(ito < itoe, "Error on adding the main iterator");

        for(offset o(0); o < to_add; o++)
        {
          #ifndef NDEBUG
          DEBUG_ASSERT(neighbor.shift_center() == yaRC_ok, "Error on shifting the SE");
          #else
          neighbor.shift_center();
          #endif
          ito[o] = op(neighbor.begin(), neighbor.end(), it[o]);
        }

        it += to_add;
        ito += to_add;
        DEBUG_ASSERT(it < ite || (it == ite && o2 == 0), "Error on adding the main iterator");
        DEBUG_ASSERT(ito < itoe || (ito == itoe && o2 == 0), "Error on adding the main iterator");

        for(offset o(0); o < o2; o++, ++it, ++ito)
        {
          #ifndef NDEBUG
          DEBUG_ASSERT(neighbor.center(it) == yaRC_ok, "Error on centering the SE");
          #else
          neighbor.center(it);
          #endif
          *ito = op(neighbor.begin(), neighbor.end(), *it);

        }
                
      }



      
      return yaRC_ok;
    }



    /*! Processor for operators with returning value (computation over the neighborhoods)
     *  This processor is aimed at simulating the Minkowski subtraction/addition. 
     *  op_t should be a model of ternary functor. Its return value is ignored.
     *  We cannot remove the center directly in this function. In case op is a idempotent operator,
     *  the center of the structuring element can be safely removed by the caller. 
     */
    template <class se_t, class op_t, class image_out_t>
    yaRC neighbor_op_with_center_to_neighborhood(const se_t& se, op_t& op, image_out_t& imout) {
    
      BOOST_STATIC_ASSERT((boost::is_same<typename image_out_t::iterator::iterator_category, std::random_access_iterator_tag>::value)); // main iterator should implement random access concept

      typename image_out_t::iterator ito(imout.begin_block()), itoe(imout.end_block());

      typedef se::s_runtime_neighborhood<image_out_t, se_t> neighborhood_t;// to be delegated to another structure
      neighborhood_t neighbor(imout, se);
      neighbor.set_shift(1); // here we supppose iterator goes on x
      
      const offset o1(se.maximum_extension(0, false) + 1), o2(se.maximum_extension(0, true));
      const offset line_size = imout.Size()[0];
      const offset to_add = std::max<offset>(0, line_size - o1 - o2);
      
      // here check the size of the blocks and use only one iterator if possible
      for(; ito < itoe;) {

        for(offset o(0); o < o1; o++, ++ito)
        {
          #ifndef NDEBUG
          DEBUG_ASSERT(neighbor.center(ito) == yaRC_ok, "Error on centering the SE");
          #else
          neighbor.center(ito);
          #endif
          op(neighbor.begin(), neighbor.end(), *ito);

        }

        DEBUG_ASSERT(ito < itoe, "Error on adding the main iterator");

        for(offset o(0); o < to_add; o++)
        {
          #ifndef NDEBUG
          DEBUG_ASSERT(neighbor.shift_center() == yaRC_ok, "Error on shifting the SE");
          #else
          neighbor.shift_center();
          #endif
          op(neighbor.begin(), neighbor.end(), ito[o]);
        }

        ito += to_add;
        DEBUG_ASSERT(ito < itoe || (ito == itoe && o2 == 0), "Error on adding the main iterator");

        for(offset o(0); o < o2; o++, ++ito)
        {
          #ifndef NDEBUG
          DEBUG_ASSERT(neighbor.center(ito) == yaRC_ok, "Error on centering the SE");
          #else
          neighbor.center(ito);
          #endif
          op(neighbor.begin(), neighbor.end(), *ito);

        }
                
      }
           
      return yaRC_ok;
    }


  };
     




  /*! Strategy for choosing the best processor depending on the type of the structuring element and the operation to
   *  perform on each neighborhood.
   */
  template <class se_tag, class operator_type>
  struct neighborhood_processing_strategy {
    typedef s_generic_processor processor_t;
  };


  template <class operator_type>
  struct neighborhood_processing_strategy<se::structuring_element::se_tags::structuring_element_no_reshape, operator_type> {
    typedef s_generic_processor_constant_on_x processor_t;
  };

  template <class operator_type>
  struct neighborhood_processing_strategy<se::structuring_element::se_tags::structuring_element_reshape_on_coordinate_no_x, operator_type> {
    typedef s_generic_processor_constant_on_x processor_t;
  };
//! @} doxygroup: llm_details_grp      
}}

#endif /* YAYI_LOWLEVEL_MORPHOLOGY_NEIGHBOR_PROC_HPP__ */
