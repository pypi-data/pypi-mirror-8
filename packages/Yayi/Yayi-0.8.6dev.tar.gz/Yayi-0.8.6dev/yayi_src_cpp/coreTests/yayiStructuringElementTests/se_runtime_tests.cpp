


/*!@file
 * This file test the functions associated to runtime structuring elements
 *
 * @author Raffi Enficiaud
 */

#include "main.hpp"
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_t.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>

using namespace yayi;
using namespace yayi::se;
#define SE_FROM_TABLE(x) x, x + sizeof(x)/sizeof(x[0])



struct runtime_tests_fixture
{
  typedef Image<yaUINT8> image_t;
  typedef s_neighborlist_se<image_t::coordinate_type> neigh_t;
  neigh_t se;
  
  runtime_tests_fixture()
  {
    static const image_t::coordinate_type::scalar_coordinate_type coords [] = {0,0, 1,0, -1,0, 0,1};
    std::vector<image_t::coordinate_type> v(image_t::coordinate_type::from_table_multiple(coords, coords + sizeof(coords)/sizeof(coords[0])));
    BOOST_REQUIRE(v.size() == 4);
    
    BOOST_CHECK_EQUAL(se.size(), 0);
    BOOST_CHECK_EQUAL(se.set_coordinates(v), yaRC_ok);
    BOOST_CHECK_EQUAL(se.size(), 4);
    
  }
};


BOOST_FIXTURE_TEST_SUITE( runtime_tests, runtime_tests_fixture )

BOOST_AUTO_TEST_CASE(basics) 
{
  BOOST_CHECK_EQUAL(*se.begin(), c2D(0,0));
}

BOOST_AUTO_TEST_CASE(check_equality)
{
  static const image_t::coordinate_type::scalar_coordinate_type coords2 [] = {0,0, 1,0, 0,1, -1,0};
  BOOST_CHECK(se == se);
  BOOST_CHECK(!(se != se));
  BOOST_CHECK(se.is_equal_unordered(se));
  
  neigh_t se2(se);
  BOOST_CHECK(se == se2);
  BOOST_CHECK(!(se != se2));
  BOOST_CHECK(se.is_equal_unordered(se2));
  BOOST_CHECK(se2.is_equal_unordered(se));

  neigh_t se3(image_t::coordinate_type::from_table_multiple(SE_FROM_TABLE(coords2)));
  BOOST_CHECK(se != se3);
  BOOST_CHECK(!(se == se3));
  BOOST_CHECK(se.is_equal_unordered(se3));
  BOOST_CHECK(se3.is_equal_unordered(se));      
}

BOOST_AUTO_TEST_CASE(iteration)
{
  int count = 0;
  for(neigh_t::const_iterator it = se.begin(), ite = se.end(); it != ite; ++it) {
    count ++;
  }
  BOOST_CHECK_MESSAGE(count == 4, "SE counted elements = " << count << " != 4");
}

BOOST_AUTO_TEST_CASE(check_max_extension)
{
  static const image_t::coordinate_type::scalar_coordinate_type coords2 [] = {0,0, 1,0, 0,3, -4,0};
  BOOST_CHECK(se.maximum_extension(0, true) == 1);
  BOOST_CHECK(se.maximum_extension(0, false) == 1);
  BOOST_CHECK(se.maximum_extension(1, true) == 1);
  BOOST_CHECK(se.maximum_extension(1, false) == 0);
  
  std::pair<image_t::coordinate_type, image_t::coordinate_type> ret = se.maximum_extension();
  BOOST_CHECK_EQUAL(ret.second[0], 1); // second are the max
  BOOST_CHECK_EQUAL(ret.first[0], -1); // first are the min
  BOOST_CHECK_EQUAL(ret.second[1], 1);
  BOOST_CHECK_EQUAL(ret.first[1], 0);
  
  
  
  neigh_t se2(image_t::coordinate_type::from_table_multiple(SE_FROM_TABLE(coords2)));
  BOOST_CHECK(se2.maximum_extension(0, true) == 1);
  BOOST_CHECK(se2.maximum_extension(0, false) == 4);
  BOOST_CHECK(se2.maximum_extension(1, true) == 3);
  BOOST_CHECK(se2.maximum_extension(1, false) == 0);

  ret = se2.maximum_extension();
  BOOST_CHECK_EQUAL(ret.second[0], 1);
  BOOST_CHECK_EQUAL(ret.first[0], -4);
  BOOST_CHECK_EQUAL(ret.second[1], 3);
  BOOST_CHECK_EQUAL(ret.first[1], 0);
}

