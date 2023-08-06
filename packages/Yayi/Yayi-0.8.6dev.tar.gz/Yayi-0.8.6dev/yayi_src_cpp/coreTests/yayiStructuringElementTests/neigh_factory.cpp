#include "main.hpp"
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_t.hpp>
#include <yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>
#include <yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <yayiIO/include/yayi_IO.hpp>

#include <yayiCommonCoreTests/data_path_for_tests.hpp>
using namespace yayi;
using namespace yayi::se;

BOOST_AUTO_TEST_SUITE(factory)

BOOST_AUTO_TEST_CASE(basics)
{
  
  std::string im_file_name(get_data_from_data_path("release-grosse bouche.jpg"));
  BOOST_TEST_MESSAGE("Reading the image " + im_file_name);  
  
  IImage *im = 0;
  yaRC res = yayi::IO::readJPG(im_file_name, im);
  BOOST_REQUIRE_MESSAGE(res == yaRC_ok, "An error occured while reading the image " << im_file_name << " error follows \n" << res);
  
  IConstNeighborhood* neigh = IConstNeighborhood::Create(*im, /*(IStructuringElement*)*/ SEHex2D);
  BOOST_CHECK_MESSAGE(neigh, "Combination not supported imin " << im->Description() << " se " << SEHex2D.Description());
  if(neigh) delete neigh;
  delete im;
}

BOOST_AUTO_TEST_SUITE_END()