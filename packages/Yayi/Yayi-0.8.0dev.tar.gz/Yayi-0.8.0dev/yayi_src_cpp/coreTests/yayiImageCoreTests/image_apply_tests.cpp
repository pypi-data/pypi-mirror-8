



#include "main.hpp"
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiImageCore/include/yayiImageUtilities_T.hpp>

#include <yayiImageCore/include/ApplyToImage_T.hpp>
#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_binary_t.hpp>

#include <boost/type_traits/is_same.hpp>
#include <boost/function.hpp>
#include <boost/bind.hpp>

#include <iostream>

using namespace yayi;



struct s_two_times {
  int count;
  
  template <class T> struct result;
  
  template <class op, class T> struct result<op(T)> {
    typedef void type;
  };
  template <class op, class T> struct result<op(const T&)> {
    typedef T type;
  };
  
  
  template <class T>
  void operator()(T& x) throw() {
    x *= 2;
    count ++;
  }

  template <class T1, class T2>
  T2 operator()(const T1& x) throw() {
    count ++;
    return x * 2;
  }

};

struct s_tree_times {
  typedef yayi::ns_operator_tag::operator_commutative operator_tag;
  typedef void result;
  template <class T>
  void operator()(T& x) const throw() {
    x *= 3;
  }
};

struct s_square {
  int count;
  
  template <class T> struct result;
  
  template <class op, class T1, class T2> struct result<op(T1, T2)> {
    typedef typename remove_reference<T2>::type type;
  };
  
  
  template <class T1, class T2>
  typename result<s_square(T1, T2)>::type operator()(T1 x, T2 y) {
    count ++;
    return x * x + y * y;
  }
};

struct image_apply_test_fixture
{
  typedef Image<yaUINT16> image_type;
  image_type im, im1, im2;

  image_apply_test_fixture()
  {
    CreateImages();
    PrepareImages();
  }

  void CreateImages() {
    BOOST_REQUIRE(im1.SetSize(c2D(6,5)) == yaRC_ok);
    BOOST_REQUIRE(im1.AllocateImage() == yaRC_ok);
    BOOST_REQUIRE(im2.SetSize(c2D(6,5)) == yaRC_ok);
    BOOST_REQUIRE(im2.AllocateImage() == yaRC_ok);  
    BOOST_REQUIRE(im.SetSize(c2D(6,5)) == yaRC_ok);
    BOOST_REQUIRE(im.AllocateImage() == yaRC_ok);  
  }
  
  void PrepareImages() {
    static const std::string s = 
      "1 2 3 4 5 42 "
      "6 7 8 8 10 41 "
      "11 12 13 14 15 40 "
      "255 254 253 252 251 39 "
      "128 127 126 125 124 38";

    std::istringstream is(s);
    BOOST_REQUIRE_MESSAGE(is >> im1, "Error during the input streaming of the image");
    BOOST_CHECK_MESSAGE(im1.pixel(c2D(4,0)) == 5, "(pixel(4,0) = " << (int)im1.pixel(c2D(4,0)) << ") != 5");  

    std::istringstream is2(s);
    BOOST_REQUIRE_MESSAGE(is2 >> im2, "Error during the input streaming of the image");
  }  
};

BOOST_FIXTURE_TEST_SUITE(image_apply, image_apply_test_fixture)


