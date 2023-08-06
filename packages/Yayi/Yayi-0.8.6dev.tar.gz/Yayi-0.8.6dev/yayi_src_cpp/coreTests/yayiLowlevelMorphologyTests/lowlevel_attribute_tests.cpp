#include "main.hpp"
#include <yayiLowLevelMorphology/include/lowlevel_attribute_t.hpp>
#include <yayiCommon/common_errors.hpp>
#include <yayiCommon/common_types.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>

BOOST_AUTO_TEST_SUITE(attributes)

BOOST_AUTO_TEST_CASE(construction) 
{
  using namespace yayi;
  using namespace yayi::llmm;

  typedef Image<yayi::yaUINT8> image_type;
  image_type im_in;
  
  //ctor area
  typedef s_attribute_Area<image_type> area;
  area m_area;

  BOOST_CHECK_EQUAL(m_area.getValue(),0);
  m_area.newPoint(10,1);
  m_area.newPoint(12,8);
  m_area.newPoint(15,9);
  m_area.computeValue();
  BOOST_CHECK_EQUAL(m_area.getValue(),3);

  area m_area2;
  BOOST_CHECK_EQUAL(m_area2.getValue(),0);
  m_area2.newPoint(1,1);
  m_area2.newPoint(1,2);
  m_area2.computeValue();
  BOOST_CHECK_EQUAL(m_area2.getValue(),2);

  m_area2.merge(m_area);
  m_area2.computeValue();
  BOOST_CHECK_EQUAL(m_area2.getValue(),5);

}

BOOST_AUTO_TEST_SUITE_END()
