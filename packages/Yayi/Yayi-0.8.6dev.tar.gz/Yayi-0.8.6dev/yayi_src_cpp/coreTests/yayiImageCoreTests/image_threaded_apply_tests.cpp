




#include "main.hpp"

#include <yayiImageCore/include/yayiImageUtilities_T.hpp>

#include <yayiImageCore/include/ApplyToImage_T.hpp>
#include <yayiImageCore/include/ApplyToImage_unary_t.hpp>
#include <yayiImageCore/include/ApplyToImage_binary_t.hpp>

#include <boost/type_traits/is_same.hpp>
#include <boost/type_traits/is_stateless.hpp>
#include <boost/type_traits/is_same.hpp>

#include <boost/utility/enable_if.hpp>

#include <boost/function.hpp>
#include <boost/bind.hpp>
#include <boost/function_types/parameter_types.hpp>
#include <boost/function_types/is_member_function_pointer.hpp>
#include <boost/function_types/is_member_object_pointer.hpp>
#include <boost/function_types/member_function_pointer.hpp>
#include <boost/function_types/property_tags.hpp>
#include <boost/function_types/components.hpp>
#include <boost/function_types/result_type.hpp>
#include <boost/fusion/include/size.hpp>

#include <iostream>

#include <boost/mpl/push_front.hpp>

#include <boost/thread/thread.hpp>
#include <boost/thread/future.hpp>

#include <boost/mpl/vector.hpp>//TR seems missing
using namespace yayi;


#include <boost/fusion/include/transform.hpp>
#include <boost/fusion/include/make_fused_function_object.hpp>
#include <boost/fusion/include/zip.hpp>
#include <boost/fusion/adapted/mpl.hpp>
#include <boost/fusion/include/make_vector.hpp>
#include <boost/fusion/include/at.hpp>
#include <boost/fusion/include/as_vector.hpp>
#include <boost/fusion/include/for_each.hpp>
#include <boost/fusion/include/copy.hpp>
#include <boost/fusion/include/make_fused_procedure.hpp>
#include <boost/fusion/include/vector_tie.hpp>
#include <boost/fusion/view/joint_view.hpp>
#include <boost/fusion/include/push_front.hpp>
#include <boost/fusion/functional/invocation/invoke_function_object.hpp>
#include <boost/fusion/functional/invocation/invoke.hpp>
#include <boost/fusion/include/single_view.hpp>
#include <boost/fusion/include/fold.hpp>
#include <boost/fusion/include/join.hpp>
#include <boost/fusion/include/deduce_sequence.hpp>
namespace bf = boost::fusion;

#include <boost/scoped_array.hpp>

// for keeping supertype of iterator difference
#include <boost/numeric/conversion/conversion_traits.hpp>

// operators classification utilities
#include <yayiImageCore/include/yayiImageOperatorClassification_t.hpp>


//! Indicates the composition of operators when applied on disjoin sets
//! This structure compose the operator op_ as if several objects op_ were 
//! executed independantly on sets with empty intersection. 
//! The composition can be either commutative and associative, which means the order does not count 
//! (and only a few copy of op_ are instanciated) or without any property, in which case s_operator_composition
//! takes a vector of op_ in order to perform the composition.
//! In all cases, op_ should be copy and default constructible
template <class op_>
struct s_operator_composition
{
  typedef boost::false_type type;
};





// This structure cannot be multithreaded, because of count
// operator() are not const
// The structure is however splittable, and each copy can be joined after having ran concurrently.
struct s_multiply_by_two_multithreaded {
  int count;
  
  template <class T> struct result;
  
  template <class op, class T> struct result<op(T)> {
    typedef void type;
  };
  template <class op, class T> struct result<op(const T&)> {
    typedef T type;
  };
  
  
  template <class T>
  void operator()(T& x) throw() {
    x *= 2;
    count ++;
  }

  template <class T1, class T2>
  T2 operator()(const T1& x) throw() {
    count ++;
    return x * 2;
  }

};

template <>
struct s_operator_composition<s_multiply_by_two_multithreaded> : boost::true_type
{
  typedef s_multiply_by_two_multithreaded T;
  typedef T generated_t;

  template <class distance_t>
  T generate(T const &original, distance_t /*d*/) const
  {
    T ret;
    ret.count = 0;
    return ret;
  }
  
  bool compose(T & initial, T const& r) const
  {
    initial.count += r.count;
    return true;
  }
};

// the calls to operator() can be multithreaded
struct s_three_times_mt {
  typedef yayi::ns_operator_tag::operator_commutative operator_tag;
  typedef void result_type;
  template <class T>
  void operator()(T& x) const throw() {
    x *= 3;
  }
};

// same remark as s_two_times_mt
struct s_square_mt {
  int count;
  
  template <class T> struct result;
  
  template <class op, class T1, class T2> struct result<op(T1, T2)> {
    typedef typename remove_reference<T2>::type type;
  };
  
  
  template <class T1, class T2>
  typename result<s_square_mt(T1, T2)>::type operator()(T1 x, T2 y) {
    count ++;
    return x * x + y * y;
  }
};









struct s_apply_unary_operator_threaded
{
  
public:


  /*! Metafunction enabling the multithreading dispatch by detecting properties of the operator.
   *
   * The metafunction returns true if the operator meets one of the following property:
   * - it is empty (no instance member, but may fail for static variables)
   * - it is const (no possibility to change member variables)
   * - the operator() is const
   * - a specialization of s_operator_composition for this operator exists, and s_operator_composition<op>::type valuates to true_type
   */
  template <class op_t, class it_t>
  struct s_operator_enabling_t
  {
    typedef typename boost::mpl::or_<
      boost::is_empty<op_t>, 
      boost::is_const<op_t>,
      s_operator_is_functor_call_const< boost::mpl::vector<op_t, typename it_t::reference> >,
      s_operator_composition<op_t>
    >::type type;
  };

