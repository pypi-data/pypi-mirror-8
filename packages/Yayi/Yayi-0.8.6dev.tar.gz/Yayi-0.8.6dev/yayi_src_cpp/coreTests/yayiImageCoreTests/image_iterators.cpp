#include "main.hpp"
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiImageCore/include/yayiImageUtilities_T.hpp>

#include <yayiImageCore/include/ApplyToImage_T.hpp>

#include <boost/type_traits/is_same.hpp>


#include <iostream>

using namespace yayi;

BOOST_AUTO_TEST_SUITE(image_iterators)

BOOST_AUTO_TEST_CASE(image_iterators_basic_tests)
{
  typedef Image<yaUINT16> image_t;
  image_t im1, im2;
  
  BOOST_REQUIRE(im1.SetSize(c2D(5,5)) == yaRC_ok);
  BOOST_REQUIRE(im1.AllocateImage() == yaRC_ok);
  BOOST_REQUIRE(im2.SetSize(im1.Size()) == yaRC_ok);
  BOOST_REQUIRE(im2.AllocateImage() == yaRC_ok);
  
  // number of points
  int i = 0;
  for(image_t::iterator it = im1.begin_block(), ite = im1.end_block(); it != ite; ++it, i++) {
    *it = 0;
    BOOST_CHECK_MESSAGE(im1.pixel(i) == 0, "failure with *it = 0 at pixel " << i << " : it = " << (int)(*it));
  }
  BOOST_CHECK_MESSAGE(i == 25, "The number of points " << i << " is different from the number of pixels in the image (25)");
  
  
  // same number of points in const and non-const iterators
  image_t::iterator it = im1.begin_block(), ite = im1.end_block();
  image_t::const_iterator itC = im1.begin_block(), iteC = im1.end_block();
  
  i = 0;
  for(; (it != ite) && (itC != iteC); ++it, ++itC, i++) {
    *it = i;
    BOOST_CHECK_MESSAGE(*itC == i, "failure with *it = " << (int)*itC << " != " << i << " at pixel " << i);
  }
  BOOST_CHECK_MESSAGE(i == 25, "The number of points " << i << " is different from the number of pixels in the image (25)");
  BOOST_CHECK_MESSAGE(it == ite, "non-const iterator has not reached the end");
  BOOST_CHECK_MESSAGE(itC == iteC, "const iterator has not reached the end");
  
  
  // test copy constructor of iterators (from non-const to const)
  it = im1.begin_block();
  itC = it;
  
  i = 0;
  for(; (it != ite) && (itC != iteC); ++it, ++itC, i++) {
    *it = i+1;
    BOOST_CHECK_MESSAGE(*itC == i+1, "failure with *it = " << (int)*itC << " != " << i << " at pixel " << i);
  }
  BOOST_CHECK_MESSAGE(i == 25, "The number of points " << i << " is different from the number of pixels in the image (25)");
  BOOST_CHECK_MESSAGE(it == ite, "non-const iterator has not reached the end");
  BOOST_CHECK_MESSAGE(itC == iteC, "const iterator has not reached the end");
  
}

BOOST_AUTO_TEST_CASE(image_iterators_basic_tests2)
{
  typedef Image<yaINT16> image_type;
  image_type im;

  image_type::coordinate_type coord;
  coord[0] = 10;
  coord[1] = 20;
  im.SetSize(coord);
  BOOST_REQUIRE(im.AllocateImage() == yaRC_ok);

  image_type::iterator it = im.begin_block(), ite = im.end_block();
  BOOST_REQUIRE(it.SetPosition(coord) != yaRC_ok);

  int pixel_count = 0;
  for(; it != ite; ++it)
  {
    //std::cout << "iterator position : " << it.Position() << std::endl;

    *it = pixel_count;
    pixel_count++;
  }

  BOOST_CHECK_MESSAGE(pixel_count == total_number_of_points(coord), "Bad number of points parsed : " + int_to_string(pixel_count) + std::string(" != ") + int_to_string(total_number_of_points(coord)));
  //BOOST_CHECK_MESSAGE(it.Position() == im.Size(), "Bad stop position " + any_to_string(it.Position()) + std::string(" != ") + any_to_string(im.Size()));

  image_type::coordinate_type::scalar_coordinate_type coord_tab[] = {9,19};
  const image_type::coordinate_type coord_check = image_type::coordinate_type::from_table(coord_tab);
  BOOST_CHECK_MESSAGE(im.pixel(coord_check) == 199, "Bad value at last position" + int_to_string(im.pixel(coord_check)) + std::string(" != ") + int_to_string(199));
}