BOOST_AUTO_TEST_CASE(check_transpose)
{
  BOOST_CHECK_MESSAGE(se.transpose().size() == 4, "SE size = " << se.transpose().size() << " != 4");

  static const image_t::coordinate_type::scalar_coordinate_type coords_transpose [] = {0,0, -1,0, 1,0, 0,-1};
  static const image_t::coordinate_type::scalar_coordinate_type coords_transpose_unordered [] = {0,0, 1,0, -1,0, 0,-1};
  static const image_t::coordinate_type::scalar_coordinate_type coords_transpose_unordered_more [] = {0,0, 1,0, -1,0, 0,-1, 0,0};  

  s_neighborlist_se<image_t::coordinate_type> 
    se_transposed(se.transpose()), 
    se_transposed_test(image_t::coordinate_type::from_table_multiple(SE_FROM_TABLE(coords_transpose))),
    se_transposed_test_unordered(image_t::coordinate_type::from_table_multiple(SE_FROM_TABLE(coords_transpose_unordered))),
    se_transposed_test_unordered_more(image_t::coordinate_type::from_table_multiple(SE_FROM_TABLE(coords_transpose_unordered_more)))
    ;

  BOOST_CHECK(se_transposed == se_transposed); // test d'égalité simple
  BOOST_CHECK(se_transposed == se_transposed_test);
  BOOST_CHECK(!(se_transposed == se_transposed_test_unordered));
  BOOST_CHECK(!(se_transposed_test == se_transposed_test_unordered));
  
  BOOST_CHECK(se_transposed.is_equal_unordered(se_transposed_test));
  BOOST_CHECK(se_transposed.is_equal_unordered(se_transposed_test_unordered));
  BOOST_CHECK(se_transposed.is_equal_unordered(se_transposed_test_unordered_more));
  BOOST_CHECK(se_transposed_test.is_equal_unordered(se_transposed_test_unordered_more));
  

  static const image_t::coordinate_type::scalar_coordinate_type coords_no_center [] = {1,0, -1,0, 0,1};
  static const image_t::coordinate_type::scalar_coordinate_type coords_transpose_no_center_unordered [] = {0,1, 1,0, -1,0};
  static const image_t::coordinate_type::scalar_coordinate_type coords_transpose_no_center_unordered_more [] = {1,0, -1,0, 0,-1};
  
  s_neighborlist_se<image_t::coordinate_type> 
    se_no_center(se.remove_center()),
    se_no_center_test(image_t::coordinate_type::from_table_multiple(SE_FROM_TABLE(coords_no_center))),
    se_transposed_no_center(se.transpose().remove_center()),
    se_transposed_no_center2(se_transposed_test_unordered_more.remove_center()),
    se_transposed_no_center3(image_t::coordinate_type::from_table_multiple(SE_FROM_TABLE(coords_transpose_no_center_unordered_more)))
    ; 

  BOOST_CHECK(se_no_center == se_no_center_test);
  BOOST_CHECK(se_no_center.is_equal_unordered(se_no_center_test));
  
  BOOST_CHECK(se_transposed_no_center == se_transposed.remove_center());
  BOOST_CHECK(se_transposed == se_transposed_test); // test de non de modification du SE original

  BOOST_CHECK(se_transposed_no_center2 == se_transposed_no_center3);



}