  /*! Metafunction enabling the multithreading dispatch by detecting properties of the operator.
   *
   * The metafunction returns true if the operator meets one of the following property:
   * - it is empty (no instance member, but may fail for static variables)
   * - it is const (no possibility to change member variables)
   * - the operator() is const when called with it_t::reference (ie. op_t::operator()(it_t::reference) leaves op_t const).
   */
  template <class op_t, class it_t>
  struct s_operator_enabling_no_member_t
  {
    typedef typename boost::mpl::and_<
      boost::mpl::or_<
        boost::is_empty<op_t>, 
        boost::is_const<op_t>,
        s_operator_is_functor_call_const< boost::mpl::vector<op_t, typename it_t::reference> >
      >,
      boost::is_same<typename std::iterator_traits<it_t>::iterator_category, std::random_access_iterator_tag>
    >::type type;
  };
  
  template <class op_t, class ittuples_t>
  struct s_operator_enabling_no_member_tuples_t
  {
    typedef typename
      boost::mpl::not_<
        boost::mpl::contains<
          boost::mpl::transform_view<ittuples_t, s_operator_enabling_no_member_t<op_t, mpl::_1> >, 
          boost::mpl::false_
        > 
      >::type type;

  };  

  /*!@brief Checks the possibility to use the operator composition scheme.
   * 
   * The operator composition is enabled if the following two conditions are met:
   * - a composition operator exists (a specialization of s_operator_composition for which @c 's_operator_composition<op_t>::type' evaluates to true_).
   * - the iterator implements the random_access iterator concept.
   *
   * @tparam op_t the operator type
   * @tparam ittuples_t a tuple of iterator types.
   *
   *
   * Otherwise the operator is not eligible for composition using the provided iterator. 
   */
  template <class op_t, class it_t>
  struct s_operator_enabling_composition_t
  {
    typedef typename boost::mpl::and_<
      s_operator_composition<op_t>,
      boost::is_same<typename std::iterator_traits<it_t>::iterator_category, std::random_access_iterator_tag>
    >::type type;
  };
  
  /*!@brief Checks the s_operator_enabling_composition_t for a set of iterators against an operator.
   * 
   * @tparam op_t the operator type
   * @tparam ittuples_t a tuple of iterator types.
   *
   */
  template <class op_t, class ittuples_t>
  struct s_operator_enabling_composition_tuples_t
  {
    typedef typename 
      boost::mpl::not_<
        boost::mpl::contains<
          boost::mpl::transform_view<ittuples_t, s_operator_enabling_composition_t<op_t, mpl::_1> >, 
          boost::mpl::false_
        > 
      >::type type;
  };

#if 0
  //! Helper functor, for thread
  template <class op_apply_bind_t, class op_ptr_t>
  struct threaded_op_apply_t
  {
    typedef threaded_op_apply_t<op_apply_bind_t, op_ptr_t> this_type;
    op_apply_bind_t op_bind;
    op_ptr_t p_op;
    typename op_apply_bind_t::result_type result;

    //threaded_op_apply_t() {}

    void operator()()
    {
      result = op_bind(*p_op);
    }

  };
  
  
  

  
  //! Utility destroying the created applicators
  //! @todo: delete this structure
  template <class vector_t>
  struct s_vector_cleaner
  {
    vector_t& v;
    s_vector_cleaner(vector_t &v_): v(v_){}
    ~s_vector_cleaner()
    {
      for(typename vector_t::iterator it(v.begin()), ite(v.end()); it != ite; ++it)
        delete it->p_op;
    }
  };

  //! Multithreaded execution of the applicator, provided the operator is const, op_t::operator() is const, or op_t is stateless
  //! This may not work properly when op_t has mutable member accessed in op_t::operator().
  template <class op_apply_t, class op_t, class it_t, class image_in_out>
  typename enable_if<
    typename s_operator_enabling_no_member_t<op_t, it_t>::type,
    yaRC>::type
  apply_stage(op_t& op, it_t it, it_t ite, image_in_out& im) const
  {
    typename std::iterator_traits<it_t>::difference_type const d = ite - it;
    unsigned int const j = NbProcessorUnit() ? std::min(NbProcessorUnit(), boost::thread::hardware_concurrency()) : boost::thread::hardware_concurrency();
    typename std::iterator_traits<it_t>::difference_type const delta = d / j;

    typedef typename boost::add_reference<op_t>::type argument_t;
    
    typedef threaded_op_apply_t< 
      boost::function<typename op_apply_t::result_type (argument_t)>, 
      typename boost::add_pointer<op_t>::type
    > op_apply_mt_t;
    
    typedef std::vector<op_apply_mt_t> vector_t;
    vector_t vect_apply(j);

    it_t ite2 = it + delta;

    boost::thread_group g;
    for(unsigned int i = 0; i < j; i++, ite2 += delta, it += delta)
    {
      vect_apply[i].p_op = &op;
      
      vect_apply[i].op_bind = boost::bind(op_apply_t(), _1, it, (i == j-1 ? ite:ite2), boost::ref(im));

      g.create_thread(boost::ref(vect_apply[i]));
    }

    g.join_all();

    for(unsigned int i = 0; i < j; i++)
    {

      if(vect_apply[i].result != yaRC_ok)
      {
        DEBUG_INFO("Error detected in execution thread " << i << " error = " << vect_apply[i].result);
        return vect_apply[i].result;
      }
    }
    
    // there is nothing to recompose, nothing to free
    return yaRC_ok;
  }