BOOST_AUTO_TEST_CASE(image_iterators_basic_tests3)
{
  typedef Image<yaUINT16> image_t;
  image_t im1;
  
  BOOST_REQUIRE(im1.SetSize(c2D(5,5)) == yaRC_ok);
  image_t::iterator it, ite;
  
  #ifndef NDEBUG
  BOOST_CHECK_THROW(it = im1.begin_block(), errors::yaException);
  BOOST_CHECK_THROW(ite = im1.end_block(),  errors::yaException);
  #endif
  
  image_t::interface_iterator Iit = im1.begin(), Iite = im1.end();
  BOOST_CHECK_MESSAGE(Iit == 0, "the returned iterator on unallocated image seems to be valid");
  BOOST_CHECK_MESSAGE(Iite == 0, "the returned iterator on unallocated image seems to be valid");

  BOOST_REQUIRE(it.SetPosition(c2D(1,1)) != yaRC_ok);

  
  BOOST_REQUIRE(im1.AllocateImage() == yaRC_ok);
  Iit = im1.begin();
  Iite = im1.end();
  BOOST_CHECK_MESSAGE(Iit != 0, "the returned iterator on allocated image seems to be non valid");
  BOOST_CHECK_MESSAGE(Iite != 0, "the returned iterator on allocated image seems to be non valid");
  
  delete Iit; delete Iite;
  
}


BOOST_AUTO_TEST_CASE(image_iterators_random_access)
{
  typedef Image<yaINT16> image_type;
  image_type im;

  image_type::coordinate_type coord;
  coord[0] = 10;
  coord[1] = 20;
  im.SetSize(coord);
  BOOST_REQUIRE(im.AllocateImage() == yaRC_ok);

  image_type::iterator it = im.begin_block(), ite = im.end_block();
  BOOST_REQUIRE(it.SetPosition(coord) != yaRC_ok);

  int pixel_count = 0;
  for(; it != ite; )
  {
    *it = pixel_count;
    pixel_count++;
    if(pixel_count > total_number_of_points(coord))
      break;
    it += 1;
  }

  BOOST_CHECK_MESSAGE(pixel_count == total_number_of_points(coord), "Bad number of points parsed : " + int_to_string(pixel_count) + std::string(" != ") + int_to_string(total_number_of_points(coord)));
  //BOOST_CHECK_MESSAGE(it.Position() == im.Size(), "Bad stop position " + any_to_string(it.Position()) + std::string(" != ") + any_to_string(im.Size()));

  image_type::coordinate_type::scalar_coordinate_type coord_tab[] = {9,19};
  const image_type::coordinate_type coord_check = image_type::coordinate_type::from_table(coord_tab);
  BOOST_CHECK_MESSAGE(im.pixel(coord_check) == 199, "Bad value at last position" + int_to_string(im.pixel(coord_check)) + std::string(" != ") + int_to_string(199));

  it = im.begin_block();
  pixel_count = 0;
  for(; it < ite; )
  {
    for(int i = 0; i < coord[0]; i++)
      it[i] = (pixel_count + i) % 7;
    
    pixel_count += coord[0];
    if(pixel_count > total_number_of_points(coord))
      break;
    it += coord[0];
  }

  BOOST_CHECK_MESSAGE(pixel_count == total_number_of_points(coord), "Bad number of points parsed : " + int_to_string(pixel_count) + std::string(" != ") + int_to_string(total_number_of_points(coord)));
  
  BOOST_CHECK_MESSAGE(im.pixel(coord_check) == 199 % 7, "Bad value at last position" + int_to_string(im.pixel(coord_check)) + std::string(" != ") + int_to_string(199 % 7));

}


