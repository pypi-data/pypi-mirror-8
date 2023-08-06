#include "main.hpp"
#include <yayiCommon/common_histogram.hpp>
#include <yayiCommon/common_variant.hpp>

BOOST_AUTO_TEST_SUITE(histograms)

BOOST_AUTO_TEST_CASE(histogram_8bits)
{
  using namespace yayi;
  typedef s_histogram_t<yaUINT8, yaUINT16> histogram_type;
  typedef s_histogram_t<yaUINT16, yaUINT16> histogram16_type;

  histogram_type hist;
  BOOST_CHECK_MESSAGE(hist.max_bin() == 0, "max_bin = " << (int)hist.max_bin() << " != 0 (theory)");
  BOOST_CHECK_MESSAGE(hist.min_bin() == 255, "min_bin = " << (int)hist.min_bin() << " != 255 (theory)");

  hist[255]++;

  BOOST_CHECK_MESSAGE(hist.max_bin() == 255, "max_bin = " << (int)hist.max_bin() << " != 255 (theory)");
  BOOST_CHECK_MESSAGE(hist.min_bin() == 255, "min_bin = " << (int)hist.min_bin() << " != 255 (theory)");
  BOOST_CHECK_MESSAGE(hist.sum() == 1, "sum = " << (double)hist.sum() << " != 1 (theory)");

  hist[128]++;
  BOOST_CHECK_MESSAGE(hist.max_bin() == 255, "max_bin = " << (int)hist.max_bin() << " != 255 (theory)");
  BOOST_CHECK_MESSAGE(hist.min_bin() == 128, "min_bin = " << (int)hist.min_bin() << " != 128 (theory)");
  BOOST_CHECK_MESSAGE(hist.sum() == 2, "sum = " << (double)hist.sum() << " != 2 (theory)");

  histogram16_type hist16;
  BOOST_CHECK_MESSAGE(hist16.max_bin() == 0, "max_bin = " << (int)hist16.max_bin() << " != 0 (theory)");
  BOOST_CHECK_MESSAGE(hist16.min_bin() == (1<<16)-1, "min_bin = " << (int)hist16.min_bin() << " != "<< ((1<<16)-1) << " (theory)");

  hist16[255]++;
  BOOST_CHECK_MESSAGE(hist16.max_bin() == 255, "max_bin = " << (int)hist16.max_bin() << " != 255 (theory)");
  BOOST_CHECK_MESSAGE(hist16.min_bin() == 255, "min_bin = " << (int)hist16.min_bin() << " != 255 (theory)");
  BOOST_CHECK_MESSAGE(hist16.sum() == 1, "sum = " << (double)hist16.sum() << " != 1 (theory)");

  hist16[((1<<16)-1)]++;
  BOOST_CHECK_MESSAGE(hist16.max_bin() == std::numeric_limits<yaUINT16>::max(), "max_bin = " << (int)hist16.max_bin() << " != "<< std::numeric_limits<yaUINT16>::max() << " (theory)");
  BOOST_CHECK_MESSAGE(hist16.min_bin() == 255, "min_bin = " << (int)hist16.min_bin() << " != 255 (theory)");
  BOOST_CHECK_MESSAGE(hist16.sum() == 2, "sum = " << (double)hist16.sum() << " != 2 (theory)");
}

BOOST_AUTO_TEST_CASE(histogram_8bits_to_variant)
{
  using namespace yayi;
  typedef s_histogram_t<yaUINT8, yaUINT16> histogram_type;

  histogram_type hist;
  BOOST_CHECK_MESSAGE(hist.max_bin() == 0, "max_bin = " << (int)hist.max_bin() << " != 0 (theory)");
  BOOST_CHECK_MESSAGE(hist.min_bin() == 255, "min_bin = " << (int)hist.min_bin() << " != 255 (theory)");

  hist[255]++;

  BOOST_CHECK_MESSAGE(hist.max_bin() == 255, "max_bin = " << (int)hist.max_bin() << " != 255 (theory)");
  BOOST_CHECK_MESSAGE(hist.min_bin() == 255, "min_bin = " << (int)hist.min_bin() << " != 255 (theory)");

  yayi::variant v = hist;
  std::vector<std::pair<yaUINT8, yaUINT16> > vv = v;
  BOOST_REQUIRE_MESSAGE(vv.size() == 1, "size = " << vv.size() << " != 1 (theory)");
  BOOST_CHECK_MESSAGE(vv[0].first == 255, "first element = " << vv[0].first << " != 255 (theory)");
}

BOOST_AUTO_TEST_CASE(histogram_16bits_to_variant)
{
  using namespace yayi;
  typedef s_histogram_t<yaUINT16, yaUINT16> histogram_type;

  histogram_type hist;
  BOOST_CHECK_MESSAGE(hist.max_bin() == 0, "max_bin = " << (int)hist.max_bin() << " != 0 (theory)");
  BOOST_CHECK_MESSAGE(hist.min_bin() == std::numeric_limits<yaUINT16>::max(), "min_bin = " << (int)hist.min_bin() << " != " << std::numeric_limits<yaUINT16>::max() << " (theory)");

  hist[255]++;

  BOOST_CHECK_MESSAGE(hist.max_bin() == 255, "max_bin = " << (int)hist.max_bin() << " != 255 (theory)");
  BOOST_CHECK_MESSAGE(hist.min_bin() == 255, "min_bin = " << (int)hist.min_bin() << " != 255 (theory)");

  yayi::variant v = hist;
  std::vector<std::pair<yaUINT8, yaUINT16> > vv = v;
  BOOST_REQUIRE_MESSAGE(vv.size() == 1, "size = " << vv.size() << " != 1 (theory)");
  BOOST_CHECK_MESSAGE(vv[0].first == 255, "first element = " << vv[0].first << " != 255 (theory)");
}

BOOST_AUTO_TEST_SUITE_END()