BOOST_AUTO_TEST_CASE(test_image_application1)
{
  // Unary operator in-place
  s_apply_unary_operator/*<s_two_times>*/ op_im;
  s_two_times op;
  op.count = 0;
  
  BOOST_CHECK(op_im(im1, op) == yaRC_ok);
  BOOST_CHECK_MESSAGE(op.count == 6*5, "Number of counted operations " << op.count << " !=  " << 6*5);
  
  for(image_type::const_iterator it = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it != ite; ++it, ++it2) {
    BOOST_CHECK_MESSAGE(*it == 2 * (*it2), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
  }
  
  // fonction Process à tester également
}

BOOST_AUTO_TEST_CASE(test_image_application1_inplace)
{
  // Unary operator in-place
  s_apply_unary_operator op_im;
  s_two_times op;
  op.count = 0;
  
  BOOST_CHECK(op_im(im1, op) == yaRC_ok);
  BOOST_CHECK_MESSAGE(op.count == 6*5, "Number of counted operations " << op.count << " !=  " << 6*5);
  
  for(image_type::const_iterator it = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it != ite; ++it, ++it2) {
    BOOST_CHECK_MESSAGE(*it == 2 * (*it2), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
  }
  
  // fonction Process à tester également
}


BOOST_AUTO_TEST_CASE(test_image_application1_notinplace)
{
  // Unary operator in-place
  s_two_times op;
  
  // Adapting the appropriate overloaded method of the object
  boost::function<image_type::pixel_type (const image_type::pixel_type&)> f;
  f = boost::bind(&s_two_times::operator()<image_type::pixel_type, image_type::pixel_type>, &op, _1);
  
  s_apply_unary_operator op_im;

  op.count = 0;
  
  BOOST_CHECK(op_im(im1, im, f) == yaRC_ok);
  BOOST_CHECK_MESSAGE(op.count == 6*5, "Number of counted operations " << op.count << " !=  " << 6*5);
  
  for(image_type::const_iterator it = im1.begin_block(), it2 = im.begin_block(), it3 = im2.begin_block(), ite = im1.end_block(); 
      it != ite; ++it, ++it2, ++it3) {
    BOOST_CHECK_MESSAGE(*it2 == 2 * (*it), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
    BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));
  }
  
  
  // fonction Process à tester également
}


BOOST_AUTO_TEST_CASE(test_image_application2)
{
  s_apply_binary_operator op_im;
  s_square op;
  op.count = 0;
  
  BOOST_CHECK(op_im(im1, im1, im2, op) == yaRC_ok);
  BOOST_CHECK_MESSAGE(op.count == 6*5, "Number of counted operations " << op.count << " !=  " << 6*5);
  
  for(image_type::const_iterator it1 = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it1 != ite; ++it1, ++it2) {
    BOOST_CHECK_MESSAGE(*it2 == static_cast<image_type::pixel_type>(2 * (*it1) * (*it1)) /*% ((1<<16) -1)*/, "failure with *it2 = " << (int)(*it2) << " and 2 * (*it1) *  (*it1) = " << static_cast<image_type::pixel_type>(2 * (*it1) * (*it1)) /*% ((1<<16) -1)*/);
  }

  PrepareImages();
  op.count = 0;
  BOOST_CHECK(op_im(im1, im1, im1, op) == yaRC_ok);
  BOOST_CHECK_MESSAGE(op.count == 6*5, "Number of counted operations " << op.count << " !=  " << 6*5);
  
  for(image_type::const_iterator it1 = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it1 != ite; ++it1, ++it2) {
    BOOST_CHECK_MESSAGE(*it1 == static_cast<image_type::pixel_type>(2 * (*it2) * (*it2)) /*% ((1<<16) -1)*/, "failure with *it1 = " << (int)(*it1) << " and 2 * (*it2) *  (*it2) = " << static_cast<image_type::pixel_type>(2 * (*it2) * (*it2)) /*% ((1<<16) -1)*/);
  }
}


BOOST_AUTO_TEST_CASE(test_image_windowed_unary_application_no_intersection_with_boundaries)
{
  s_two_times op;
  
  // Adapting the appropriate overloaded method of the object
  boost::function<image_type::pixel_type (const image_type::pixel_type&)> f;
  f = boost::bind(&s_two_times::operator()<image_type::pixel_type, image_type::pixel_type>, &op, _1);
  
  s_apply_unary_operator op_im;

  op.count = 0;
  
  s_hyper_rectangle<2> window(c2D(1,1), c2D(2,2));
  
  for(int i = 0; i < total_number_of_points(im.Size()); i++)
    im.pixel(i) = i;
  
  BOOST_CHECK(op_im(im1, window, im, window, f) == yaRC_ok);
  BOOST_CHECK_MESSAGE(total_number_of_points(window.Size()) == 4, "Number of point mistake " << total_number_of_points(window.Size()) << " !=  " << 4);
  BOOST_CHECK_MESSAGE(op.count == 4, "Number of counted operations " << op.count << " !=  " << 4);
  
  for(image_type::const_iterator it = im1.begin_block(), it2 = im.begin_block(), it3 = im2.begin_block(), ite = im1.end_block(); 
      it != ite; ++it, ++it2, ++it3) 
  {
    if(is_point_inside(window, it.Position()))
    {
      BOOST_CHECK_MESSAGE(*it2 == 2 * (*it), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
      BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));
    }
    else
    {
      BOOST_CHECK_MESSAGE(*it2 == it.Offset(), "failure with it.Offset() = " << (int)(it.Offset()) << " and *it2 = " << *it2 << " - operation made outside the window");
      BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));      
    }
  }
  
}
  
