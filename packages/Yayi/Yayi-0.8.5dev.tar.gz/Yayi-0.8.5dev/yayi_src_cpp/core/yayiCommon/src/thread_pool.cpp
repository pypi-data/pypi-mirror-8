//! @file
//! This file contains the thread pool interface
//! @author Raffi Enficiaud


#include <yayiCommon/common_types.hpp>
#include <yayiCommon/include/thread_pool.hpp>

#include <boost/asio/io_service.hpp>
#include <boost/bind.hpp>
#include <boost/thread/thread.hpp>
#include <boost/thread/recursive_mutex.hpp>
#include <map>


namespace yayi
{

  namespace thread_internal
  {



    struct thread_pool_manager
    {
      boost::asio::io_service ioService;
      // the order is important here, work should appear after ioService
      boost::asio::io_service::work work;
      boost::thread_group threadpool;


      int nb_threads_current;
      std::map<boost::thread::id, boost::thread*> threads_map;
      boost::condition_variable_any condition_;

      // Mutex for protected operations
      typedef boost::recursive_mutex mutex_t;
      // Exclusive lock
      typedef boost::lock_guard<mutex_t> lock_t;

      // Our Mutex
      mutable mutex_t internal_mutex;



      thread_pool_manager() : work(ioService), nb_threads_current(0)
      {
      }

      void peek_free_thread_id(int& counter, boost::thread::id& out_id)
      {
        boost::unique_lock<mutex_t> lock(internal_mutex);

        out_id = boost::this_thread::get_id();
        counter++;
        condition_.notify_one();

        // this call kills the thread from within, without propagating the exception.
        throw boost::thread_interrupted();
      }

      yaRC operator()(int nb_threads)
      {
        boost::unique_lock<mutex_t> lock(internal_mutex);


        if(nb_threads >= nb_threads_current)
        {
          // increase the number of threads
          for(int i = 0; i < nb_threads - nb_threads_current; i++)
          {
            boost::thread* new_thread = threadpool.create_thread(boost::bind(&boost::asio::io_service::run, &ioService));
            threads_map[new_thread->get_id()] = new_thread;
          }
          nb_threads_current = nb_threads;
        }
        else
        {
          int nb_updates(0);

          std::vector<boost::thread::id> removed_threads(nb_threads_current - nb_threads);
          for(int i = 0; i < nb_threads_current - nb_threads; i++)
          {
            ioService.post(boost::bind(&thread_pool_manager::peek_free_thread_id, this, boost::ref(nb_updates), boost::ref(removed_threads[i])));
          }

          // we wait for nb_threads_current - nb_threads removals

          while (nb_updates < nb_threads_current - nb_threads)
          {
            // when entering wait, the lock is unlocked and made available to other threads.
            // when awakened, the lock is locked before wait returns. 
            condition_.wait(lock);

          }

          // removing the freed threads
          for(int i = 0; i < nb_threads_current - nb_threads; i++)
          {
            boost::thread* removed_thread = threads_map[removed_threads[i]];
            if(removed_thread)
            {
              threadpool.remove_thread(removed_thread);
              delete removed_thread;
            }
          }

          // update the number of current threads
          nb_threads_current = nb_threads;

        }
        return yaRC_ok;
      }

      // Size of the current thread pool
      std::size_t size() const
      {
        return threadpool.size();
      }


      // Releases the thread pool and wait for completion
      ~thread_pool_manager()
      {
        ioService.stop();
        threadpool.join_all();
      }


    };


    thread_pool_manager manager;

  }


  yaRC set_thread_pool_size(int i)
  {
    // we should wait until the active processes finish
    return thread_internal::manager(i);
  }

  std::size_t get_thread_pool_size()
  {
    return thread_internal::manager.size();
  }
}