BOOST_AUTO_TEST_CASE(check_hexagonal_se_initialisation)
{
  typedef image_t::coordinate_type coordinate_type;
  s_neighborlist_se_hexa_x<coordinate_type> se_hex, se_hex2, se_hex3;
  
  BOOST_CHECK_MESSAGE(se_hex.number_of_list() == 2, "Bad number of lists (init): " << se_hex.number_of_list() << " != 2");
  
  static const coordinate_type::scalar_coordinate_type coords [] = {0,0, 1,0, -1,0, 0,1,   0,0, 1,0, -1,0, 0,-1};
  
  std::vector<coordinate_type> v(coordinate_type::from_table_multiple(coords, coords + sizeof(coords)/sizeof(coords[0])));
  BOOST_REQUIRE(v.size() == 8);
  
  BOOST_CHECK_MESSAGE(se_hex.size() == 0, "SE size = " << se.size() << " != 0");
  BOOST_CHECK(se_hex.set_coordinates(v) == yaRC_ok);
  BOOST_CHECK_MESSAGE(se_hex.size() == 8, "SE size = " << se.size() << " != 8");
  BOOST_CHECK_MESSAGE(*se_hex.begin() == c2D(0,0), "First element corrupted " << *se_hex.begin() << " != " << c2D(0,0));
  
  BOOST_CHECK_MESSAGE(se_hex.number_of_list() == 2, "Bad number of lists : " << se_hex.number_of_list() << " != 2");
  BOOST_CHECK(se_hex.has_multiple_list());
  BOOST_CHECK(se_hex.GetType() == e_set_neighborlist);
  BOOST_CHECK(se_hex.GetSubType() == e_sest_neighborlist_hexa);

  BOOST_CHECK(se_hex.is_equal_unordered(se_hex));
  BOOST_CHECK(se_hex == se_hex);
  BOOST_CHECK(!(se_hex != se_hex));


  
  BOOST_CHECKPOINT("check_hexa_init: copy test");
  se_hex2 = se_hex;
  BOOST_CHECK(se_hex2.has_multiple_list());
  BOOST_CHECK_MESSAGE(se_hex2.number_of_list() == 2, "Bad number of lists : " << se_hex2.number_of_list() << " != 2");

  se_hex3 = se_hex; // save status
  se_hex2 = se_hex.transpose();
  BOOST_CHECK_MESSAGE(se_hex == se_hex3, "Transposition does not garanty the initial state of the structuring element (should return a transposed copy)");
  BOOST_CHECK(se_hex2.has_multiple_list());
  BOOST_CHECK_MESSAGE(se_hex2.number_of_list() == 2, "Bad number of lists : " << se_hex2.number_of_list() << " != 2");
  BOOST_CHECK(se_hex2 != se_hex);
  BOOST_CHECK(!(se_hex2 == se_hex));
  BOOST_CHECK(!se_hex2.is_equal_unordered(se_hex));
  BOOST_CHECK(!se_hex.is_equal_unordered(se_hex2));
  BOOST_CHECK(!se_hex.is_equal_unordered(se_hex2));
  

  static const coordinate_type::scalar_coordinate_type coords_unequal [] = {0,0, 1,0, -1,0, 0,1, 0,-1};
  std::vector<coordinate_type> vv(coordinate_type::from_table_multiple(coords_unequal, coords_unequal + sizeof(coords_unequal)/sizeof(coords_unequal[0])));

  BOOST_CHECK(se_hex2.set_coordinates(vv) == yaRC_ok);
  BOOST_CHECK(se_hex2.has_multiple_list());
  BOOST_CHECK_MESSAGE(se_hex2.number_of_list() == 2, "Bad number of lists : " << se_hex2.number_of_list() << " != 2");
  BOOST_CHECK(se_hex2 != se_hex);
  BOOST_CHECK(!(se_hex2 == se_hex));
  BOOST_CHECK(!se_hex2.is_equal_unordered(se_hex));
  BOOST_CHECK(se_hex2.is_equal_unordered(se_hex2));
  
}

BOOST_AUTO_TEST_SUITE_END()