BOOST_AUTO_TEST_CASE(test_image_windowed_unary_application)
{
  s_two_times op;
  
  // Adapting the appropriate overloaded method of the object
  boost::function<image_type::pixel_type (const image_type::pixel_type&)> f;
  f = boost::bind(&s_two_times::operator()<image_type::pixel_type, image_type::pixel_type>, &op, _1);
  
  s_apply_unary_operator op_im;    
  s_hyper_rectangle<2> window(c2D(1,1), c2D(2,2));    
  
 
  // In this run, the size of the windows (input and output) are not the same
  // The number of operations is limited by the smallest window intersecting the image on which it is applied,
  // the geometry of the window is preserved in the processing sequence.
  // This means that the output image should be something like this:
  
  static const std::string s = 
    "0 1 2 3 4 5 "
    "6 7 8 9 10 11 "
    "12 13 14 15 16 17 "
    "18 19 20 14 16 24 " // 14 16 24 come from 7, 8, 12 (lines index 1 and 2 positions (1,1), (1,2), (2, 1))
    "24 25 26 26 28 29 "; // the second 26 comes from 13 (line index 2 position (2, 2))
  
  std::istringstream is(s);
  BOOST_REQUIRE_MESSAGE(is >> im2, "Error during the input streaming of the image");
  
  
  
  
  op.count = 0;
  s_hyper_rectangle<2> window2(c2D(3,3), c2D(3,3));
  for(int i = 0; i < total_number_of_points(im.Size()); i++)
    im.pixel(i) = i;

  BOOST_CHECK(op_im(im1, window, im, window2, f) == yaRC_ok);
  BOOST_CHECK_MESSAGE(op.count == 4, "Number of counted operations " << op.count << " !=  " << 4);

  for(image_type::const_iterator it = im1.begin_block(), it2 = im.begin_block(), it3 = im2.begin_block(), ite = im1.end_block(); 
      it != ite; ++it, ++it2, ++it3) 
  {
    BOOST_CHECK_MESSAGE(*it2 == *it3, "Error detected at position " << it2.Position() << " output = " << *it2 << " != " << *it3);
  }


}

BOOST_AUTO_TEST_CASE(test_image_windowed_unary_application_intersection_with_boundary)
{
  s_two_times op;
  
  // Adapting the appropriate overloaded method of the object
  boost::function<image_type::pixel_type (const image_type::pixel_type&)> f;
  f = boost::bind(&s_two_times::operator()<image_type::pixel_type, image_type::pixel_type>, &op, _1);
  
  s_apply_unary_operator op_im;    
  s_hyper_rectangle<2> window(c2D(1,1), c2D(2,2)); 
  
  
  s_hyper_rectangle<2> window2(c2D(4,3), c2D(3,3)); // the output intersects with the image boundary: the intersection is taken during the process
  for(int i = 0; i < total_number_of_points(im.Size()); i++)
    im.pixel(i) = i;
  
  op.count = 0;
  BOOST_CHECK(op_im(im1, window, im, window2, f) == yaRC_ok);
  BOOST_CHECK_MESSAGE(op.count == 4, "Number of counted operations " << op.count << " !=  " << 4);
  
  s_hyper_rectangle<2> activity_window(c2D(4,3), c2D(2,2));
  
  int i = 0;
  for(image_type::const_iterator it = im1.begin_block(), it2 = im.begin_block(), it3 = im2.begin_block(), ite = im1.end_block(); 
      it != ite; ++it, ++it2, ++it3) 
  {
    if(is_point_inside(activity_window, it.Position()) && i < 4)
    {
      ++i;
      BOOST_CHECK(is_point_inside(window2, it.Position()));
      BOOST_CHECK_MESSAGE(*it2 == 2 * im1.pixel(it2.Position() - window2.Origin() + window.Origin()), 
        "failure with *it = " << (int)(*it) 
        << " and 2 * im1.pixel(it2.Position() - c2D(4,4) + c2D(1,1)) = " << 2 * im1.pixel(it2.Position() - window2.Origin() + window.Origin())
        << " for position " << it2.Position()
        );
      BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));
    }
    else
    {
      BOOST_CHECK_MESSAGE(*it2 == it.Offset(), 
        "failure with it.Offset() = " << (int)(it.Offset()) 
        << " and *it2 = " << *it2 
        << " at position " << it.Position()
        << " - operation made outside the window");
      BOOST_CHECK_MESSAGE(*it == *it3, "failure of const original with *it (result) = " << (int)(*it) << " and *it3 (original) = " << (int)(*it3));      
    }
  }

  //std::cout << "im1" << std::endl;
  //print_im(std::cout, im1);
  //std::cout << "im" << std::endl;
  //print_im(std::cout, im);    
}

BOOST_AUTO_TEST_SUITE_END()



