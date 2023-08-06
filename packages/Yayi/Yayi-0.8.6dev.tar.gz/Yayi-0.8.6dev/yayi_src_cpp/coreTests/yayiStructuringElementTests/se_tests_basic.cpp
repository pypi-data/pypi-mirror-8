


/*!@file
 * This file test the functions associated to structuring elements (ie. not the neighborhoods)
 *
 * @author Raffi Enficiaud
 */

#include "main.hpp"
#include <yayiStructuringElement/yayiStructuringElement.hpp>
#include <yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <iostream>

using namespace yayi;
using namespace yayi::se;


BOOST_AUTO_TEST_SUITE(predefined_se_checks)



BOOST_AUTO_TEST_CASE(predefined_se)
{
  
  BOOST_CHECK(SEHex2D.size() == 14);
  BOOST_CHECK(SEHex2D.number_of_list() == 2);
  BOOST_CHECK(SEHex2D.has_multiple_list());
  BOOST_CHECK(SEHex2D.GetType() == e_set_neighborlist);
  BOOST_CHECK(SEHex2D.GetSubType() == e_sest_neighborlist_hexa);

  BOOST_CHECK(SEHex2D.maximum_extension().first == c2D(-1,-1));
  BOOST_CHECK_MESSAGE(SEHex2D.maximum_extension().second == c2D(1,1), "Maximal extension error : " << SEHex2D.maximum_extension().second << " != " << c2D(1,1));
  
  BOOST_CHECK(SESquare2D.size() == 9);
  BOOST_CHECK(SESquare2D.number_of_list() == 1);
  BOOST_CHECK(!SESquare2D.has_multiple_list());
  BOOST_CHECK(SESquare2D.GetType() == e_set_neighborlist);
  BOOST_CHECK(SESquare2D.GetSubType() == e_sest_neighborlist_generic_single);


  BOOST_CHECK(SESquare3D.size() == 27);
  BOOST_CHECK(SESquare3D.number_of_list() == 1);
  BOOST_CHECK(!SESquare3D.has_multiple_list());
  BOOST_CHECK(SESquare3D.GetType() == e_set_neighborlist);
  BOOST_CHECK(SESquare3D.GetSubType() == e_sest_neighborlist_generic_single);
  
}


BOOST_AUTO_TEST_CASE(check_equality)
{
  
  BOOST_CHECK(SEHex2D == SEHex2D);
  BOOST_CHECK(!(SEHex2D != SEHex2D));
}

BOOST_AUTO_TEST_CASE(check_remove_center)
{

  BOOST_CHECK(SEHex2D.remove_center() != SEHex2D);
  BOOST_CHECK(!(SEHex2D.remove_center() == SEHex2D));
  
  BOOST_CHECK(SESquare2D.size() == SESquare2D.remove_center().size() + 1);
}

BOOST_AUTO_TEST_CASE(check_unordered_equality)
{
  BOOST_CHECK(SEHex2D.is_equal_unordered(SEHex2D));
  BOOST_CHECK(!SEHex2D.remove_center().is_equal_unordered(SEHex2D));
  BOOST_CHECK(!SEHex2D.is_equal_unordered(SEHex2D.remove_center()));
  
  BOOST_CHECK(dynamic_cast<const IStructuringElement&>(SESquare2D).is_equal(&SESquare2D));
  BOOST_CHECK(!dynamic_cast<const IStructuringElement&>(SESquare2D).is_equal(&SEHex2D));
  BOOST_CHECK(dynamic_cast<const IStructuringElement&>(SESquare2D).is_equal_unordered(&SESquare2D));
  BOOST_CHECK(!dynamic_cast<const IStructuringElement&>(SESquare2D).is_equal_unordered(&SEHex2D));

}

//BOOST_AUTO_TEST_SUITE_END()

//BOOST_AUTO_TEST_SUITE(predefined_se_checks)

BOOST_AUTO_TEST_CASE(clone)
{
  const IStructuringElement* se_ = &SEHex2D;
  std::auto_ptr<IStructuringElement> se2_(se_->Clone());
  std::auto_ptr<IStructuringElement> se3_(se_->Transpose());
  
  BOOST_CHECK(se_);
  BOOST_CHECK(se2_.get());
  BOOST_CHECK(se3_.get());
}

BOOST_AUTO_TEST_CASE(remove_center)
{
  typedef s_coordinate<2> coordinate_type;
  BOOST_CHECK(SEHex2D.size() == 14);
  BOOST_CHECK(SEHex2D.remove_center().size() == 12);
  BOOST_CHECK(SEHex2D.number_of_list() == 2);
  BOOST_CHECK(SEHex2D.remove_center().number_of_list() == 2);
  BOOST_CHECK(SEHex2D.has_multiple_list());
  BOOST_CHECK(SEHex2D.remove_center().has_multiple_list());
  BOOST_CHECK(SEHex2D.GetType() == e_set_neighborlist);
  BOOST_CHECK(SEHex2D.remove_center().GetType() == e_set_neighborlist);
  BOOST_CHECK(SEHex2D.GetSubType() == e_sest_neighborlist_hexa);
  BOOST_CHECK(SEHex2D.remove_center().GetSubType() == e_sest_neighborlist_hexa);
  
  s_neighborlist_se_hexa_x<coordinate_type> se, sep;
  
  static const coordinate_type::scalar_coordinate_type coords [] = {0,0, 1,0, -1,0, 0,1,   0,0, 1,0, -1,0, 0,-1};
  
  std::vector<coordinate_type> v(coordinate_type::from_table_multiple(coords, coords + sizeof(coords)/sizeof(coords[0])));
  BOOST_REQUIRE(v.size() == 8);
  
  BOOST_CHECK_MESSAGE(se.size() == 0, "SE size = " << se.size() << " != 0");
  BOOST_CHECK(se.set_coordinates(v) == yaRC_ok);
  BOOST_CHECK_MESSAGE(se.size() == 8, "SE size = " << se.size() << " != 6");
  BOOST_CHECK_MESSAGE(*se.begin() == c2D(0,0), "First element corrupted " << *se.begin() << " != " << c2D(0,0));
  
  BOOST_CHECK_MESSAGE(se.remove_center().size() == 6, "SE size = " << se.size() << " != 6");
  BOOST_CHECK_MESSAGE(*se.remove_center().begin() == c2D(1,0), "First element (removed center) corrupted " << *se.remove_center().begin() << " != " << c2D(1,0));
  BOOST_CHECK_MESSAGE(*(se.remove_center().begin() + 3) == c2D(1,0), "Forth element (removed center) corrupted " << *se.remove_center().begin() << " != " << c2D(1,0));

  sep = se.remove_center();
  BOOST_CHECK_MESSAGE(sep.size() == 6, "SE size = " << sep.size() << " != 6");
  BOOST_CHECK_MESSAGE(*sep.begin() == c2D(1,0), "First element (removed center) corrupted " << *sep.begin() << " != " << c2D(1,0));
  BOOST_CHECK_MESSAGE(*(sep.begin() + 3) == c2D(1,0), "Forth element (removed center) corrupted " << *sep.begin() << " != " << c2D(1,0));

  
}

BOOST_AUTO_TEST_SUITE_END()


