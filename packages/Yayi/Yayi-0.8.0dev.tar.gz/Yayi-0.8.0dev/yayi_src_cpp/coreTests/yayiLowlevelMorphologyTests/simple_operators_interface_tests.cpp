
#include "main.hpp"
#include <yayiLowLevelMorphology/lowlevel_erosion_dilation.hpp>
#include <yayiLowLevelMorphology/include/lowlevel_erosion_dilation_t.hpp>
#include <yayiIO/include/yayi_IO.hpp>
#include <yayiImageCore/yayiImageCoreFunctions.hpp>
#include <yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <yayiPixelProcessing/image_channels_process.hpp>
#include <iostream>
#include <yayiCommon/include/common_time.hpp>



// for data paths
#include <yayiCommonCoreTests/data_path_for_tests.hpp>



struct fixture_low_level 
{
  yayi::IImage *im, *imtemp, *imout;
  fixture_low_level() : im(0), imtemp(0), imout(0) {}
  
  ~fixture_low_level() 
  {
    delete im;
    delete imtemp;
    delete imout;
  }
};

BOOST_FIXTURE_TEST_SUITE(low_level_interface_tests, fixture_low_level);

BOOST_AUTO_TEST_CASE(erosion_interface_function)
{
  using namespace yayi;
  std::string im_file_name(get_data_from_data_path("release-grosse bouche.jpg"));
  BOOST_TEST_MESSAGE("Reading the image " + im_file_name);
  
  BOOST_REQUIRE(yayi::IO::readJPG(im_file_name, im) == yaRC_ok);
  imtemp = GetSameImage(im, type_scalar_uint8);
  BOOST_REQUIRE(imtemp != 0);
  imout = GetSameImage(imtemp);
  BOOST_REQUIRE(imout != 0);
  
  yaRC res(yaRC_ok);
  
  res = copy_one_channel(im, 0, imtemp);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, 
    "An errror occured during the extraction of the first channel. Details follows: \n" 
    << res 
    << "\nInput image " << im->Description() 
    << "\nOutput image " << imtemp->Description() << "\n");

  #define NB_LOOP 10

  yayi::time::s_time_elapsed time_e;
  for(int i = 0; i < NB_LOOP; i++)
  {
    BOOST_REQUIRE_EQUAL(llmm::erosion(imtemp, &se::SESquare2D, imout), yaRC_ok);
  }
  yayi::time::s_time_elapsed stop_e;
  
  std::cout << "Erosion total microseconds = " << time_e.total_microseconds(stop_e)/NB_LOOP << "\tfor each pixel: " << time_e.total_microseconds(stop_e)/(NB_LOOP*total_number_of_points(imtemp->GetSize())) << std::endl;

  yayi::time::s_time_elapsed time_e2;
  for(int i = 0; i < NB_LOOP; i++)
  {
    BOOST_REQUIRE_EQUAL(
      llmm::erode_image_t(
        dynamic_cast< Image<yaUINT8> const& >(*imtemp), 
        se::SESquare2D, 
        dynamic_cast< Image<yaUINT8> & >(*imout)), 
      yaRC_ok);
  }
  yayi::time::s_time_elapsed stop_e2;

  std::cout << "Erosion total microseconds (template) = " << time_e2.total_microseconds(stop_e2)/NB_LOOP << "\tfor each pixel: " << time_e2.total_microseconds(stop_e2)/(NB_LOOP*total_number_of_points(imtemp->GetSize())) << std::endl;

}

BOOST_AUTO_TEST_SUITE_END()


