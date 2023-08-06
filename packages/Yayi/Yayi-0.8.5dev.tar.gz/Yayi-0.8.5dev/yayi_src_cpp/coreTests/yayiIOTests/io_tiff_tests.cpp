
#include "main.hpp"
#include <boost/test/parameterized_test.hpp>
#include <yayiIO/include/yayi_IO.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiCommonCoreTests/data_path_for_tests.hpp>




BOOST_AUTO_TEST_SUITE(tiff_io)

struct test_data
{
  yayi::type image_type;
  bool should_fail;
  const std::string filename;
};



struct fixture_tiff_test
{
  yayi::IImage *im;
  
  fixture_tiff_test() : im(0) 
  {}
  
  ~fixture_tiff_test()
  {
    delete im;
  }
  
  void ReadTIFFTest(test_data const& test_param) 
  {
    using namespace yayi;
    BOOST_CHECKPOINT("test tiff read");

    std::string im_file_name(get_data_from_data_path("libtiff/" + test_param.filename));
    yaRC ret = yayi::IO::readTIFF(im_file_name, 0, im);

    if(!test_param.should_fail)
    {
      BOOST_CHECK_MESSAGE(ret == yaRC_ok, "read error: " + static_cast<string_type>(ret) + " / file: " + test_param.filename);

      BOOST_REQUIRE_MESSAGE(im != 0, "null image");
      BOOST_REQUIRE_MESSAGE(im->IsAllocated(), "im not allocated ?");
      BOOST_CHECK_MESSAGE(im->DynamicType() == test_param.image_type, "image of the wrong type image:" << im->DynamicType() << " / should be: " << test_param.image_type);

      BOOST_CHECK_MESSAGE(yayi::IO::writeRAW(std::string("./test_") + test_param.filename + ".raw", im) == yaRC_ok, "failed to write the image into raw");

    }
    else
    {
      BOOST_CHECK_MESSAGE(ret != yaRC_ok, "read error (should fail): " + static_cast<string_type>(ret) + " / file: " + test_param.filename );
      BOOST_REQUIRE_MESSAGE(im == 0, "null image (should fail)");
    }

  /*
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

  */
  }  
};

BOOST_FIXTURE_TEST_SUITE(read_tiff, fixture_tiff_test)
const test_data tiff_files[] = {
  {yayi::to_type<yayi::yaUINT8>(),    false, "minisblack-1c-8b.tiff"},
  {yayi::to_type<yayi::pixel8u_3>(),  false, "rgb-3c-8b.tiff"},
  {yayi::to_type<yayi::pixel8u_3>(),  false, "quad-tile.jpg.tiff"},
  {yayi::to_type<yayi::pixel8u_3>(),  false, "release-grosse bouche_tiled.tiff"},
  {yayi::to_type<yayi::pixel8u_3>(),  false, "release-grosse bouche_planar_big_endian_zip.tiff"},
  {yayi::to_type<yayi::pixel8u_4>(),  false, "release-grosse bouche_interleaved_big_endian_zip_cmyk.tiff"},
  {yayi::to_type<yayi::pixel16u_4>(), false, "release-grosse bouche_interleaved_big_endian_zip_cmyk16bits.tiff"},
  {yayi::to_type<yayi::pixelFs_3>(),  false, "release-grosse bouche_interleaved_big_endian_zip_rgbFloat32bits.tiff"},
  {yayi::to_type<yayi::pixelFs_3>(),  true,  "release-grosse bouche_interleaved_big_endian_zip_rgbFloat16bits.tiff"}
};

// waiting for the BOOST_AUTO_PARAM_TEST_CASE here

BOOST_AUTO_TEST_CASE(minisblack_1c_8b)
{
  this->ReadTIFFTest(tiff_files[0]);
}

BOOST_AUTO_TEST_CASE(rgb_3c_8b)
{
  this->ReadTIFFTest(tiff_files[1]);
}

BOOST_AUTO_TEST_CASE(quad_tile)
{
  this->ReadTIFFTest(tiff_files[2]);
}

BOOST_AUTO_TEST_CASE(tiled)
{
  this->ReadTIFFTest(tiff_files[3]);
}

BOOST_AUTO_TEST_CASE(planar_big_endian_zip)
{
  this->ReadTIFFTest(tiff_files[4]);
}

BOOST_AUTO_TEST_CASE(interleaved_big_endian_zip_cmyk)
{
  this->ReadTIFFTest(tiff_files[5]);
}

BOOST_AUTO_TEST_CASE(interleaved_big_endian_zip_cmyk16bits)
{
  this->ReadTIFFTest(tiff_files[6]);
}

BOOST_AUTO_TEST_CASE(interleaved_big_endian_zip_rgbFloat32bits)
{
  this->ReadTIFFTest(tiff_files[7]);
}

BOOST_AUTO_TEST_CASE(interleaved_big_endian_zip_rgbFloat16bits)
{
  this->ReadTIFFTest(tiff_files[8]);
}

BOOST_AUTO_TEST_SUITE_END()




namespace 
{
  template <class P>
  void addForTest(P& p, const int i) 
  {
    p += i;
  }

  template <class T, class I>
  void addForTest(yayi::s_compound_pixel_t<T, I>& p, const int i) 
  {
    p[0] += i;
  }

  template <class T>
  T const & to_string(T const &t){return t;}

  inline int to_string(char const &t){return t;}
  inline int to_string(unsigned char const &t){return t;}
}

typedef boost::mpl::list<
  yayi::yaUINT8, yayi::yaUINT16, yayi::yaUINT32, yayi::yaUINT64,
  yayi::yaINT8, yayi::yaINT16, yayi::yaINT32, yayi::yaINT64,
  yayi::yaF_simple, yayi::yaF_double,

  yayi::pixel8u_3, yayi::pixel16u_3,
  yayi::pixel8u_4, yayi::pixel16u_4,

  yayi::pixelFs_3, yayi::pixelFd_3
  > test_types;


BOOST_AUTO_TEST_CASE_TEMPLATE(WriteTIFFTest, pixel_type, test_types)
{
  using namespace yayi;

  typedef Image<pixel_type> image_t;
  image_t im;
  im.SetSize(c2D(100, 100));
  BOOST_REQUIRE_EQUAL(im.AllocateImage(), yaRC_ok);

  pixel_type p = 0;
  for(typename image_t::iterator it(im.begin_block()), ite(im.end_block()); it != ite; ++it, addForTest(p, 1)/*+= 1*/)
  {
    *it = p;
  }

  BOOST_CHECK_EQUAL(yayi::IO::writeTIFF("test_im.tiff", &im), yaRC_ok);


  IImage *im2 = 0;

  BOOST_REQUIRE_EQUAL(yayi::IO::readTIFF("test_im.tiff", 0, im2), yaRC_ok);

  std::auto_ptr<IImage> p_im2(im2);
  BOOST_REQUIRE_NE(im2, (IImage *)0);

  image_t *im2t = dynamic_cast<image_t*>(im2);
  BOOST_REQUIRE_NE(im2t, (image_t*)0);

  p = 0;
  for(typename image_t::iterator it(im2t->begin_block()), ite(im2t->end_block()); it != ite; ++it, addForTest(p, 1)/*p+= 1*/)
  {
    BOOST_CHECK_MESSAGE(*it == p, "error at position " << it.Position() << "*it = " << to_string(*it) << " != p = " << to_string(p));
  }

}


BOOST_AUTO_TEST_SUITE_END()
