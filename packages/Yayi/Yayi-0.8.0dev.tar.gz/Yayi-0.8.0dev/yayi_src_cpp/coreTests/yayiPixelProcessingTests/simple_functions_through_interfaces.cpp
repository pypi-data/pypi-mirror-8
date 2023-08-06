

#include "main.hpp"

#include <yayiPixelProcessing/image_constant.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiPixelProcessing/include/image_constant_T.hpp>

#include <iostream>



struct fixture_image_unary_interface
{
  typedef yayi::Image<yayi::yaUINT8> image_t;
  typedef yayi::Image<yayi::yaF_simple, yayi::s_coordinate<3> > image_3f_t;

  image_t im;
  image_3f_t im3D;
  
  fixture_image_unary_interface()
  {
    using namespace yayi;
    BOOST_REQUIRE_EQUAL(im.SetSize(c2D(10, 20)), yaRC_ok);
    BOOST_REQUIRE_EQUAL(im.AllocateImage(), yaRC_ok);
    BOOST_REQUIRE(im.IsAllocated());
    
    BOOST_REQUIRE_EQUAL(im3D.SetSize(c3D(50, 40, 30)), yaRC_ok);
    BOOST_REQUIRE_EQUAL(im3D.AllocateImage(), yaRC_ok);
    BOOST_REQUIRE(im3D.IsAllocated());
  }
};

BOOST_FIXTURE_TEST_SUITE(interface_tests, fixture_image_unary_interface)  


  
BOOST_AUTO_TEST_CASE(set_constant)
{
  using namespace yayi;
  int i = 0;
  for(image_t::iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it, i++) {
    *it = i;
    BOOST_CHECK_MESSAGE(im.pixel(i) == i, "failure with *it = i at pixel " << i << " : it = " << (int)(*it));
  }
  BOOST_CHECK_MESSAGE(i == 200, "The number of points " << i << " is different from the number of pixels in the image (200)");
    
  yaRC res = constant((yaUINT8)11, &im);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Return of constant shows an error : " << "\n\t\"" << res << "\"");

  i = 0;
  for(image_t::iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it, i++) {
    BOOST_CHECK_MESSAGE(im.pixel(i) == 11, "failure with *it = i at pixel " << i << " : it = " << (int)(*it));
  }
  BOOST_CHECK_MESSAGE(i == 200, "The number of points " << i << " is different from the number of pixels in the image (200)");
    
    
}

BOOST_AUTO_TEST_CASE(set_constant2)
{
  using namespace yayi;
  
  int i = 0;
  for(image_3f_t::iterator it = im3D.begin_block(), ite = im3D.end_block(); it != ite; ++it, i++) {
    *it = image_3f_t::pixel_type(i);
    BOOST_CHECK_MESSAGE(im3D.pixel(i) == i, "failure with *it = i at pixel " << i << " : it = " << (int)(*it));
  }
  BOOST_CHECK_MESSAGE(i == 50*40*30, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");
    
  yaRC res = constant(0.3f, &im3D);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Return of constant shows an error : " << "\n\t\"" << res << "\"");

  i = 0;
  for(image_3f_t::iterator it = im3D.begin_block(), ite = im3D.end_block(); it != ite; ++it, i++) {
    BOOST_CHECK_MESSAGE(std::abs(im3D.pixel(i) - 0.3f) < 1E-10, "failure with *it = i at pixel " << i << " : it = " << (int)(*it));
  }
  BOOST_CHECK_MESSAGE(i == 50*40*30, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");
    
    
}

BOOST_AUTO_TEST_SUITE_END()  

