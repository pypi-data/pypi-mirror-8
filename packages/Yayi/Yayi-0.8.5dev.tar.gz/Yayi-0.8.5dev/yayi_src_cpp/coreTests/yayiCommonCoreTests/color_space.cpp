#include "main.hpp"
#include <yayiCommon/common_colorspace.hpp>

BOOST_AUTO_TEST_SUITE(color_space)

BOOST_AUTO_TEST_CASE(color_space_equality)
{
  using namespace yayi;
  yaColorSpace cs1(yaColorSpace::ecd_rgb), cs2(yaColorSpace::ecd_rgb);
  BOOST_CHECK_EQUAL(cs1, cs2);
  BOOST_CHECK_EQUAL(cs1, cs1);
  BOOST_CHECK_EQUAL(cs2, cs1);
  
  yaColorSpace cs3(yaColorSpace::ecd_rgb, yaColorSpace::ei_d65);
  BOOST_CHECK_NE(cs1, cs3);
  BOOST_CHECK_NE(cs3, cs1);
  BOOST_CHECK_EQUAL(cs3, cs3);
}

BOOST_AUTO_TEST_SUITE_END()