  //! Multithreaded execution of the applicator, provided the exitence of composition the image/pixel operator
  template <class op_apply_t, class op_t, class it_t, class image_in_out>
  typename enable_if<
    typename s_operator_enabling_composition_t<op_t, it_t>::type,
    yaRC>::type
  apply_stage(op_t& op, it_t it, it_t ite, image_in_out& im) const
  {
    typename std::iterator_traits<it_t>::difference_type const d = ite - it;
    unsigned int const j = NbProcessorUnit() ? std::min(NbProcessorUnit(), boost::thread::hardware_concurrency()) : boost::thread::hardware_concurrency();
    typename std::iterator_traits<it_t>::difference_type const delta = d / j;

    typedef s_operator_composition<op_t> compositer_t;

    typedef threaded_op_apply_t< 
      boost::function<typename op_apply_t::result_type (typename boost::add_reference<typename compositer_t::generated_t>::type)>, 
      typename boost::add_pointer<typename compositer_t::generated_t>::type
    > op_apply_mt_t;

    typedef std::vector<op_apply_mt_t> vector_t;
    vector_t vect_apply(j);
    s_vector_cleaner<vector_t> op_cleaner(vect_apply);
    
    compositer_t compositor;

    it_t ite2 = it + delta, it0 = it;

    boost::thread_group g;

    // create intermediate function objects
    for(unsigned int i = 0; i < j; i++, ite2 += delta, it += delta)
    {
      vect_apply[i].p_op = new op_t(compositor.generate(op, it-it0));
      vect_apply[i].op_bind = boost::bind(
        op_apply_t(), 
        _1,
        it, 
        (i == j-1 ? ite:ite2), boost::ref(im));
      g.create_thread(boost::ref(vect_apply[i]));
    }

    // wait for all threads to complete
    g.join_all();

    // check results
    for(unsigned int i = 0; i < j; i++)
    {
      if(vect_apply[i].result != yaRC_ok)
      {
        DEBUG_INFO("Error detected in execution thread #" << i << ": error = " << vect_apply[i].result);
        return vect_apply[i].result;
      }
    }

    // composition, cleaning is done automatically
    for(unsigned int i = 0; i < j; i++)
    {
      compositor.compose(op, *vect_apply[i].p_op);
    }

    return yaRC_ok;
  }
#endif
  
  //! Polymorphic function object for obtaining a single vector from a zip view 
  struct s_super_fold
  {
    template <class T>
    struct result;
    
    template <class S, class E>
    struct result<s_super_fold(S, E)>
    {
      typedef 
        typename bf::traits::deduce_sequence<
          typename bf::result_of::join<
          typename boost::add_const< typename boost::remove_reference<S>::type >::type, 
          E>::type
        >::type type;
    };
    
    template<class S, typename E>
    typename result<s_super_fold(S, E)>::type operator()(S s, E e)
    {
      return typename result<s_super_fold(S, E)>::type(bf::join(s, e));
    }
     
  };  
  
  /*!@brief Function object wrapping the iteration method of pixel functors.  
   *
   * The purpose of this operator is mainly the implementation of a delayed call
   * on the appropriate iteration method for pixel functors (an application method). The implementation 
   * is given by a function object of type operator_on_iterators_t (should be stateless
   * and default constructible, see eg. s_apply_op_range<iterators_same_pointer_and_same_images_tag, operator_type_unary>), which 
   * accepts a number of arguments depending on the number of images and the type of operator. 
   *
   * This function object acts also as an adapter to such application method, since the signatures are slighty different, but always of the 
   * same nature: N pairs of iterators (begin and end), and N images. 
   *
   * It relies on the unfused functionality of boost.fusion.
   * op_t should be a reference to the object, since it is impossible to get back the internal instance otherwise.
   *
   * @author Raffi Enficiaud
   */
  template <
    class operator_on_iterators_t,
    class op_t,
    class iterators_vector_t_, 
    class images_vector_t>
  struct s_call_operator
  {
    //! The result type of operator_on_iterators_t, which is also the result type of this operator
    typedef typename operator_on_iterators_t::result_type result_type;
  
    //! The operator (on images) to be called at each iteration
    //! @note The underlying type is possibly a reference to an operator and possibly mutable (hence operator() cannot be const).
    op_t t;
    
    //! The vector of iterators, respectively for begin and end (boost::fusion sequence type)
    typedef typename bf::traits::deduce_sequence<iterators_vector_t_>::type iterators_vector_t;
    iterators_vector_t its, ites;
  
    //! The vector of images (boost::fusion sequence type)
    images_vector_t& image_vector;
  
    s_call_operator(op_t op, iterators_vector_t_ itv, iterators_vector_t_ itve, images_vector_t& ims):
      t(op), its(itv), ites(itve), image_vector(ims)
    {}
  

    result_type operator()() //const
    {
      typedef bf::vector<iterators_vector_t&, iterators_vector_t&> v_iterators_t;
      
      v_iterators_t v_iterators(its, ites);
      
      bf::zip_view< v_iterators_t > zipv(v_iterators);
      
      typedef typename bf::result_of::fold<bf::zip_view< v_iterators_t >, bf::vector0<>, s_super_fold>::type fold_res_t;
      fold_res_t res_t = bf::fold(zipv, bf::vector0<>(), s_super_fold());
      
      typedef bf::joint_view<fold_res_t, images_vector_t> u_t;
      u_t uuu(boost::ref(res_t), image_vector);
      
      bf::single_view<op_t> tv(t);
      bf::joint_view<bf::single_view<op_t> const, u_t> bbb(tv, boost::ref(uuu));
      operator_on_iterators_t obj;
      
      return bf::invoke(obj, bbb);
    }
  };
  
  
  
