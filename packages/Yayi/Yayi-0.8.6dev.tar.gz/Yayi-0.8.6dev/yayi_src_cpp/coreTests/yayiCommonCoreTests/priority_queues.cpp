#include "main.hpp"

#include <yayiCommon/common_priority_queues.hpp>

BOOST_AUTO_TEST_SUITE(priority_queue)

BOOST_AUTO_TEST_CASE(generic_priority_queue)
{
  typedef yayi::priority_queue_t<int, int> pq_t;
  pq_t pq;
  for(int i = 0; i < 100; i++)
  {
    pq.insert(i/10, i);
  }
  
  BOOST_CHECK(pq.size() == 100);
  BOOST_CHECK(pq.number_keys() == 10);
  BOOST_CHECK(pq.min_key() == 0);
  BOOST_CHECK(!pq.empty());
  
  int count = 10;
  for(pq_t::plateau_const_iterator_type it(pq.begin_top_plateau()), ite(pq.begin_top_plateau()); it != ite; ++it)
  {
    BOOST_CHECK(it.key() == 0);
    BOOST_CHECK(*it == count++);
  }
  BOOST_CHECK(count == 10);
  
}

BOOST_AUTO_TEST_SUITE_END()