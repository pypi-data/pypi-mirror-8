#define BOOST_TEST_MAIN

#include <boost/test/unit_test_suite.hpp>
#include <boost/test/unit_test_log.hpp>
#include <boost/test/unit_test.hpp>
#include <boost/test/framework.hpp>
#include <boost/test/test_tools.hpp>
using boost::unit_test::test_suite;


#include <boost/tuple/tuple.hpp>
#include <boost/tuple/tuple_io.hpp>

#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiCommon/include/common_time.hpp>

#include <fstream>
#include <cmath>

#include <yayiPixelProcessing/include/image_arithmetics_t.hpp>

struct TimeLogger {
  // test name, nb dimensions, nb pixels, nb_tests, mean time, var time, min time, max time in microseconds
  typedef std::vector< boost::tuple<std::string, int, int, int, boost::tuple<double, double>, boost::tuple<double, double> > > benches_collection_t;
  
  //! The collection of benches
  static benches_collection_t benches;
  
  //! The filename to which the results will be outputed.
  //! The results will be written at program termination.
  static std::string report_filename;
  
  TimeLogger()
  {
  }
  
  //! Tests if the file can be opened.
  static bool open()
  {
    std::ofstream s(report_filename.c_str());
    return s.is_open();
  }
  
  ~TimeLogger()
  {
    std::ofstream s(report_filename.c_str());
    s << boost::tuples::set_open(' ') << boost::tuples::set_close(' ') << boost::tuples::set_delimiter('\t');
    for(benches_collection_t::iterator it(benches.begin()), ite(benches.end()); it != ite; ++it)
    {
      std::cout << *it << std::endl;
      s << *it << std::endl;
    }
  }
  
  static void add_results(std::string const &name, int dimension, int nb_pixels, yayi::time::s_time_elapsed & measurements)
  {
    benches.push_back(boost::make_tuple(
      name,
      dimension,
      nb_pixels,
      measurements.number_of_observations(),
      boost::make_tuple(measurements.mean_variance().first, std::sqrt(measurements.mean_variance().second)),
      boost::make_tuple(measurements.min_max().first, measurements.min_max().second)));
    
    measurements.reset();
  }
};
std::string TimeLogger::report_filename = "";
TimeLogger::benches_collection_t TimeLogger::benches = TimeLogger::benches_collection_t();
BOOST_GLOBAL_FIXTURE( TimeLogger );



BOOST_AUTO_TEST_SUITE( bench_binary_pixel_processors )

#if 0
BOOST_AUTO_TEST_CASE( test_case1 )
{
  BOOST_REQUIRE(TimeLogger::open());
  yayi::time::s_time_elapsed time_meas;
  
  int nb_pixels = 10;
  for(int k = 0; k < 10; k++, nb_pixels *= 10)
  {
    for(int i = 0; i < 20; i++)
    {
      double d = i;
      for(int j = 0; j < nb_pixels; j++)
      {
        d *= j % (i+1);
      }
      
      time_meas.stack_observation();
    }
    
    TimeLogger::add_results("time_meas_test", 1, nb_pixels, time_meas);

  }
}
#endif