  /*!Helper functor for returning the difference of a pair of iterators
   *
   * Was initially used only for random access iterators, but this condition was relaxed and delegated to @c "std::distance".
   */
  struct s_get_iterator_distance
  {
    template <typename Sig>
    struct result;

    template <class Self, typename T>
    struct result< Self(T,T) >
    {
      typedef 
        typename std::iterator_traits<
          typename boost::remove_const<
            typename boost::remove_reference<T>::type
          >::type
        >::difference_type type;
    };

    
    template<typename T>
    typename result<s_get_iterator_distance(T,T)>::type 
    operator()(T it, T ite) const
    {
      return std::distance(it, ite);
    }    
  };
  
  
  /*!Helper structure for returning a sequence of difference on a range of iterators
   *
   * The iterators are packed as 2 tuples: one tuple contains all begin points, the other all end points
   * in the same order.
   */
  struct s_get_iterator_distance_sequence
  {

    template <typename Sig>
    struct result;

    template <class Self, typename T>
    struct result< Self(T,T) >
    {
      typedef typename boost::add_reference< typename boost::add_const<T>::type >::type constref_T;
      typedef typename bf::result_of::zip<constref_T, constref_T>::type zip_type; // const needed here
      
      typedef typename bf::result_of::transform<
          zip_type const, // const needed here
          typename bf::result_of::make_fused_function_object<s_get_iterator_distance>::type 
        >::type type;
    };

    template <class iterator_sequence>
    typename result<s_get_iterator_distance_sequence(iterator_sequence const&, iterator_sequence const&)>::type
    operator()(iterator_sequence const& it, iterator_sequence const &ite) const
    {
      // list of differences on the iterator ranges
      return bf::transform(
          bf::zip(it, ite), 
          bf::make_fused_function_object(s_get_iterator_distance()));
    }
  };
  
  
  //! Helper functor for that computes the minimum of the distances within a set of pairs of iterators
  //! Used for instance for determining the minimum delta that satisfies an increment of all iterators
  //! without reaching the given bounds.
  struct s_iterator_sequence_min_distance
  {
    
    struct s_min_keeper
    {
      s_get_iterator_distance op;
      
      template <class sig> struct result;
      template <class Self, class T, class res>
      struct result<Self(res, T)>
      {
        typedef typename boost::result_of<
          s_get_iterator_distance(
            typename bf::result_of::at_c<T, 0>::type,
            typename bf::result_of::at_c<T, 1>::type)>::type difference_type;
        
        typedef typename boost::numeric::conversion_traits<
          typename boost::remove_reference<res>::type, difference_type>::supertype type;
      };
      
      
      template<typename T, typename res>
      typename result<s_min_keeper(res, T)>::type
      operator()(res const &d, T const& t) const
      {
        BOOST_MPL_ASSERT_RELATION((bf::result_of::size<T>::type::value), ==, 2);
        return std::min<typename result<s_min_keeper(res, T)>::type>(op(bf::at_c<0>(t), bf::at_c<1>(t)), d);
      }
    };
    
    
    template <class>
    struct result;
    
    template <class Self, class T>
    struct result<Self(T,T)>
    {
      typedef typename bf::result_of::fold<
        bf::zip_view< bf::vector<T const&, T const&> >,
        ptrdiff_t,
        s_min_keeper>::type fold_type;
      
      typedef typename boost::remove_const<typename boost::remove_reference<fold_type>::type>::type type;
    };
    
    template <class itv_t>
    typename result<s_iterator_sequence_min_distance(itv_t,itv_t)>::type
    operator()(itv_t const& itv, itv_t const& itve) const
    {
      return bf::fold(
        bf::zip_view< bf::vector<itv_t const&, itv_t const&> >(bf::vector_tie(itv, itve)),
        std::numeric_limits<ptrdiff_t>::max(),
        s_min_keeper());
    }
  };

  //! Helper functor for incrementing an iterator by a distance known at construction, without exceeding a bound 
  //! given by another iterator.
  template <class D>
  struct s_iterator_increment_with_bounds
  { 
    D d;
    s_iterator_increment_with_bounds(D const& d_) : d(d_){}
        
    template<typename T>
    void operator()(T& it, T const& ite) const
    {
      if(std::distance(it, ite) > d)
      {
        std::advance(it, d);
      }
      else
      {
        it = ite;
      }
    }
  };
  
  
  /*! @brief Increments a vector of iterators with a constant step, without exceeding the bound given by a second vector
   *
   *  This helper function (for multithreaded call) increments the iterators in itv (boost::fusion vector) by delta. The 
   *  iterators should all implement operator+= and operator- (the one considered implement random_access iterator concept).
   *  No iterator can exceed a bound given by iterator at the same index in itve. 
   *  
   *  The signature of the function ensures the given vectors are of the same size. 
   *
   *  @returns the increment applied to all vectors (may be lower than delta, if a bound has been found)
   *  @see s_iterator_increment_with_bounds
   */
  template <class delta_t, class itv_t>
  delta_t bounded_increment(delta_t delta, itv_t &itv, itv_t const& itve) const
  {
    //delta_t delta_new = s_iterator_sequence_min_distance()(itv, itve);
    
    // we should test if all increment are free of bound
    bf::for_each(
      bf::zip_view< bf::vector<itv_t&, itv_t const&> >(bf::vector_tie(itv, itve)), 
      bf::make_fused_procedure(s_iterator_increment_with_bounds<delta_t>(delta))
    );
    
    return delta;
  }
  
  
  template <class op_t, bool B = false>
  struct s_create_new
  {
    op_t * operator()(op_t &t) const {return &t;}
  };
  template <class op_t>
  struct s_create_new<op_t, true>
  {
    op_t * operator()(op_t const&t) const {return new op_t(t);}
  };
  
