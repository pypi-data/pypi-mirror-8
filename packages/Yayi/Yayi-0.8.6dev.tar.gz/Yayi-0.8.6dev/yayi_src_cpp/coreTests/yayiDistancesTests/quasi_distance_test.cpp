#include "main.hpp"

#include <yayiDistances/include/quasi_distance_T.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>


BOOST_AUTO_TEST_CASE(quasi_distance_and_residual) 
{
  using namespace yayi;
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_test_res, im_test_dist, im_out_res, im_out_dist;
  image_type* p_im[] = {&im_in, &im_test_res, &im_test_dist, &im_out_res, &im_out_dist};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE_EQUAL(p_im[i]->SetSize(coord), yaRC_ok);
    BOOST_REQUIRE_EQUAL(p_im[i]->AllocateImage(), yaRC_ok);
  }
  
  // input image
  {
    static const std::string s = 
      "1 2 3 2 "
      "6 7 8 8 "
      "1 2 0 4 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // theoretical residu image
  {
    static const std::string s = 
      "1 1 2 2 "
      "5 7 8 8 "
      "1 2 0 4 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_res, "Error during the input streaming of the image");
  }

  // theoretical distance image
  {
    static const std::string s = 
      "2 2 2 2 "
      "1 1 1 1 "
      "2 1 0 1 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_dist, "Error during the input streaming of the image");
  }
  
  BOOST_REQUIRE_EQUAL(distances::quasi_distance_t(im_in, se::SESquare2D, im_out_dist, im_out_res), yaRC_ok);
  
  // check des sorties
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out_res.pixel(i) == im_test_res.pixel(i), "Residu error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_res.pixel(i) << " != " << (int)im_test_res.pixel(i));
  }
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out_dist.pixel(i) == im_test_dist.pixel(i), 
      "Distance error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_dist.pixel(i) << " != " << (int)im_test_dist.pixel(i));
  }
  
  
}


