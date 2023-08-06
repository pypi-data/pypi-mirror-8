#include "main.hpp"
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <yayiReconstruction/include/morphological_fill_holes_t.hpp>

BOOST_AUTO_TEST_CASE(fill_hole) 
{
  using namespace yayi;
  
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_test, im_out;
  image_type* p_im[] = {&im_in, &im_test, &im_out};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 4;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE_EQUAL(p_im[i]->SetSize(coord), yaRC_ok);
    BOOST_REQUIRE_EQUAL(p_im[i]->AllocateImage(), yaRC_ok);
  }
  
  // input mask image
  {
    static const std::string s = 
      "1 2 1 0 "
      "1 0 1 0 "
      "2 1 3 0 "
      "0 0 0 0 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // output test image
  {
    static const std::string s = 
      "1 2 1 0 "
      "1 1 1 0 "
      "2 1 3 0 "
      "0 0 0 0 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }

  BOOST_REQUIRE_EQUAL(reconstructions::fill_holes_image_t(im_in, se::SESquare2D, im_out), yaRC_ok);
  
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Erosion error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
}