  //! Utility destroying the created applicators
  //! @todo: delete this structure
  template <class sequence_t, bool bown = true>
  struct s_operator_sequence_holder
  {
    sequence_t& s;
    s_operator_sequence_holder(sequence_t &s_): s(s_){}
    ~s_operator_sequence_holder()
    {
      if(bown)
      {
        for(typename sequence_t::iterator it(s.begin()), ite(s.end()); it != ite; ++it)
          delete *it;
      }
    }
  };  
  
  //! This class does nothing, but implements the compositor interface
  template <class op_t>
  struct s_dummy_compositor
  {
    template <class distance_t>
    op_t & generate(op_t &op, distance_t /*d*/) const
    {
      return op;
    }
  
    bool compose(op_t &, op_t const& ) const
    {
      return true;
    }  
  };


  /*! @brief Multithreaded execution of the applicator, provided the exitence of composition the image/pixel operator
   *
   *  @author Raffi Enficiaud
   */
  template <class op_apply_t, class op_t, class ittuples_t, class imagestuples>
  #if 0
  typename enable_if<
    typename s_operator_enabling_no_member_tuples_t<op_t, ittuples_t>::type,
    yaRC>::type
  #endif
  yaRC
  apply_stage2(op_t& op, ittuples_t it, ittuples_t ite, imagestuples im) const
  {
    unsigned int const nb_threads = NbProcessorUnit() ?
      std::min(NbProcessorUnit(), boost::thread::hardware_concurrency()) : 
      boost::thread::hardware_concurrency();

    // the distance in each pair of iterators in it/ite.
    typedef typename boost::result_of<
      s_iterator_sequence_min_distance(ittuples_t, ittuples_t)
      >::type delta_t;
    delta_t min_delta = s_iterator_sequence_min_distance()(it, ite);
    
    // do we need a compositor ?
    typedef typename boost::mpl::if_<
      typename s_operator_enabling_no_member_tuples_t<op_t, ittuples_t>::type,
      boost::mpl::false_,
      typename boost::mpl::if_<
        typename s_operator_enabling_composition_tuples_t<op_t, ittuples_t>::type,
        boost::mpl::true_,
        boost::mpl::false_>::type // for tests
      >::type need_compositor_t;
    
    // this object returns the existing operator or creates a new instance (related to the
    // composition strategy)
    s_create_new<op_t, need_compositor_t::value> op_creator;
    
    typedef typename boost::mpl::if_<
      need_compositor_t,
      s_operator_composition<op_t>,
      s_dummy_compositor<op_t>
      >::type compositer_t;
      
    compositer_t compositor;
    
    typedef s_call_operator<
      op_apply_t,
      op_t &,
      ittuples_t, 
      imagestuples      
      > call_operator_t;
    
    // the increment in the data range to apply to each thread / unit of execution
    delta_t delta = min_delta / nb_threads;

    typedef boost::unique_future<yaRC> future_t;
    boost::scoped_array<future_t> futures(new future_t[nb_threads]);
    
    // holder over all the instances of the pixel operators
    typedef std::vector<op_t*> operator_sequence_t;
    operator_sequence_t op_sequence;
    
    // cleanup if necessary (see need_compositor_t)
    s_operator_sequence_holder<operator_sequence_t, need_compositor_t::value> op_sequence_holder(op_sequence);
    
    ittuples_t it_current_unit_end;
    bf::copy(it, it_current_unit_end);
    delta = bounded_increment(delta, it_current_unit_end, ite);
    
  
    boost::thread_group g;    
    
    // create intermediate function objects
    for(unsigned int i = 0; i < nb_threads; i++)
    {
      // creates a new instance if needed
      op_t *new_op = op_creator(compositor.generate(op, delta));
      assert(new_op != 0); // this object cannot be null
      
      // push this new/current instance into the sequence of operators
      op_sequence.push_back(new_op);
      
      // creates a new packaged task returning yaRC
      boost::packaged_task<yaRC> pt(call_operator_t(*new_op, it, it_current_unit_end, im));
    
      // get the future of this task
      futures[i] = pt.get_future();
      
      // move the task into a thread
      boost::thread *task = new boost::thread(boost::move(pt));
      
      // move this task into the group of threads
      g.add_thread(task);

      // copy the previous sequence of iterators into the current
      bf::copy(it_current_unit_end, it);
      
      // increments the sequence of iterators
      delta = bounded_increment(delta, it_current_unit_end, ite);
    }    
    
    // wait for all threads to complete
    g.join_all();
    
    
    // test if everything was ok
    for(unsigned int i = 0; i < nb_threads; i++)
    {
      if(futures[i].has_exception())
      {
        DEBUG_INFO("Exception detected in execution thread #" << i);
        return yaRC_E_unknown;
      }
      assert(futures[i].is_ready());
      assert(futures[i].has_value());
      if(futures[i].get() != yaRC_ok)
      {
        DEBUG_INFO("Error detected in execution thread #" << i << ": error = " << futures[i].get());
        return futures[i].get();
      }
    }


    // composition
    for(unsigned int i = 0; i < nb_threads; i++)
    {
      if(!compositor.compose(op, *op_sequence[i]))
      {
        DEBUG_INFO("Error detected in composition of the result of thread #" << i );
        return yaRC_E_unknown;
      }
    }
    
    
    #if 0
    // consider using a thread pool
    // Create an io_service:
    asio::io_service io_service;

    // and some work to stop its run() function from exiting if it has nothing else to do:

    asio::io_service::work work(io_service);

    // Start some worker threads:

    boost::thread_group threads;
    for (std::size_t i = 0; i < my_thread_count; ++i)
    {
      threads.create_thread(boost::bind(&asio::io_service::run, &io_service));
    }

    // Post the tasks to the io_service so they can be performed by the worker threads:
    io_service.post(boost::bind(an_expensive_calculation, 42));
    io_service.post(boost::bind(a_long_running_task, 123));

    // Finally, before the program exits shut down the io_service and wait for all threads to exit:

    io_service.stop();
    threads.join_all();


    #endif
    


    return yaRC_ok;
  }




