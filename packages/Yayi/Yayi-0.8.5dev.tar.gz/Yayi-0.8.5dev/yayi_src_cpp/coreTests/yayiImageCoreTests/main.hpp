#ifndef YAYI_IMAGE_CORETESTS_MAIN_HPP__
#define YAYI_IMAGE_CORETESTS_MAIN_HPP__

#include <boost/test/unit_test_suite.hpp>
#include <boost/test/unit_test_log.hpp>
#include <boost/test/unit_test.hpp>
#include <boost/test/framework.hpp>
#include <boost/test/test_tools.hpp>
using boost::unit_test::test_suite;

#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiCommon/include/common_string_utilities.hpp>

template <class o_stream, class U, class V, class W>
o_stream& print_im(o_stream& os, const yayi::Image<U,V,W> &im) {
  typedef yayi::Image<U,V,W> image_t;
  int l = im.Size()[0], i = 0;
  for(typename image_t::const_iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it) {
    os << yayi::int_to_string(*it, 3) << " ";
    ++i;
    if(i >= l)
    {
      i = 0;
      os << std::endl;
    }
  }
  return os;
}  

#endif /* YAYI_IMAGE_CORETESTS_MAIN_HPP__ */