BOOST_AUTO_TEST_CASE(image_iterators_random_access_operations)
{
  typedef Image<yaINT16> image_type;
  image_type im;

  image_type::coordinate_type coord;
  coord[0] = 10;
  coord[1] = 20;
  im.SetSize(coord);
  BOOST_REQUIRE(im.AllocateImage() == yaRC_ok);

  image_type::iterator it = im.begin_block(), ite = im.end_block();

  BOOST_CHECK_EQUAL(ite - it, total_number_of_points(im.Size()));

  BOOST_REQUIRE(it.SetPosition(coord) != yaRC_ok);

  image_type::const_iterator itc(it), itce(ite);
  BOOST_CHECK(it.GetPosition() == itc.GetPosition());
  BOOST_CHECK(*it == *itc);

  BOOST_CHECK(ite - it == itce - itc);

  image_type::iterator it2 = it + 5;
  BOOST_CHECK(it2 < ++(im.begin_block() + 5));
  BOOST_CHECK(it2 == ++(im.begin_block() + 4));
  BOOST_CHECK(!(++(im.begin_block() + 5) < it2));


  itce = itc = im.begin_block() + 5;
  BOOST_CHECK(itc.GetPosition() == it2.GetPosition());
  BOOST_CHECK(itc == itce);
  BOOST_CHECK(*itc == im.begin_block()[5]);

  ite = it = im.begin_block() + 5;
  BOOST_CHECK(it.GetPosition() == it2.GetPosition());
  BOOST_CHECK(it == ite);
  BOOST_CHECK(*it == im.begin_block()[5]);


  itc = const_cast<image_type const&>(im).begin_block() + 5;
  BOOST_CHECK(itc.GetPosition() == it2.GetPosition());
  BOOST_CHECK(itc == itce);

}

struct s_count
{
  int c;
  s_count() : c(0){}
  template <class T>
  void operator()(T& ) 
  {
    c++;
  }
};

template <class T>
struct s_generator
{
  int i;
  s_generator() : i(0) {}
  T operator()() 
  {
    return static_cast<T>((i++) % 17);
  }
};

// checks the compatibility of the iterators with standard stl operations
BOOST_AUTO_TEST_CASE(image_iterators_random_access_stl_compatibility)
{
  typedef Image<yaINT16> image_type;
  image_type im;

  image_type::coordinate_type coord;
  coord[0] = 10;
  coord[1] = 20;
  im.SetSize(coord);
  BOOST_REQUIRE(im.AllocateImage() == yaRC_ok);

  image_type::iterator it = im.begin_block(), ite = im.end_block();
  
  s_count op = std::for_each(it, ite, s_count());
  BOOST_CHECK(op.c == total_number_of_points(im.Size()));

  std::generate(im.begin_block(), im.end_block(), s_generator<yaINT16>());

  int i = 0;
  for(image_type::iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it, i++) {
    BOOST_CHECK_MESSAGE(im.pixel(i) == i % 17, "failure with *it = " << i % 17<< " at pixel " << i << " : it = " << (int)(*it));
  }


}