  //! Linear execution of the applicator
  template <class op_apply_t, class op_t, class it_t, class image_in_out>
  typename boost::disable_if<
    typename boost::mpl::or_< 
      s_operator_enabling_no_member_t<op_t, it_t>,
      s_operator_enabling_composition_t<op_t, it_t> 
    >::type, 
    yaRC>::type
  apply_stage(op_t& op, it_t it, it_t ite, image_in_out& im) const
  {
    op_apply_t op_apply;
    return op_apply(op, it, ite, im);
  }

  //! Dispatch from the provided iterator extractor into the operator applicator
  template <class iterator_extractor_t, class image_in_out, class op_>
  yaRC apply(image_in_out& im, op_& op) const
  {
    //BOOST_STATIC_ASSERT(is_void<typename op_::result_type>::value);
    typedef s_iterator_extractor<iterator_extractor_t> extractor_type;
    
    extractor_type extractor;
    
    typedef typename extractor_type::template result<extractor_type(image_in_out&)>::type result_type;
    
    const result_type iterators(extractor(im));
    typename result_type::first_type        it  = iterators.first;
    typename result_type::second_type const ite = iterators.second;
    
    // test the return of op if it exists ??
    typedef typename s_extract_operator_type::template result< op_(typename result_type::first_type::reference) >::type range_type_with_potential_return;
    typedef typename s_remove_return<range_type_with_potential_return>::type range_type;
    
    
    // Here we can add more precision on the type of 
    typedef s_apply_op_range<iterators_same_pointer_and_same_images_tag, range_type> op_apply_t;
    
    return apply_stage2<op_apply_t>(op, bf::make_vector(it), bf::make_vector(ite), bf::make_vector(boost::ref(im)));
  }
  
public:
  template <class image_in_out, class op_>
  yaRC operator()(image_in_out& im, op_& op) const
  {
    return apply<iterator_choice_strategy_non_windowed_tag>(im, op);
  }
};




struct image_apply_threaded_test_fixture
{
  typedef Image<yaUINT16> image_type;
  image_type im, im1, im2;
  
  image_apply_threaded_test_fixture()
  {
    //BOOST_TEST_MESSAGE("Fixture");
    CreateImages();
    PrepareImages();
  }

  void CreateImages()
  {
    image_type::coordinate_type size(c2D(50,50));

    BOOST_REQUIRE(im1.SetSize(size) == yaRC_ok);
    BOOST_REQUIRE(im1.AllocateImage() == yaRC_ok);
    BOOST_REQUIRE(im2.SetSize(size) == yaRC_ok);
    BOOST_REQUIRE(im2.AllocateImage() == yaRC_ok);
    BOOST_REQUIRE(im.SetSize(size) == yaRC_ok);
    BOOST_REQUIRE(im.AllocateImage() == yaRC_ok);
  }
  
  void PrepareImages()
  {
    size_t i = 0;
    for(image_type::iterator it(im1.begin_block()), ite(im1.end_block()), it2(im2.begin_block()); it != ite; ++it, ++it2, ++i)
    {
      *it2 = *it = i % 17;
    }
  }
};


BOOST_AUTO_TEST_SUITE(apply_multithread)

BOOST_AUTO_TEST_CASE(check_operator_composition_availability)
{
  typedef image_apply_threaded_test_fixture::image_type image_type;
  // checks the response of s_operator_enabling_composition
  BOOST_CHECK_MESSAGE((s_apply_unary_operator_threaded::s_operator_enabling_composition_t<s_multiply_by_two_multithreaded, image_type::const_iterator>::type::value),
    "failure while checking composition possibility of \"s_two_times_mt\" against \"image_type::const_iterator\"");
  BOOST_CHECK_MESSAGE(!(s_apply_unary_operator_threaded::s_operator_enabling_composition_t<s_multiply_by_two_multithreaded, std::list<int>::const_iterator>::type::value),
    "failure while checking composition possibility of \"s_two_times_mt\" against \"std::list<int>::const_iterator\"");
  BOOST_CHECK_MESSAGE(!(s_apply_unary_operator_threaded::s_operator_enabling_composition_t<s_three_times_mt, image_type::const_iterator>::type::value),
    "failure while checking composition possibility of \"s_three_times_mt\" against \"image_type::const_iterator\"");
  BOOST_CHECK_MESSAGE(!(s_apply_unary_operator_threaded::s_operator_enabling_composition_t<s_three_times_mt, std::list<int>::const_iterator>::type::value),
    "failure while checking composition possibility of \"s_three_times_mt\" against \"std::list<int>::const_iterator\"");
}


