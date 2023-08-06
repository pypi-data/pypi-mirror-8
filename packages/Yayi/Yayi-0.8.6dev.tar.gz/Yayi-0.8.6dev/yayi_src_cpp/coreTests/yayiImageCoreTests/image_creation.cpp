
#include "main.hpp"
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiImageCore/include/yayiImageUtilities_T.hpp>

#include <boost/mpl/list.hpp>
#include <boost/smart_ptr/scoped_ptr.hpp>

#include <iostream>

using namespace yayi;


BOOST_AUTO_TEST_SUITE(image_lifetime)

BOOST_AUTO_TEST_CASE(construction)
{
  Image<yaINT16> im;

  Image<yaINT16>::coordinate_type coord;

  coord[0] = 0; coord[1] = 0;
  BOOST_CHECK_MESSAGE(im.SetSize(coord) != yaRC_ok, "return is ok while the set dimension is not : coordinate = " << coord);

  coord[0] = 100; coord[1] = 0;
  BOOST_CHECK_MESSAGE(im.SetSize(coord) != yaRC_ok, "return is ok while the set dimension is not : coordinate = " << coord);

  coord[0] = 100; coord[1] = -2;
  BOOST_CHECK_MESSAGE(im.SetSize(coord) != yaRC_ok, "return is ok while the set dimension is not : coordinate = " << coord);

  yaRC res;
  coord[0] = 100; coord[1] = 1;
  res = im.SetSize(coord);
  BOOST_CHECK_MESSAGE(res == yaRC_ok, "return is not ok '" << res << "' while the set dimension is ok : coordinate = " << coord);
  BOOST_CHECK_MESSAGE(im.GetSize() == coord, "set coordinate is different from the get one : set = " << coord << " -- get = " << im.GetSize());

  for(int i = 1; i < 50; i++)
  {
    coord[0] = 10 * i;
    coord[1] = 20 * i;

    res = im.SetSize(coord);
    BOOST_CHECK_MESSAGE(res == yaRC_ok, "return is '" << res << "' instead of 'ok' for coordinate " << coord);

    if(res != yaRC_ok)
      continue;

    res = im.AllocateImage();
    BOOST_CHECK_MESSAGE(res == yaRC_ok, "Allocate failed with coords : " << coord);
    if(res != yaRC_ok)
      continue;
    BOOST_CHECK_MESSAGE(im.Size()[0] == 10 * i, "Bad image size : " << im.Size()[0] << " != " << 10 * i);
    BOOST_CHECK_MESSAGE(im.Size()[1] == 20 * i, "Bad image size : " << im.Size()[1] << " != " << 20 * i);
    BOOST_CHECK(im.IsAllocated());

    res = im.FreeImage();
    BOOST_CHECK_MESSAGE(res == yaRC_ok, "FreeImage failed with coords : " << coord);
    BOOST_CHECK_MESSAGE(im.Size()[0] == 10 * i, "Bad image size : " << im.Size()[0] << " != " << 10 * i);
    BOOST_CHECK_MESSAGE(im.Size()[1] == 20 * i, "Bad image size : " << im.Size()[1] << " != " << 20 * i);
    BOOST_CHECK(!im.IsAllocated());
  }
}

BOOST_AUTO_TEST_CASE(interface_creation)
{
  //! [test_interface_creation]
  yayi::type t = to_type<yaUINT32>();
  boost::scoped_ptr<IImage> im(IImage::Create(t, 2));
  BOOST_REQUIRE_MESSAGE(im.get() != 0, "Image creation error");


  Image<yaUINT32> *im_t = 0;
  im_t = dynamic_cast<Image<yaUINT32>*> (im.get());

  BOOST_CHECK_MESSAGE(im_t != 0, "Unable to cast the image interface into an Image<yaUINT32>");

  im.reset();
  //! [test_interface_creation]
}