BOOST_AUTO_TEST_CASE(image_windowed_iterators_basic_tests)
{
  typedef Image<yaUINT16> image_t;
  image_t im1, im2;
  
  BOOST_REQUIRE(im1.SetSize(c2D(10,10)) == yaRC_ok);
  BOOST_REQUIRE(im1.AllocateImage() == yaRC_ok);
  BOOST_REQUIRE(im2.SetSize(im1.Size()) == yaRC_ok);
  BOOST_REQUIRE(im2.AllocateImage() == yaRC_ok);
  
  // number of points
  int i = 0;
  for(image_t::iterator it = im1.begin_block(), ite = im1.end_block(); it != ite; ++it, i++) {
    *it = i % 11;
    BOOST_CHECK_MESSAGE(im1.pixel(i) == i % 11, "failure with *it = 0 at pixel " << i % 11 << " : it = " << (int)(*it));
  }
  BOOST_CHECK_MESSAGE(i == 100, "The number of points " << i << " is different from the number of pixels in the image (100)");
  
  
  // same number of points in const and non-const iterators
  image_t::window_iterator it = im1.begin_window(c2D(2,2), c2D(5,5)), ite = im1.end_window(c2D(2,2), c2D(5,5));
  image_t::const_window_iterator itC = im1.begin_window(c2D(2,2), c2D(5,5)), iteC = im1.end_window(c2D(2,2), c2D(5,5));
  
  i = 0;
  for(; (it != ite) && (itC != iteC); ++it, ++itC, i++) {
    BOOST_CHECK_MESSAGE(itC.Position()[0] == i % 5 + 2, 
      "failure with iterator position on x : pos_x = " << itC.Position()[0]
      << " != " << i % 5 + 2 << " at offset " << i);
    BOOST_CHECK_MESSAGE(it.Position()[0] == i % 5 + 2, 
      "failure with iterator position on x : pos_x = " << itC.Position()[0]
      << " != " << i % 5 + 2 << " at offset " << i);
    BOOST_CHECK_MESSAGE(itC.Position()[1] == i / 5 + 2, 
      "failure with iterator position on x : pos_x = " << itC.Position()[1]
      << " != " << i / 5 + 2 << " at offset " << i);
    BOOST_CHECK_MESSAGE(it.Position()[1] == i / 5 + 2, 
      "failure with iterator position on x : pos_x = " << itC.Position()[1]
      << " != " << i / 5 + 2 << " at offset " << i);


    BOOST_CHECK_MESSAGE(*itC == itC.Offset() % 11, "failure with *it = " << (int)*itC << " != " << itC.Offset() % 11 << " at pixel " << itC.Position() << " (number " << i << " of the loop)");
    BOOST_CHECK_MESSAGE((itC.Position()[0] >= 2) && (itC.Position()[0] < 2+5), "failure of the position of the iterator along x = " << itC.Position() << " outside [2,7[" << " (number " << i << " of the loop)");
    BOOST_CHECK_MESSAGE((itC.Position()[1] >= 2) && (itC.Position()[1] < 2+5), "failure of the position of the iterator along y = " << itC.Position() << " outside [2,7[" << " (number " << i << " of the loop)");
    
    BOOST_CHECK_MESSAGE(itC.Position()[0] == 2 + i % 5, "failure of the position of the iterator along x = " << itC.Position() << " != " << 2 + i % 5 << " (number " << i << " of the loop)");
    BOOST_CHECK_MESSAGE(itC.Position()[1] == 2 + i / 5, "failure of the position of the iterator along y = " << itC.Position() << " != " << 2 + i / 5 << " (number " << i << " of the loop)");
    
  }
  BOOST_CHECK_MESSAGE(i == 25, "The number of points " << i << " is different from the number of pixels in the window (25)");
  BOOST_CHECK_MESSAGE(it == ite, "non-const iterator has not reached the end");
  BOOST_CHECK_MESSAGE(itC == iteC, "const iterator has not reached the end");
  
  
  // test copy constructor of iterators (from non-const to const)
  it = im1.begin_window(c2D(2,2), c2D(5,5));
  itC = it;
  
  i = 0;
  for(; (it != ite) && (itC != iteC); ++it, ++itC, i++) {
    *it = i+1;
    BOOST_CHECK_MESSAGE(*itC == i+1, "failure with *it = " << (int)*itC << " != " << i << " at pixel " << i);
  }
  BOOST_CHECK_MESSAGE(i == 25, "The number of points " << i << " is different from the number of pixels in the block (25)");
  BOOST_CHECK_MESSAGE(it == ite, "non-const iterator has not reached the end");
  BOOST_CHECK_MESSAGE(itC == iteC, "const iterator has not reached the end");
  
  #ifndef NDEBUG
  BOOST_CHECK_THROW(im1.begin_window(c2D(2,2), c2D(5,6)) == ite, yayi::errors::yaException);
  BOOST_CHECK_THROW(im1.begin_window(c2D(2,2), c2D(5,6)) != ite, errors::yaException);
  #endif
  
}


