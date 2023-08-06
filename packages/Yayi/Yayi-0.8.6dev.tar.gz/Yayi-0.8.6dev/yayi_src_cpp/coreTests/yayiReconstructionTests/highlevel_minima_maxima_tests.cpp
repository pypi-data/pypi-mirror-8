#include "main.hpp"

#include <yayiReconstruction/include/highlevel_minima_maxima_t.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>


struct fixture_hminmax_tests
{
  typedef yayi::Image<yayi::yaUINT8> image_type;
  image_type im_in, im_test, im_out;
  image_type::coordinate_type coord;
  
  fixture_hminmax_tests() : coord(yayi::c2D(10, 5))
  {
    using namespace yayi;
    BOOST_REQUIRE_EQUAL(im_in.SetSize(coord), yaRC_ok);
    BOOST_REQUIRE_EQUAL(im_in.AllocateImage(), yaRC_ok);

    BOOST_REQUIRE_EQUAL(im_test.SetSize(coord), yaRC_ok);
    BOOST_REQUIRE_EQUAL(im_test.AllocateImage(), yaRC_ok);

    BOOST_REQUIRE_EQUAL(im_out.SetSize(coord), yaRC_ok);
    BOOST_REQUIRE_EQUAL(im_out.AllocateImage(), yaRC_ok);  
  }
};

BOOST_FIXTURE_TEST_SUITE(hminmax, fixture_hminmax_tests)

BOOST_AUTO_TEST_CASE(hminima) 
{
  using namespace yayi;
  // input image
  {
    static const std::string s = 
      "8 8 8 8 8 8 8 8 8 8 "
      "8 7 7 7 8 8 7 7 7 8 "
      "8 7 6 7 8 8 7 3 7 8 "
      "8 7 7 7 8 8 7 7 7 8 "
      "8 8 8 8 8 8 8 8 8 8";

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // output image
  {
    static const std::string s = 
      "8 8 8 8 8 8 8 8 8 8 "
      "8 8 8 8 8 8 7 7 7 8 "
      "8 8 8 8 8 8 7 6 7 8 "
      "8 8 8 8 8 8 7 7 7 8 "
      "8 8 8 8 8 8 8 8 8 8";

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }

  BOOST_REQUIRE_EQUAL(hlmm::image_h_minima_t(im_in,se::SESquare2D,3,im_out), yaRC_ok);

  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "hminima error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
}

BOOST_AUTO_TEST_CASE(hmaxima) 
{
  using namespace yayi;

  // input image
  {
    static const std::string s =
      "3 3 3 3 3 3 3 3 3 3 "
      "3 4 4 4 3 3 4 4 4 3 "
      "3 4 5 4 3 3 4 9 4 3 "
      "3 4 4 4 3 3 4 4 4 3 "
      "3 3 3 3 3 3 3 3 3 3";

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // output image
  {
    static const std::string s =
      "3 3 3 3 3 3 3 3 3 3 "
      "3 3 3 3 3 3 4 4 4 3 "
      "3 3 3 3 3 3 4 6 4 3 "
      "3 3 3 3 3 3 4 4 4 3 "
      "3 3 3 3 3 3 3 3 3 3";

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }

  BOOST_REQUIRE_EQUAL(hlmm::image_h_maxima_t(im_in,se::SESquare2D,3,im_out), yaRC_ok);

  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "hmaxima error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
}

BOOST_AUTO_TEST_CASE(hconvex) 
{
  using namespace yayi;

  // input image
  {
    static const std::string s =
      "3 3 3 3 3 3 3 3 3 3 "
      "3 4 4 4 3 3 4 4 4 3 "
      "3 4 5 4 3 3 4 9 4 3 "
      "3 4 4 4 3 3 4 4 4 3 "
      "3 3 3 3 3 3 3 3 3 3";

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // output image
  {
    static const std::string s =
      "0 0 0 0 0 0 0 0 0 0 "
      "0 1 1 1 0 0 0 0 0 0 "
      "0 1 2 1 0 0 0 3 0 0 "
      "0 1 1 1 0 0 0 0 0 0 "
      "0 0 0 0 0 0 0 0 0 0";

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }

  BOOST_REQUIRE_EQUAL(hlmm::image_h_convex_t(im_in,se::SESquare2D,3,im_out), yaRC_ok);
  
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "hconvex error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
}


BOOST_AUTO_TEST_CASE(hconcave) 
{
  using namespace yayi;

  // input image
  {
    static const std::string s = 
      "8 8 8 8 8 8 8 8 8 8 "
      "8 7 7 7 8 8 7 7 7 8 "
      "8 7 6 7 8 8 7 3 7 8 "
      "8 7 7 7 8 8 7 7 7 8 "
      "8 8 8 8 8 8 8 8 8 8";

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // output image
  {
    static const std::string s = 
      "0 0 0 0 0 0 0 0 0 0 "
      "0 1 1 1 0 0 0 0 0 0 "
      "0 1 2 1 0 0 0 3 0 0 "
      "0 1 1 1 0 0 0 0 0 0 "
      "0 0 0 0 0 0 0 0 0 0";

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }

  BOOST_REQUIRE_EQUAL(hlmm::image_h_concave_t(im_in,se::SESquare2D,3,im_out), yaRC_ok);
  
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "hconcave error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
}

BOOST_AUTO_TEST_CASE(pseudo_dynamic_closing)
{
  using namespace yayi;
  // input image
  {
    static const std::string s = 
      "8 8 8 8 8 8 8 8 8 8 "
      "8 7 7 7 8 8 7 7 7 8 "
      "8 7 6 7 8 8 7 3 7 8 "
      "8 7 7 7 8 8 7 7 7 8 "
      "8 8 8 8 8 8 8 8 8 8";

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // output image
  {
    static const std::string s = 
      "8 8 8 8 8 8 8 8 8 8 "
      "8 8 8 8 8 8 7 7 7 8 "
      "8 8 8 8 8 8 7 3 7 8 "
      "8 8 8 8 8 8 7 7 7 8 "
      "8 8 8 8 8 8 8 8 8 8"; //3 and not 6 at position (7,2) see

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }

  BOOST_REQUIRE_EQUAL(hlmm::image_h_dynamic_closing_t(im_in,se::SESquare2D,3,im_out), yaRC_ok);
  
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "pseudo_dynamic_closing error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
}


BOOST_AUTO_TEST_CASE(pseudo_dynamic_opening)
{
  using namespace yayi;

  // input image
  {
    static const std::string s = 
      "3 3 3 3 3 3 3 3 3 3 "
      "3 4 4 4 3 3 4 4 4 3 "
      "3 4 5 4 3 3 4 9 4 3 "
      "3 4 4 4 3 3 4 4 4 3 "
      "3 3 3 3 3 3 3 3 3 3";

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // output image
  {
    static const std::string s = 
      "3 3 3 3 3 3 3 3 3 3 "
      "3 3 3 3 3 3 4 4 4 3 "
      "3 3 3 3 3 3 4 9 4 3 "
      "3 3 3 3 3 3 4 4 4 3 "
      "3 3 3 3 3 3 3 3 3 3"; //9 and not 6 at position (7,2)

    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test, "Error during the input streaming of the image");
  }

  BOOST_REQUIRE_EQUAL(hlmm::image_h_dynamic_opening_t(im_in,se::SESquare2D,3,im_out), yaRC_ok);
  
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out.pixel(i) == im_test.pixel(i), "pseudo_dynamic_opening error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out.pixel(i) << " != " << (int)im_test.pixel(i));
  }
}

BOOST_AUTO_TEST_SUITE_END()