BOOST_AUTO_TEST_CASE(check_difference_on_iterators_computation)
{
  std::vector<int> v100(100);
  std::list<float> l10(v100.begin(), v100.begin() + 10);
  
  s_apply_unary_operator_threaded::s_get_iterator_distance_sequence diff_op;

  // checks that the distance between the iterators of the first container is 100
  BOOST_CHECK(bf::at_c<0>(diff_op(
    bf::make_vector(v100.begin(), l10.begin()),
    bf::make_vector(v100.end(), l10.end()))) == 100);
  
  // same for the second iterator
  // this doe snot compile if s_get_iterator_distance works only on random access iterators, which shows that
  // all these probes are lazily evaluated.
  BOOST_CHECK(bf::at_c<1>(diff_op(
    bf::make_vector(v100.begin(), l10.begin()),
    bf::make_vector(v100.end(), l10.end()))) == 10);
  
  // computes now the min distance
  typedef s_apply_unary_operator_threaded::s_iterator_sequence_min_distance op_mindist_t;
  op_mindist_t op_min_dist;

  // warning to this type, if at_c is not available, op_mindist_t::s_min_keeper::result fails to compile and
  // we get an "SFINAE", which then makes the specialization of result unavailable.
  typedef bf::vector<
            std::vector<int>::const_iterator,
            std::vector<int>::const_iterator > vect_t;
  
  typedef boost::result_of<op_mindist_t::s_min_keeper( ptrdiff_t const&, vect_t) >::type result_of_s_min_keeper_t;
  typedef boost::result_of<op_mindist_t::s_min_keeper( ptrdiff_t, vect_t) >::type result_of_s_min_keeper2_t;
  
  // this should be the call made by boost::fusion, we should prevent the return reference to a temporary problem.
  BOOST_STATIC_ASSERT_MSG(!(boost::is_reference<result_of_s_min_keeper_t>::value),
    "the returned value is a reference while it should be a plain value");
      
  BOOST_STATIC_ASSERT_MSG(!(boost::is_reference<result_of_s_min_keeper2_t>::value),
    "the returned value is a reference while it should be a plain value");
  
  BOOST_CHECK(op_min_dist(
    bf::make_vector(v100.begin(), l10.begin()),
    bf::make_vector(v100.end(), l10.end())) == 10);
  
}


