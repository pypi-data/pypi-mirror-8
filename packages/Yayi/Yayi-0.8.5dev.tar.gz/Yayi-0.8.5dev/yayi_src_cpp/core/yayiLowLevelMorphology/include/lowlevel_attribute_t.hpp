#ifndef YAYI_LOWLEVEL_ATTRIBUTES_T_HPP__
#define YAYI_LOWLEVEL_ATTRIBUTES_T_HPP__

#include <yayiCommon/common_types.hpp>

/*!@file
 * This file defines attributes suitable for attribute opening/closing
 * @author Thomas Retornaz
 */

namespace yayi
{
  namespace llmm 
  {
    /*!@defgroup attributes_grp Attributes
     * @ingroup llm_details_grp
     *
     * @{
     */      

    /*!@brief Base attribute class.
     * @tparam result_type the attribute type. This type should be default constructible.
     *
     * @note This class is pure virtual.
     */
    template<class image_in, typename result_type>
    struct s_attribute_base
    {
      typedef typename image_in::pixel_type value_type_in;
      typedef result_type value_type_out;
      value_type_out m_value;

      s_attribute_base()
        : m_value()
      {}
      
      virtual ~s_attribute_base(){}

      const value_type_out& getValue() const throw()
      {
        return m_value;
      }

      //! returns true if computeValue can be called with meaningful results
      virtual bool dataIsValid() const = 0;

      template< class Position > // could be coordinate_type and or offset  
      void update(const value_type_in& ,const Position) throw();

      //! precomputes (if possible) the value
      virtual void computeValue() = 0;

      //! Merging operation beetween two attribute, Update m_value and storage data 
      virtual void merge(const s_attribute_base& rhs)
      {
      }
    };



    /*!@brief Attribute area for attribute closing/opening 
     * @see s_attribute_base
     */
    template <class image_in>
    struct s_attribute_Area
      : public s_attribute_base<image_in, offset> //should be signed accumulator_type(offset) ? YUINT64?
    {
      typedef s_attribute_base<image_in, offset> parent_class;
      typedef typename parent_class::value_type_out value_type_out;
      typedef typename parent_class::value_type_in value_type_in;

      s_attribute_Area()
        : parent_class(),localMeasure(0)
      {}

      template< class Position >
      inline void newPoint(const value_type_in&, const Position) throw()
      { 
        localMeasure++;
      }

      void merge(const s_attribute_Area& rhs)
      {
        localMeasure+=rhs.getValue();
      }

      inline bool dataIsValid() const throw() 
      { 
        return true;
      }

      void computeValue() throw()
			{
				this->m_value = localMeasure;
			}

      value_type_out localMeasure;
    };


    //TODO Attribute builded around HyperRectangle (Strain)
    //TODO Should attribute store offsets of visited pixels ? I think its more logical that dedicated structure store them
    //! @} doxygroup: attributes_grp
  }//namespace llmm
}//namespace yayi

#endif /* YAYI_LOWLEVEL_CRITERION_T_HPP__ */
