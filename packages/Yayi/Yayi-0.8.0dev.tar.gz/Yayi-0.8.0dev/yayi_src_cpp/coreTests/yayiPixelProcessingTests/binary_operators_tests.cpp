

#include "main.hpp"
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiPixelProcessing/image_copy.hpp>
#include <yayiPixelProcessing/image_arithmetics.hpp>
#include <yayiPixelProcessing/image_channels_process.hpp>


struct fixture_image_binary
{
  typedef yayi::Image<yayi::yaUINT8> image_t;
  typedef yayi::Image<yayi::yaF_simple, yayi::s_coordinate<3> > image_3f_t;

  image_t im, im2;
  image_3f_t im3D, im3D_2;
  
  fixture_image_binary()
  {
    using namespace yayi;
    BOOST_REQUIRE_EQUAL(im.SetSize(c2D(10, 20)), yaRC_ok);
    BOOST_REQUIRE_EQUAL(im.AllocateImage(),yaRC_ok);
    BOOST_REQUIRE(im.IsAllocated());

    BOOST_REQUIRE_EQUAL(im2.SetSize(c2D(10, 20)), yaRC_ok);
    BOOST_REQUIRE_EQUAL(im2.AllocateImage(), yaRC_ok);
    BOOST_REQUIRE(im2.IsAllocated());

    BOOST_REQUIRE_EQUAL(im3D.SetSize(c3D(50, 40, 30)), yaRC_ok);
    BOOST_REQUIRE_EQUAL(im3D.AllocateImage(), yaRC_ok);
    BOOST_REQUIRE(im3D.IsAllocated());
    
    BOOST_REQUIRE_EQUAL(im3D_2.SetSize(c3D(50, 40, 30)), yaRC_ok);
    BOOST_REQUIRE_EQUAL(im3D_2.AllocateImage(), yaRC_ok);
    BOOST_REQUIRE(im3D_2.IsAllocated());  
  }
};

BOOST_FIXTURE_TEST_SUITE(binary_operators, fixture_image_binary)  

  
BOOST_AUTO_TEST_CASE(multiply_constant)
{
  using namespace yayi;
  int i = 0;
  for(image_t::iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it, i++) {
    *it = i % 17;
    BOOST_CHECK_MESSAGE(im.pixel(i) == i % 17, "failure with *it = i at pixel " << i << " : it = " << (int)(*it) << " != " << i % 17);
  }
  BOOST_CHECK_MESSAGE(i == 10*20, "The number of points " << i << " is different from the number of pixels in the image (10*20)");
  
  BOOST_CHECKPOINT("image_binary_interface::test_set_constant - copy");
  yaRC res = yayi::image_multiply_constant(&im, yaUINT8(255), &im);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Return of copy indicates an error : " << "\n\t\"" << res << "\"");

  BOOST_CHECKPOINT("image_binary_interface::test_multiply_constant - check");
  i = 0;
  for(image_t::iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it, i++) {
    BOOST_CHECK_MESSAGE(im.pixel(i) == static_cast<yaUINT8>((i % 17) * 255), "failure with *it = i at pixel " << i << " : it = " << *it << " != " << (int)static_cast<yaUINT8>(i % 17 % 255));
  }
  BOOST_CHECK_MESSAGE(i == 10*20, "The number of points " << i << " is different from the number of pixels in the image (10*20)");
}
  
BOOST_AUTO_TEST_CASE(copy_channel_into_another)
{
  using namespace yayi;
  typedef Image< pixel8u_3 > image_3c;
  
  image_3c imc;
  
  BOOST_REQUIRE(imc.SetSize(c2D(10, 20)) == yaRC_ok);
  BOOST_REQUIRE_MESSAGE(imc.AllocateImage() == yaRC_ok, "Allocate failed with coords : " << c2D(10, 20));

  
  int i = 0;
  for(image_3c::iterator it = imc.begin_block(), ite = imc.end_block(); it != ite; ++it, i++) {
    *it = pixel8u_3(i % 17, i%11, i%37);
    BOOST_CHECK_MESSAGE(imc.pixel(i)[1] == i % 11, "failure with *it = i at pixel " << i << " : it = " << (int)(*it)[1] << " != " << i % 11);
  }
  BOOST_CHECK_MESSAGE(i == 10*20, "The number of points " << i << " is different from the number of pixels in the image (10*20)");
  
  BOOST_CHECKPOINT("image_binary_interface::test_copy_channel_into_another - do");
  yaRC res = yayi::copy_one_channel_to_another(&imc, 0,2, &imc);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Return of copy indicates an error : " << "\n\t\"" << res << "\"");

  BOOST_CHECKPOINT("image_binary_interface::test_copy_channel_into_another - check");
  i = 0;
  for(image_3c::iterator it = imc.begin_block(), ite = imc.end_block(); it != ite; ++it, i++) {
    BOOST_CHECK_MESSAGE(imc.pixel(i)[0] == imc.pixel(i)[2] && imc.pixel(i) == pixel8u_3(i % 17, i%11, i%17) && *it == pixel8u_3(i % 17, i%11, i%17), "failure with *it = i at pixel " << i << " : it = " << *it << " != " << pixel8u_3(i % 17, i%11, i%17));
  }
  BOOST_CHECK_MESSAGE(i == 10*20, "The number of points " << i << " is different from the number of pixels in the image (10*20)");
    
    
}
  
  
BOOST_AUTO_TEST_CASE(set_constant)
{
  using namespace yayi;
  int i = 0;
  for(image_3f_t::iterator it = im3D.begin_block(), ite = im3D.end_block(); it != ite; ++it, i++) {
    *it = i / float(50*40*30);
    BOOST_CHECK_CLOSE(im3D.pixel(i), static_cast<float>(i / float(50*40*30)), 1E-4);//, "failure with *it = i at pixel " << i << " : it = " << (float)(*it) << " != " << i / float(50*40*30));
  }
  BOOST_CHECK_MESSAGE(i == 50*40*30, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");
  
  BOOST_CHECKPOINT("image_binary_interface::test_set_constant - copy");
  yaRC res = copy(&im3D, &im3D_2);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Return of copy indicates an error : " << "\n\t\"" << res << "\"");

  BOOST_CHECKPOINT("image_binary_interface::test_set_constant - check");
  i = 0;
  for(image_3f_t::iterator it = im3D_2.begin_block(), ite = im3D_2.end_block(); it != ite; ++it, i++) {
    BOOST_CHECK_CLOSE(im3D_2.pixel(i), i / float(50*40*30), 1E-4);//, "failure with *it = i at pixel " << i << " : it = " << *it);
    BOOST_CHECK_CLOSE(*it, i / float(50*40*30), 1E-4);//, "failure with *it = i at pixel " << i << " : it = " << *it);
  }
  BOOST_CHECK_MESSAGE(i == 50*40*30, "The number of points " << i << " is different from the number of pixels in the image (50*40*30)");
    
    
}  

BOOST_AUTO_TEST_SUITE_END()