BOOST_FIXTURE_TEST_CASE(image_application1, image_apply_threaded_test_fixture)
{
  // Unary operator in-place
  
  s_apply_unary_operator_threaded op_im;
  s_multiply_by_two_multithreaded op;
  op.count = 0;
  
  BOOST_CHECK(op_im(im1, op) == yaRC_ok);
  BOOST_CHECK_MESSAGE(op.count == total_number_of_points(im1.Size()), "Number of counted operations " << op.count << " !=  " << total_number_of_points(im1.Size()));
  
  for(image_type::const_iterator it = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it != ite; ++it, ++it2) {
    BOOST_CHECK_MESSAGE(*it == 2 * (*it2), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
  }
  
  
  // fonction Process à tester également
}


BOOST_FIXTURE_TEST_CASE(image_application2, image_apply_threaded_test_fixture)
{
  // Unary operator in-place

  s_apply_unary_operator_threaded op_im;
  s_three_times_mt op;
  
  
  BOOST_CHECK(op_im(im1, op) == yaRC_ok);
  
  
  for(image_type::const_iterator it = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it != ite; ++it, ++it2) {
    BOOST_CHECK_MESSAGE(*it == 3 * (*it2), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 3 * (*it2));
  }
  
  
  // fonction Process à tester également
}  

BOOST_AUTO_TEST_SUITE_END()




class image_apply_threaded_test 
{
public:
  
  

  #if 0
  void test_image_application1_inplace() {
    // Unary operator in-place
    BOOST_CHECKPOINT("test_image_application1_inplace");
    
    PrepareImages();
    
    s_apply_unary_operator op_im;
    s_two_times_mt op;
    op.count = 0;
    
    BOOST_CHECK(op_im(im1, op) == yaRC_ok);
    BOOST_CHECK_MESSAGE(op.count == total_number_of_points(im1.Size()), "Number of counted operations " << op.count << " !=  " << total_number_of_points(im1.Size()));
    
    for(image_type::const_iterator it = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it != ite; ++it, ++it2) {
      BOOST_CHECK_MESSAGE(*it == 2 * (*it2), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
    }
    
    
    // fonction Process à tester également
  }


  void test_image_application1_notinplace() {
    // Unary operator in-place
    BOOST_CHECKPOINT("test_image_application1_notinplace");
    
    PrepareImages();
    
    s_two_times_mt op;
    
    // Adapting the appropriate overloaded method of the object
    boost::function<image_type::pixel_type (const image_type::pixel_type&)> f;
    f = boost::bind(&s_two_times_mt::operator()<image_type::pixel_type, image_type::pixel_type>, &op, _1);
    
    s_apply_unary_operator op_im;

    op.count = 0;
    
    BOOST_CHECK(op_im(im1, im, f) == yaRC_ok);
    BOOST_CHECK_MESSAGE(op.count == total_number_of_points(im1.Size()), "Number of counted operations " << op.count << " !=  " << total_number_of_points(im1.Size()));
    
    for(image_type::const_iterator it = im1.begin_block(), it2 = im.begin_block(), it3 = im2.begin_block(), ite = im1.end_block(); 
        it != ite; ++it, ++it2, ++it3) {
      BOOST_CHECK_MESSAGE(*it2 == 2 * (*it), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
      BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));
    }
    
    
    // fonction Process à tester également
  }


  void test_image_application2() {
    BOOST_CHECKPOINT("test_image_application2");	

    PrepareImages();

    s_apply_binary_operator op_im;
    s_square_mt op;
    op.count = 0;
    
    BOOST_CHECK(op_im(im1, im1, im2, op) == yaRC_ok);
    BOOST_CHECK_MESSAGE(op.count == total_number_of_points(im1.Size()), "Number of counted operations " << op.count << " !=  " << total_number_of_points(im1.Size()));
    
    for(image_type::const_iterator it1 = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it1 != ite; ++it1, ++it2) {
      BOOST_CHECK_MESSAGE(*it2 == static_cast<image_type::pixel_type>(2 * (*it1) * (*it1)) /*% ((1<<16) -1)*/, "failure with *it2 = " << (int)(*it2) << " and 2 * (*it1) *  (*it1) = " << static_cast<image_type::pixel_type>(2 * (*it1) * (*it1)) /*% ((1<<16) -1)*/);
    }

    PrepareImages();
    op.count = 0;
    BOOST_CHECK(op_im(im1, im1, im1, op) == yaRC_ok);
    BOOST_CHECK_MESSAGE(op.count == total_number_of_points(im1.Size()), "Number of counted operations " << op.count << " !=  " << total_number_of_points(im1.Size()));
    
    for(image_type::const_iterator it1 = im1.begin_block(), it2 = im2.begin_block(), ite = im1.end_block(); it1 != ite; ++it1, ++it2) {
      BOOST_CHECK_MESSAGE(*it1 == static_cast<image_type::pixel_type>(2 * (*it2) * (*it2)) /*% ((1<<16) -1)*/, "failure with *it1 = " << (int)(*it1) << " and 2 * (*it2) *  (*it2) = " << static_cast<image_type::pixel_type>(2 * (*it2) * (*it2)) /*% ((1<<16) -1)*/);
    }

   
  }
  

  
  
  void test_image_windowed_unary_application() {
    BOOST_CHECKPOINT("test_image_windowed_unary_application");	
    
    PrepareImages();
    
    s_two_times_mt op;
    
    // Adapting the appropriate overloaded method of the object
    boost::function<image_type::pixel_type (const image_type::pixel_type&)> f;
    f = boost::bind(&s_two_times_mt::operator()<image_type::pixel_type, image_type::pixel_type>, &op, _1);
    
    s_apply_unary_operator op_im;

    op.count = 0;
    
    s_hyper_rectangle<2> window(c2D(1,1), c2D(2,2));
    
    for(int i = 0; i < total_number_of_points(im.Size()); i++)
      im.pixel(i) = i;
    
    BOOST_CHECK(op_im(im1, window, im, window, f) == yaRC_ok);
    BOOST_CHECK_MESSAGE(total_number_of_points(window.Size()) == 4, "Number of point mistake " << total_number_of_points(window.Size()) << " !=  " << 4);
    BOOST_CHECK_MESSAGE(op.count == 4, "Number of counted operations " << op.count << " !=  " << 4);
    
    for(image_type::const_iterator it = im1.begin_block(), it2 = im.begin_block(), it3 = im2.begin_block(), ite = im1.end_block(); 
        it != ite; ++it, ++it2, ++it3) 
    {
      if(is_point_inside(window, it.Position()))
      {
        BOOST_CHECK_MESSAGE(*it2 == 2 * (*it), "failure with *it = " << (int)(*it) << " and 2 * (*it2) = " << 2 * (*it2));
        BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));
      }
      else
      {
        BOOST_CHECK_MESSAGE(*it2 == (it.Offset() % (std::numeric_limits<yaUINT16>::max()+1)), "failure with it.Offset() = " << (int)(it.Offset()) << " and *it2 = " << *it2 << " - operation made outside the window");
        BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));      
      }
    }
    
    
    PrepareImages();
    op.count = 0;
    s_hyper_rectangle<2> window2(c2D(3,3), c2D(3,3));
    for(int i = 0; i < total_number_of_points(im.Size()); i++)
      im.pixel(i) = i;

    BOOST_CHECK(op_im(im1, window, im, window2, f) == yaRC_ok);
    BOOST_CHECK_MESSAGE(op.count == 4, "Number of counted operations " << op.count << " !=  " << 4);

    for(image_type::const_iterator it = im1.begin_block(), it2 = im.begin_block(), it3 = im2.begin_block(), ite = im1.end_block(); 
        it != ite; ++it, ++it2, ++it3) 
    {
      if(is_point_inside(window2, it2.Position()))
      {
        //BOOST_CHECK(is_point_inside(window2, it2.Position()));
        BOOST_CHECK_MESSAGE(*it2 == 2 * im1.pixel(it2.Position() - window2.Origin() + window.Origin()), 
          "failure with *it = " << (int)(*it) 
          << " and 2 * im1.pixel(it2.Position() - c2D(3,3) + c2D(1,1)) = " << 2 * im1.pixel(it2.Position() - window2.Origin() + window.Origin())
          << " for position " << it2.Position()
          );
        BOOST_CHECK_MESSAGE(*it == (*it3), "failure of const original with *it = " << (int)(*it) << " and (*it3 (original)) = " << (int)(*it3));
      }
      else
      {
        BOOST_CHECK_MESSAGE(*it2 == it.Offset() % (std::numeric_limits<yaUINT16>::max()+1), 
          "failure with it.Offset() = " << (int)(it.Offset()) 
          << " and *it2 = " << *it2 
          << " at position " << it.Position()
          << " - operation made outside the window");
        BOOST_CHECK_MESSAGE(*it == *it3, "failure of const original with *it (result) = " << (int)(*it) << " and *it3 (original) = " << (int)(*it3));      
      }
    }
    
    std::cout << "im1" << std::endl;
    print_im(std::cout, im1);
    std::cout << "im" << std::endl;
    print_im(std::cout, im);
    
  }



  #endif

};


