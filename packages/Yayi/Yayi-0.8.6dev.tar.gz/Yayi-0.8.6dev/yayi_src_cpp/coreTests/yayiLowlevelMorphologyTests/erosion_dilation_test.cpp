#include "main.hpp"
#include <yayiLowLevelMorphology/include/lowlevel_erosion_dilation_t.hpp>
#include <yayiIO/include/yayi_IO.hpp>
#include <yayiImageCore/yayiImageCoreFunctions.hpp>
#include <yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <yayiPixelProcessing/image_channels_process.hpp>
#include <yayiImageCore/include/yayiImageUtilities_T.hpp>
#include <iostream>



BOOST_AUTO_TEST_CASE(erosion) 
{
  using namespace yayi;
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_test, im_out;
  image_type::coordinate_type coord;
  coord[0] = 5; coord[1] = 5;
  BOOST_REQUIRE(im_in.SetSize(coord) == yaRC_ok);
  BOOST_REQUIRE_MESSAGE(im_in.AllocateImage() == yaRC_ok, "im_test.AllocateImage() error");

  BOOST_REQUIRE(im_test.SetSize(coord) == yaRC_ok);
  BOOST_REQUIRE_MESSAGE(im_test.AllocateImage() == yaRC_ok, "imout.AllocateImage() error");

  BOOST_REQUIRE(im_out.SetSize(coord) == yaRC_ok);
  BOOST_REQUIRE_MESSAGE(im_out.AllocateImage() == yaRC_ok, "imout.AllocateImage() error");
  
  // input image
  {
    static const std::string s = 
      "1 2 3 4 5 "
      "6 7 8 8 2 "
      "11 12 13 14 15 "
      "255 254 253 252 251 "
      "128 127 126 125 124";
      
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // output image
  {
    static const std::string s = 
      "1 1 2 2 2 "
      "1 1 2 2 2 "
      "6 6 7 2 2 "
      "11 11 12 13 14 "
      "127 126 125 124 124";
      
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }
  
  yaRC res = llmm::erode_image_t(im_in, se::SESquare2D, im_out);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "Error during the erosion, details : \n " << res);

  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Erosion error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }

}