BOOST_AUTO_TEST_CASE( bench_predicate_apply_operator_different_images )
{
  const int nb_trials = 10;
  using namespace yayi;
  typedef Image<yaUINT8> image_t;
  
  
  for(int s = 100; s < 10000; s+= 1000)
  {
    image_t im1, im2, imout;
    
    BOOST_CHECK(im1.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(im2.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(imout.SetSize(c2D(s, s)) == yaRC_ok);
    
    BOOST_CHECK(im1.AllocateImage() == yaRC_ok);
    BOOST_CHECK(im2.AllocateImage() == yaRC_ok);
    BOOST_CHECK(imout.AllocateImage() == yaRC_ok);
    
    
    s_predicate_image<
      image_t::pixel_type,
      image_t::pixel_type,
      image_t::pixel_type,
      std::greater<image_t::pixel_type>
    > op;
    s_apply_binary_operator op_processor;

    yayi::time::s_time_elapsed time_meas;
    for(int k = 0; k < nb_trials; k++)
    {
      op_processor(im1, im2, imout, op);
      time_meas.stack_observation();
    }

    TimeLogger::add_results(boost::unit_test::framework::current_test_case().p_name, 2, s*s, time_meas);
  }
  
}

BOOST_AUTO_TEST_CASE( bench_predicate_apply_operator_different_images_manual_1 )
{
  const int nb_trials = 10;
  using namespace yayi;
  typedef Image<yaUINT8> image_t;
  
  
  for(int s = 100; s < 10000; s+= 1000)
  {
    image_t im1, im2, imout;
    
    BOOST_CHECK(im1.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(im2.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(imout.SetSize(c2D(s, s)) == yaRC_ok);
    
    BOOST_CHECK(im1.AllocateImage() == yaRC_ok);
    BOOST_CHECK(im2.AllocateImage() == yaRC_ok);
    BOOST_CHECK(imout.AllocateImage() == yaRC_ok);

    yayi::time::s_time_elapsed time_meas;
    for(int k = 0; k < nb_trials; k++)
    {
      offset nb_pixels = total_number_of_points(im1.Size());
      
      image_t::reference b1 = im1.pixel(0), b2 = im2.pixel(0), bo = imout.pixel(0);
      yaUINT8 * __restrict p1(&b1), * __restrict p2(&b2), * __restrict po(&bo);
#if 1
      for(offset i = 0; i < nb_pixels; i++)
      {
        po[i] = p1[i] > p2[i] ? p1[i] : p2[i];
      }
#else
      // unrolling the loop manually
      for(offset i = 0; i < nb_pixels-16; i+=16)
      {
        for(int j = 0; j < 16; j++)
        {
          po[j] = p1[j] > p2[j] ? p1[j] : p2[j];
        }
        po+= 16;
        p1+= 16;
        p2+= 16;
      }
      for(int j = 0; j < nb_pixels%16; j++)
      {
        po[j] = p1[j] > p2[j] ? p1[j] : p2[j];
      }
      
      // generated code in llvm-apple (sse4a, loop unroll), poor vectorisation
      /*
+0xd10	            movq                %r9, %rcx
+0xd13	            nopw                %cs:(%rax,%rax)
+0xd20	                movb                (%rdi,%rcx), %dl
+0xd23	                movb                (%rbx,%rcx), %al
+0xd26	                cmpb                %dl, %al
+0xd28	                ja                  _ZN29bench_binary_pixel_processorsL64bench_predicate_apply_operator_different_images_manual_1_invokerEv+0xd2c
+0xd2a	                movb                %dl, %al
+0xd2c	                movb                %al, (%rsi,%rcx)
+0xd2f	                incq                %rcx
+0xd32	                cmpl                $16, %ecx
+0xd35	                jne                 _ZN29bench_binary_pixel_processorsL64bench_predicate_apply_operator_different_images_manual_1_invokerEv+0xd20
+0xd37	            addq                $16, %rdi
+0xd3b	            addq                $16, %rbx
+0xd3f	            addq                $16, %rsi
+0xd43	            addq                $16, %rbp
+0xd47	            cmpq                %r10, %rbp
+0xd4a	            jl                  _ZN29bench_binary_pixel_processorsL64bench_predicate_apply_operator_different_images_manual_1_invokerEv+0xd10
      */
      
      // llvm-gcc, not any better
      /*
	            nop                 
+0xd40	                movb                (%r10,%r12), %r13b
+0xd44	                cmpb                %r13b, (%r11,%r12)
+0xd48	                movq                %r10, %r13
+0xd4b	                cmovaq              %r11, %r13
+0xd4f	                movb                (%r13,%r12), %r13b
+0xd54	                movb                %r13b, (%r15,%r12)
+0xd58	                incq                %r12
+0xd5b	                cmpq                $16, %r12
+0xd5f	                jne                 bench_binary_pixel_processors::bench_predicate_apply_operator_different_images_manual_1::test_method()+0xd40
+0xd61	            addq                $16, %r9
+0xd65	            cmpq                %r9, %rax
+0xd68	            jg                  bench_binary_pixel_processors::bench_predicate_apply_operator_different_images_manual_1::test_method()+0xd30
*/
      
#endif
      
      time_meas.stack_observation();
    }

    TimeLogger::add_results(boost::unit_test::framework::current_test_case().p_name, 2, s*s, time_meas);
  }
  
}

BOOST_AUTO_TEST_CASE( bench_predicate_apply_operator_different_images_manual_11 )
{
  const int nb_trials = 10;
  using namespace yayi;
  typedef Image<yaUINT8> image_t;
  
  
  for(int s = 100; s < 10000; s+= 1000)
  {
    image_t im1, im2, imout;
    
    BOOST_CHECK(im1.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(im2.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(imout.SetSize(c2D(s, s)) == yaRC_ok);
    
    BOOST_CHECK(im1.AllocateImage() == yaRC_ok);
    BOOST_CHECK(im2.AllocateImage() == yaRC_ok);
    BOOST_CHECK(imout.AllocateImage() == yaRC_ok);

    yayi::time::s_time_elapsed time_meas;
    for(int k = 0; k < nb_trials; k++)
    {
      offset nb_pixels = total_number_of_points(im1.Size());
      
      image_t::reference b1 = im1.pixel(0), b2 = im2.pixel(0), bo = imout.pixel(0);
      yaUINT8 * __restrict p1(&b1), * __restrict p2(&b2), * __restrict po(&bo);
      yaUINT8 * const p1_end(p1 + nb_pixels);

      for(; p1 < p1_end; ++p1, ++p2, ++po)
      {
        *po = *p1 > *p2 ? *p1 : *p2;
      }      
      time_meas.stack_observation();
    }

    TimeLogger::add_results(boost::unit_test::framework::current_test_case().p_name, 2, s*s, time_meas);
  }
  
}


BOOST_AUTO_TEST_CASE( bench_predicate_apply_operator_different_images_manual_2 )
{
  const int nb_trials = 10;
  using namespace yayi;
  typedef Image<yaUINT8> image_t;
  
  
  std::greater<yaUINT8> op;
  
  for(int s = 100; s < 10000; s+= 1000)
  {
    image_t im1, im2, imout;
    
    BOOST_CHECK(im1.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(im2.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(imout.SetSize(c2D(s, s)) == yaRC_ok);
    
    BOOST_CHECK(im1.AllocateImage() == yaRC_ok);
    BOOST_CHECK(im2.AllocateImage() == yaRC_ok);
    BOOST_CHECK(imout.AllocateImage() == yaRC_ok);

    yayi::time::s_time_elapsed time_meas;
    for(int k = 0; k < nb_trials; k++)
    {
      offset nb_pixels = total_number_of_points(im1.Size());
      
      image_t::reference b1 = im1.pixel(0), b2 = im2.pixel(0), bo = imout.pixel(0);
      yaUINT8 *p1(&b1), *p2(&b2), *po(&bo);
      
      for(offset i = 0; i < nb_pixels; i++)
      {
        po[i] = op(p1[i], p2[i]) ? p1[i] : p2[i];
      }
      
      time_meas.stack_observation();
    }

    TimeLogger::add_results(boost::unit_test::framework::current_test_case().p_name, 2, s*s, time_meas);
  }
  
}

BOOST_AUTO_TEST_CASE( bench_predicate_apply_operator_different_images_manual_22 )
{
  const int nb_trials = 10;
  using namespace yayi;
  typedef Image<yaUINT8> image_t;
  
  
  std::greater<yaUINT8> op;
  
  for(int s = 100; s < 10000; s+= 1000)
  {
    image_t im1, im2, imout;
    
    BOOST_CHECK(im1.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(im2.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(imout.SetSize(c2D(s, s)) == yaRC_ok);
    
    BOOST_CHECK(im1.AllocateImage() == yaRC_ok);
    BOOST_CHECK(im2.AllocateImage() == yaRC_ok);
    BOOST_CHECK(imout.AllocateImage() == yaRC_ok);

    yayi::time::s_time_elapsed time_meas;
    for(int k = 0; k < nb_trials; k++)
    {
      offset nb_pixels = total_number_of_points(im1.Size());
      
      image_t::reference b1 = im1.pixel(0), b2 = im2.pixel(0), bo = imout.pixel(0);
      yaUINT8 * __restrict p1(&b1), *__restrict p2(&b2), * __restrict po(&bo);
      yaUINT8 * const p1_end(p1+nb_pixels);
      
      for(; p1 < p1_end; ++p1, ++p2, ++po)
      {
        *po = op(*p1, *p2) ? *p1 : *p2;
      }
      
      time_meas.stack_observation();
    }

    TimeLogger::add_results(boost::unit_test::framework::current_test_case().p_name, 2, s*s, time_meas);
  }
  
}


BOOST_AUTO_TEST_CASE( bench_predicate_apply_operator_two_similar_images )
{
  const int nb_trials = 10;
  using namespace yayi;
  typedef Image<yaUINT8> image_t;
  
  
  for(int s = 100; s < 10000; s+= 1000)
  {
    image_t im1, im2;
    
    BOOST_CHECK(im1.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(im2.SetSize(c2D(s, s)) == yaRC_ok);
    
    BOOST_CHECK(im1.AllocateImage() == yaRC_ok);
    BOOST_CHECK(im2.AllocateImage() == yaRC_ok);
    
    
    s_predicate_image<
      image_t::pixel_type,
      image_t::pixel_type,
      image_t::pixel_type,
      std::greater<image_t::pixel_type>
    > op;
    s_apply_binary_operator op_processor;

    yayi::time::s_time_elapsed time_meas;
    for(int k = 0; k < nb_trials; k++)
    {
      op_processor(im1, im2, im1, op);
      time_meas.stack_observation();
    }

    TimeLogger::add_results(boost::unit_test::framework::current_test_case().p_name, 2, s*s, time_meas);
  }
  
}

BOOST_AUTO_TEST_CASE( bench_predicate_apply_operator_three_similar_images )
{
  const int nb_trials = 10;
  using namespace yayi;
  typedef Image<yaUINT8> image_t;
  
  for(int s = 100; s < 10000; s+= 1000)
  {
    image_t im1;
    
    BOOST_CHECK(im1.SetSize(c2D(s, s)) == yaRC_ok);
    BOOST_CHECK(im1.AllocateImage() == yaRC_ok);
    
    s_predicate_image<
      image_t::pixel_type,
      image_t::pixel_type,
      image_t::pixel_type,
      std::greater<image_t::pixel_type>
    > op;
    s_apply_binary_operator op_processor;

    yayi::time::s_time_elapsed time_meas;
    for(int k = 0; k < nb_trials; k++)
    {
      op_processor(im1, im1, im1, op);
      time_meas.stack_observation();
    }

    TimeLogger::add_results(boost::unit_test::framework::current_test_case().p_name, 2, s*s, time_meas);
  }
  
}




BOOST_AUTO_TEST_SUITE_END()

#if 0
boost::unit_test::test_suite* init_unit_test_suite( int /*argc*/, char* /*argv*/[] ) 
{
  std::string report_filename = "./toto.txt";
  const int argc = boost::unit_test::framework::master_test_suite().argc;
  if(argc > 1)
  {
    for(int i = 1; i < argc; i++)
    {
      std::string current = boost::unit_test::framework::master_test_suite().argv[i];
      if((current == "-r" || current =="--report") && i < argc - 1)
      {
        report_filename = boost::unit_test::framework::master_test_suite().argv[i+1];
        break;
      }

    }
  }
  TimeLogger::report_filename = report_filename;
  return 0;
}
#endif