BOOST_AUTO_TEST_CASE(image_windowed_iterators_basic_tests2)
{
  // test correct crop of the windows on the image support
  typedef Image<yaUINT16> image_t;
  image_t im1, im2;
  
  BOOST_REQUIRE(im1.SetSize(c2D(10,10)) == yaRC_ok);
  BOOST_REQUIRE(im1.AllocateImage() == yaRC_ok);
  BOOST_REQUIRE(im2.SetSize(im1.Size()) == yaRC_ok);
  BOOST_REQUIRE(im2.AllocateImage() == yaRC_ok);
  
  // number of points
  int i = 0;
  for(image_t::iterator it = im1.begin_block(), ite = im1.end_block(); it != ite; ++it, i++) {
    *it = i % 11;
    BOOST_CHECK_MESSAGE(im1.pixel(i) == i % 11, "failure with *it = 0 at pixel " << i % 11 << " : it = " << (int)(*it));
  }
  BOOST_CHECK_MESSAGE(i == 100, "The number of points " << i << " is different from the number of pixels in the image (100)");
  
  
  // same number of points in const and non-const iterators
  image_t::window_iterator it = im1.begin_window(c2D(2,2), c2D(9,9)), ite = im1.end_window(c2D(2,2), c2D(9,9));
  image_t::const_window_iterator itC = im1.begin_window(c2D(2,2), c2D(9,9)), iteC = im1.end_window(c2D(2,2), c2D(9,9));
  
  i = 0;
  for(; (it != ite) && (itC != iteC); ++it, ++itC, i++) {
    BOOST_CHECK_MESSAGE(itC.Position()[0] == i % 8 + 2, 
      "failure with iterator position on x : pos_x = " << itC.Position()[0]
      << " != " << i % 8 + 2 << " at offset " << i);
    BOOST_CHECK_MESSAGE(it.Position()[0] == i % 8 + 2, 
      "failure with iterator position on x : pos_x = " << itC.Position()[0]
      << " != " << i % 8 + 2 << " at offset " << i);
    BOOST_CHECK_MESSAGE(itC.Position()[1] == i / 8 + 2, 
      "failure with iterator position on x : pos_x = " << itC.Position()[1]
      << " != " << i / 8 + 2 << " at offset " << i);
    BOOST_CHECK_MESSAGE(it.Position()[1] == i / 8 + 2, 
      "failure with iterator position on x : pos_x = " << itC.Position()[1]
      << " != " << i / 8 + 2 << " at offset " << i);

  }
  BOOST_CHECK_MESSAGE(i == 64, "The number of points " << i << " is different from the number of pixels in the window (25)");
  BOOST_CHECK_MESSAGE(it == ite, "non-const iterator has not reached the end");
  BOOST_CHECK_MESSAGE(itC == iteC, "const iterator has not reached the end");
  
  
}


// check random access of window iterators
BOOST_AUTO_TEST_CASE(image_windowed_iterators_random_access_operations)
{
  typedef Image<yaINT16> image_type;
  image_type im;

  image_type::coordinate_type coord;
  coord[0] = 10;
  coord[1] = 20;
  im.SetSize(coord);
  BOOST_REQUIRE(im.AllocateImage() == yaRC_ok);

  s_hyper_rectangle<image_type::coordinate_type::static_dimensions> h(c2D(2,2), c2D(9,9));

  image_type::window_iterator it = im.begin_window(h.Origin(), h.Size()), ite = im.end_window(h.Origin(), h.Size());

  BOOST_CHECK_EQUAL(ite - it, total_number_of_points(h));

  BOOST_REQUIRE(it.SetPosition(coord) != yaRC_ok);

  image_type::const_window_iterator itc(it), itce(ite);
  BOOST_CHECK(it.GetPosition() == itc.GetPosition());
  BOOST_CHECK(*it == *itc);

  BOOST_CHECK(ite - it == itce - itc);

  image_type::window_iterator it2 = it + 5;
  BOOST_CHECK(it2 < ++(im.begin_window(h.Origin(), h.Size()) + 5));
  BOOST_CHECK(it2 == ++(im.begin_window(h.Origin(), h.Size()) + 4));
  BOOST_CHECK(!(++(im.begin_window(h.Origin(), h.Size()) + 5) < it2));

  itce = itc = im.begin_window(h.Origin(), h.Size()) + 5;
  BOOST_CHECK(itc.GetPosition() == it2.GetPosition());
  BOOST_CHECK(itc == itce);
  BOOST_CHECK(*itc == im.begin_window(h.Origin(), h.Size())[5]);

  ite = it = im.begin_window(h.Origin(), h.Size()) + 5;
  BOOST_CHECK(it.GetPosition() == it2.GetPosition());
  BOOST_CHECK(it == ite);
  BOOST_CHECK(*it == im.begin_window(h.Origin(), h.Size())[5]);


  itc = const_cast<image_type const&>(im).begin_window(h.Origin(), h.Size()) + 5;
  BOOST_CHECK(itc.GetPosition() == it2.GetPosition());
  BOOST_CHECK(itc == itce);

}


BOOST_AUTO_TEST_SUITE_END()

