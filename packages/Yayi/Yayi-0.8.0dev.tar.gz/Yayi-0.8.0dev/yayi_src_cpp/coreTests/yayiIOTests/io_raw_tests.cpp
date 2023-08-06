


#include "main.hpp"



#include <yayiIO/include/yayi_IO.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>

BOOST_AUTO_TEST_SUITE(raw_io)

BOOST_AUTO_TEST_CASE(write_raw) 
{
  using namespace yayi;

  typedef Image<yaUINT8> image_type;
  image_type im;

  image_type::coordinate_type coord;
  coord[0] = 10;
  coord[1] = 20;
  im.SetSize(coord);

  BOOST_REQUIRE_MESSAGE(im.AllocateImage() == yaRC_ok, "im.AllocateImage() error");

  for(int i = 0; i < coord[0] * coord[1]; i++) {
    im.pixel(i) = i;
  }

  yaRC ret = yayi::IO::writeRAW("test.raw", &im);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "writeRAW error " << ret);

}

BOOST_AUTO_TEST_CASE(read_raw) 
{
  using namespace yayi;

  IImage *im = 0;
  yaRC ret = yayi::IO::readRAW("test.raw", c2D(10, 20), yayi::type(yayi::type::c_scalar, yayi::type::s_ui8), im);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "readRAW error \"" << ret << "\"");

  BOOST_REQUIRE(im != 0);

  BOOST_REQUIRE_MESSAGE(im->IsAllocated(), "im not allocated ?");

  IImage::coordinate_type coord = im->GetSize();
  //BOOST_CHECK_MESSAGE(ret == yaRC_ok, "cannot get the image size " + static_cast<string_type>(ret));
  BOOST_CHECK_MESSAGE(coord.dimension() == 2, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[0] == 10, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[1] == 20, "bad dimension");

  typedef Image<yaUINT8> image_type;
  image_type *im_t = dynamic_cast<image_type*>(im);


  BOOST_CHECK_MESSAGE(im_t != 0, "cast error");

  for(int i = 0; i < coord[0] * coord[1]; i++) {
    BOOST_CHECK_MESSAGE(im_t->pixel(i) == i, "pixel bad value");
  }

  delete im;
}

BOOST_AUTO_TEST_CASE(write_color_raw) 
{
  using namespace yayi;

  typedef Image<pixel8u_3> image_type;
  image_type im;

  image_type::coordinate_type coord;
  coord[0] = 10;
  coord[1] = 20;
  im.SetSize(coord);

  BOOST_REQUIRE_MESSAGE(im.AllocateImage() == yaRC_ok, "im.AllocateImage() error");

  for(int i = 0; i < coord[0] * coord[1]; i++) {
    im.pixel(i)[0] = i;
    im.pixel(i)[1] = i + 20;
    im.pixel(i)[2] = i + 30;
  }

  yaRC ret = yayi::IO::writeRAW("testcolor.raw", &im);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "writeRAW error " << ret);

}

BOOST_AUTO_TEST_CASE(read_color_raw) 
{
  using namespace yayi;


  IImage *im = 0;
  yaRC ret = yayi::IO::readRAW("testcolor.raw", c2D(10, 20), yayi::type(yayi::type::c_3, yayi::type::s_ui8), im);
  BOOST_CHECK_MESSAGE(ret == yaRC_ok, "readRAW error \"" << ret << "\"");

  BOOST_REQUIRE(im != 0);

  BOOST_REQUIRE_MESSAGE(im->IsAllocated(), "im not allocated ?");

  IImage::coordinate_type coord = im->GetSize();
  //BOOST_CHECK_MESSAGE(ret == yaRC_ok, "cannot get the image size " + static_cast<string_type>(ret));
  BOOST_CHECK_MESSAGE(coord.dimension() == 2, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[0] == 10, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[1] == 20, "bad dimension");

  typedef Image<pixel8u_3> image_type;
  image_type *im_t = dynamic_cast<image_type*>(im);


  BOOST_CHECK_MESSAGE(im_t != 0, "cast error");

  for(int i = 0; i < coord[0] * coord[1]; i++) {
    BOOST_CHECK_MESSAGE(im_t->pixel(i)[0] == i, "pixel bad value");
    BOOST_CHECK_MESSAGE(im_t->pixel(i)[1] == i + 20, "pixel bad value");
    BOOST_CHECK_MESSAGE(im_t->pixel(i)[2] == i + 30, "pixel bad value");
  }

  delete im;
}

BOOST_AUTO_TEST_SUITE_END()
