#include "main.hpp"
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiReconstruction/include/morphological_reconstruction_t.hpp>
#include <yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>

BOOST_AUTO_TEST_CASE(reconstruction_simple) 
{
  using namespace yayi;
  
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_mark, im_test, im_out;
  image_type* p_im[] = {&im_in, &im_test, &im_out, &im_mark};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE_EQUAL(p_im[i]->SetSize(coord), yaRC_ok);
    BOOST_REQUIRE_EQUAL(p_im[i]->AllocateImage(), yaRC_ok);
  }
  
  // input mask image
  {
    static const std::string s = 
      "1 2 5 2 "
      "5 1 3 2 "
      "1 3 10 2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // input mark image
  {
    static const std::string s = 
      "0 0 3 0 "
      "0 0 0 0 "
      "0 0 2 0 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_mark, "Error during the input streaming of the image");
  }

  // output test image
  {
    static const std::string s = 
      "1 2 3 2 "
      "3 1 3 2 "
      "1 3 3 2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }



  reconstructions::s_generic_reconstruction_t<image_type> rec_op; 
  BOOST_REQUIRE_EQUAL(rec_op(im_mark, im_in, se::SESquare2D, im_out), yaRC_ok);
  
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "Reconstruction error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
}


