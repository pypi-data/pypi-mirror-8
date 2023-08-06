
#if YAYI_IO_HDF5_ENABLED__

#include "main.hpp"
#include <yayiIO/include/yayi_IO.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiCommonCoreTests/data_path_for_tests.hpp>

BOOST_AUTO_TEST_SUITE(hdf5_io)

BOOST_AUTO_TEST_CASE(read_hdf5) 
{
  using namespace yayi;


  std::auto_ptr<IImage> im;

  std::string im_file_name(get_data_from_data_path("debug_HDF5.h5"));
  //std::string im_file_name(get_data_from_data_path("wt_K_4ora_colchcine60_RAM2.h5"));
  BOOST_TEST_MESSAGE("Reading the image " + im_file_name);

  //yaRC ret = yayi::IO::readHDF5(im_file_name, im, "/rawdata/stitched_weighted_ch0/");
  yaRC ret = yayi::IO::readHDF5(im_file_name, im.get(), "bla");
  BOOST_REQUIRE_MESSAGE(ret == yaRC_ok, "read error " + static_cast<string_type>(ret));

  BOOST_REQUIRE_MESSAGE(im->IsAllocated(), "im not allocated ?");

  IImage::coordinate_type coord = im->GetSize();
  //BOOST_CHECK_MESSAGE(ret == yaRC_ok, "cannot get the image size " + static_cast<string_type>(ret));
  BOOST_CHECK_MESSAGE(coord.dimension() == 3, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[0] == 10, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[1] == 10, "bad dimension");
  BOOST_CHECK_MESSAGE(coord[2] == 10, "bad dimension");

  typedef Image<yaF_simple, s_coordinate<3> > image_type;
  image_type *im_t = dynamic_cast<image_type*>(im.get());

  BOOST_REQUIRE_MESSAGE(im_t != 0, "cast error");

  int i = 0;
  for(int z = 0; z < coord[2] && i < 10*10*10; z++)
  {
    for(int y = 0; y < coord[1]; y++)
    {
      for(int x = 0; x < coord[0]; x++, i++)
      {
        BOOST_CHECK_MESSAGE(im_t->pixel(i) == x * y * z, "pixel bad value " << im_t->pixel(i) << " (read) != " << x * y * z << " (theory)" );
      }
    }
  }
}



#endif
