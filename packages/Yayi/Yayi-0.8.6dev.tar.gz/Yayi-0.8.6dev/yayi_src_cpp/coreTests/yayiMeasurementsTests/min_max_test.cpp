#include "main.hpp"
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiMeasurements/measurements_min_max.hpp>
#include <yayiMeasurements/include/measurements_min_max_t.hpp>

BOOST_AUTO_TEST_CASE(min_max_simple) 
{
  using namespace yayi;
  
  typedef Image<yaUINT8> image_type;
  
  image_type im_in;
  image_type* p_im[] = {&im_in};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE_EQUAL(p_im[i]->SetSize(coord), yaRC_ok);
    BOOST_REQUIRE_EQUAL(p_im[i]->AllocateImage(), yaRC_ok);
  }
  
  // input image
  {
    static const std::string s = 
      "1 2 5 2 "
      "1 1 3 2 "
      "1 3 10 2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  variant out;
  BOOST_REQUIRE_EQUAL(measurements::image_meas_min_max_t(im_in, out), yaRC_ok);
  std::pair<image_type::pixel_type, image_type::pixel_type> v = out;
  
  BOOST_CHECK_MESSAGE(v.first == 1, "Bad output for min: " << v.first << " (result) != 1 (test)");
  BOOST_CHECK_MESSAGE(v.second == 10, "Bad output for max: " << v.second << " (result) != 10 (test)");
  
}
