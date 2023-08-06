#include "main.hpp"

#include <yayiCommon/include/thread_pool.hpp>

BOOST_AUTO_TEST_SUITE(thread_pool)

BOOST_AUTO_TEST_CASE(set_nb_threads)
{
  BOOST_CHECK_EQUAL(yayi::get_thread_pool_size(), 0);
  BOOST_CHECK_EQUAL(yayi::set_thread_pool_size(1), yayi::yaRC_ok);
  BOOST_CHECK_EQUAL(yayi::get_thread_pool_size(), 1);

  BOOST_CHECK_EQUAL(yayi::set_thread_pool_size(2), yayi::yaRC_ok);
  BOOST_CHECK_EQUAL(yayi::get_thread_pool_size(), 2);
  
  BOOST_CHECK_EQUAL(yayi::set_thread_pool_size(1), yayi::yaRC_ok);
  BOOST_CHECK_EQUAL(yayi::get_thread_pool_size(), 1);
  

  BOOST_CHECK_EQUAL(yayi::set_thread_pool_size(0), yayi::yaRC_ok);
  BOOST_CHECK_EQUAL(yayi::get_thread_pool_size(), 0);
}

BOOST_AUTO_TEST_SUITE_END()