typedef boost::mpl::list<
  yaUINT8, yaINT8,
  yaUINT16,yaINT16,
  yaUINT32,yaINT32,

  pixel8u_3, pixel8u_4,
  pixel16u_3, pixel16u_4,
  pixel32u_3, pixel32u_4
> types_to_test;

BOOST_AUTO_TEST_CASE_TEMPLATE(interface_creation_typed, T, types_to_test)
{

  yayi::type t = to_type<T>();
  boost::scoped_ptr<IImage> im(IImage::Create(t, 2));
  BOOST_REQUIRE_MESSAGE(im.get() != 0, "Image creation error");

  typedef Image<T, s_coordinate<2> > im_type;

  im_type *im_t = 0;
  im_t = dynamic_cast<im_type*> (im.get());

  BOOST_CHECK_MESSAGE(im_t != 0, "Unable to cast the image interface into an Image< "<< type_description::type_support<T>::name() << " >");

  typename im_type::coordinate_type coord = c2D(10, 10);

  yaRC res = im->SetSize(coord);
  BOOST_CHECK_MESSAGE(res == yaRC_ok, "SetSize return is '" << res << "' while the set dimension is correct : coordinate = " << coord);

  res = im->AllocateImage();
  BOOST_CHECK_MESSAGE(res == yaRC_ok, "AllocateImage return is '" << res << "' while it should be correct");

  BOOST_CHECK_MESSAGE(im->GetSize() == coord, "Error in image size");

  BOOST_CHECK_MESSAGE(total_number_of_points(im->GetSize()) == 10*10, "Bad number of points");


  typename im_type::const_pixel_type& pc = im_t->pixel(c2D(1,1));
  typename im_type::pixel_type& p = im_t->pixel(c2D(1,1));

  // todo: add an access from the interface

  typename im_type::pixel_type dum = T(2);
  p = dum;
  BOOST_CHECK_MESSAGE(pc == dum, "Error on references : p = " << p << "!= pc " << pc << " (dum " << dum << ")");
  BOOST_CHECK_MESSAGE(pc == T(2), "Error on references : p = " << p << "!= pc " << T(2));

  im.reset();

}

BOOST_AUTO_TEST_CASE_TEMPLATE(interface_creation_typed_4D, T, types_to_test)
{

  yayi::type t = to_type<T>();
  boost::scoped_ptr<IImage> im(IImage::Create(t, 4));
  BOOST_REQUIRE_MESSAGE(im.get() != 0, "Image creation error");

  typedef Image<T, s_coordinate<4> > im_type;

  im_type *im_t = 0;
  im_t = dynamic_cast<im_type*> (im.get());

  BOOST_CHECK_MESSAGE(im_t != 0, "Unable to cast the image interface into an Image< "<< type_description::type_support<T>::name() << " >");

  typename im_type::coordinate_type coord = c4D(10, 10, 5, 5);

  yaRC res = im->SetSize(coord);
  BOOST_CHECK_MESSAGE(res == yaRC_ok, "SetSize return is '" << res << "' while the set dimension is correct : coordinate = " << coord);

  res = im->AllocateImage();
  BOOST_CHECK_MESSAGE(res == yaRC_ok, "AllocateImage return is '" << res << "' while it should be correct");

  BOOST_CHECK_MESSAGE(im->GetSize() == coord, "Error in image size");

  BOOST_CHECK_MESSAGE(total_number_of_points(im->GetSize()) == 10*10*5*5, "Bad number of points");

  typename im_type::const_pixel_type& pc = im_t->pixel(c4D(1,1,1,1));
  typename im_type::pixel_type& p = im_t->pixel(c4D(1,1,1,1));

  typename im_type::pixel_type dum = T(3);
  p = dum;
  BOOST_CHECK_MESSAGE(pc == dum, "Error on references : p = " << p << "!= pc " << pc << " (dum " << dum << ")");
  BOOST_CHECK_MESSAGE(pc == T(3), "Error on references : p = " << p << "!= pc " << T(3));

  im.reset();
}


BOOST_AUTO_TEST_SUITE_END()

