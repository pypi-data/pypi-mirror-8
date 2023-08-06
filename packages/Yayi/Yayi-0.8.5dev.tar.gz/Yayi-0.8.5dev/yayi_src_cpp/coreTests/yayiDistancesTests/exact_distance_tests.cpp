#include "main.hpp"
#include <boost/test/parameterized_test.hpp>
#include <boost/test/test_case_template.hpp>

#include <yayiDistances/include/exact_distances_t.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <yayiCommon/include/common_time.hpp>

#include <boost/random/uniform_real.hpp>
#include <boost/random/uniform_int.hpp>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/variate_generator.hpp>

#include <boost/numeric/conversion/bounds.hpp>
#include <boost/mpl/list.hpp>
#include <boost/mpl/pair.hpp>

#include <yayiCommon/include/common_coordinates_mpl_utils_t.hpp>
#include <fstream>
#include <yayiCommon/common_constants.hpp>


#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>


#ifdef YAYI_REAL_RANDOM_EXISTS__
typedef boost::random_device random_generator_type;
#else
typedef boost::mt19937 random_generator_type;
#endif


BOOST_AUTO_TEST_CASE(distance_functions)
{
  using namespace yayi;
  using namespace yayi::distances;
  
  typedef s_coordinate<2> coordinate_type;
  typedef s_coordinate<2, double> source_coordinate_type;
  s_euclidian_distance_op<source_coordinate_type, coordinate_type> op_dist;
  
  double tabled[] = {46.6997, 40.8816};
  int tablei[] = {49, 41};
  
  coordinate_type coord1(coordinate_type::from_table(tablei));
  source_coordinate_type coord2(source_coordinate_type::from_table(tabled));
  
  BOOST_CHECK_CLOSE(op_dist(coord2, coord1), 
                    ::sqrt((tablei[0] - tabled[0])*(tablei[0] - tabled[0]) + (tablei[1] - tabled[1])*(tablei[1] - tabled[1])), 
                    1E-10 );

  BOOST_CHECK(!(distance_has_storage_tag<distances::s_lp_distance_op<source_coordinate_type, coordinate_type, 9, 5> >::value));
  BOOST_MPL_ASSERT_NOT((distance_has_storage_tag<distances::s_lp_distance_op<source_coordinate_type, coordinate_type, 9, 5> >));

  BOOST_CHECK((distance_has_storage_tag< s_euclidian_distance_op<source_coordinate_type, coordinate_type> >::value));
  BOOST_MPL_ASSERT((distance_has_storage_tag< s_euclidian_distance_op<source_coordinate_type, coordinate_type> >));
  
  
  s_l5_distance_op<source_coordinate_type, coordinate_type> op_dist5;
  BOOST_CHECK_CLOSE(op_dist5(coord2, coord1), 
                    std::pow(std::pow(std::abs(tablei[0] - tabled[0]), 5.) + std::pow(std::abs(tablei[1] - tabled[1]), 5.), 1./5), 
                    1E-10 );
}


namespace 
{
  using namespace boost::numeric::ublas;

  template <int dim>
  matrix<double> get_rotation_matrix(const int dim1, const int dim2, const double angle)
  {
    matrix<double> m (dim, dim);
    for (unsigned i = 0; i < m.size1 (); ++ i)
    {
      for (unsigned j = 0; j < m.size2 (); ++ j)
      {
        if(i == j)
        {
          m(i, j) = 1;
        }
        else
        {
          m (i, j) = 0;
        }
      }
    }
    
    m(dim1, dim1) = m(dim2, dim2) = std::cos(angle);
    m(dim1, dim2) = std::sin(angle);
    m(dim2, dim1) = -std::sin(angle);

    return m;
  }


  template <int dim>
  matrix<double> get_diagonal_matrix(const double* diagonal_value)
  {
    matrix<double> m (dim, dim);
    for (unsigned i = 0; i < m.size1 (); ++ i)
    {
      for (unsigned j = 0; j < m.size2 (); ++ j)
      {
        if(i == j)
        {
          m(i, j) = *(diagonal_value++);
        }
        else
        {
          m (i, j) = 0;
        }
      }
    }
    return m;
  }

  std::vector<double> matrix_to_vector(const matrix<double>&m)
  {
    std::vector<double> out;
    for (unsigned i = 0; i < m.size1 (); ++ i)
    {
      for (unsigned j = 0; j < m.size2 (); ++ j)
      {
        out.push_back(m(i,j));
      }
    }

    return out;
  }


  // this function generates a distance function
  template <class seed_coordinate_t>
  yayi::distances::s_generic_euclidian_norm_op<
    seed_coordinate_t,
    yayi::s_coordinate<seed_coordinate_t::static_dimensions> 
    > 
    get_random_distance()
  {
    using namespace yayi;
    const int dim = seed_coordinate_t::static_dimensions;
    
    typedef yayi::distances::s_generic_euclidian_norm_op<seed_coordinate_t, s_coordinate<dim> > out_type;
    
    typedef boost::uniform_real<yaF_double> distribution_type;
    typedef random_generator_type generator_type;
    typedef boost::variate_generator<generator_type, distribution_type> distribution_generator_t;

    static generator_type rng;
    static distribution_generator_t generator(rng, distribution_type(0, 1.));
    
    std::vector< double > v_diag;
    for(int i = 0; i < dim; i++)
    {
      v_diag.push_back(generator() + 1.);
    }  
    
    // this is the scaling
    matrix<double> md = get_diagonal_matrix<dim>(&(*v_diag.begin()));
    
    // this is the rotation
    matrix<double> mu = get_rotation_matrix<dim>(0, 1, generator() * 2*yaPI);
    for(unsigned int i = 1; i < dim-1; i++)
    {
      matrix<double> r = get_rotation_matrix<dim>(i, i+1, generator() * 2*yaPI);
      mu = prod(matrix<double>(mu), r);
    }
    
    matrix<double> m = prod(matrix<double>(trans(mu)), md) ; 
    m = prod(matrix<double>(m), mu);
    
    return out_type(matrix_to_vector(m));
  }

}



template <class coordinate_t_>
struct param_distance_test
{
  typedef coordinate_t_ coordinate_t;
  coordinate_t image_size;
  int nb_seeds;
};

//
template <class distance_op_t, class param_t>
void test_distance_exact(const param_t &param, const distance_op_t& dist_op = distance_op_t() ) 
{
  using namespace yayi;
  typedef Image<yaF_double, typename param_t::coordinate_t> image_type;
  
  image_type im_out_dist;
  image_type* p_im[] = {&im_out_dist};
  typename image_type::coordinate_type coord(param.image_size);
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE_EQUAL(p_im[i]->SetSize(coord), yaRC_ok);
    BOOST_REQUIRE_EQUAL(p_im[i]->AllocateImage(), yaRC_ok);
  }
  
  typedef boost::uniform_real<yaF_simple> distribution_type;
  typedef random_generator_type generator_type;
  typedef boost::variate_generator<generator_type, distribution_type> distribution_generator_t;

  generator_type rng;
  distribution_generator_t generator(rng, distribution_type(0, 1.));

  // generate n random points for the distance seeds
  typedef s_coordinate<image_type::coordinate_type::static_dimensions, yaF_double> source_coordinate_t;
  std::vector< source_coordinate_t > v_sources;
  for(int i = 0; i < param.nb_seeds; i++)
  {
    source_coordinate_t current;
    for(int j = 0; j < image_type::coordinate_type::static_dimensions; j++)
    {
      current[j] = generator() * coord[j];
    }
    v_sources.push_back(current);
  }

  yayi::time::s_time_elapsed time_distance;
  
  //distances::s_euclidian_distance_op<source_coordinate_t, image_type::coordinate_type> dist_op;
  //distance_op_t dist_op;
  
  BOOST_REQUIRE_EQUAL(distances::exact_distance_t(v_sources, dist_op, im_out_dist), yaRC_ok);
  BOOST_MESSAGE("Computation of the exact distance on an image of " 
                << im_out_dist.Size()
                << " with N=" << param.nb_seeds << " seeds"
                << " took " << time_distance.total_milliseconds() << "ms");

  // exhaustive outputs checks
  yayi::time::s_time_elapsed time_check;
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    yaF_double current_distance = im_out_dist.pixel(i), min_dist = boost::numeric::bounds<yaF_double>::highest();
    typename image_type::coordinate_type const pos_current = from_offset_to_coordinate(coord, i);
    source_coordinate_t pos_min_source;
    for(int j = 0; j < param.nb_seeds; j++)
    {
      yaF_double current_dist = dist_op(v_sources[j], pos_current);
      if(min_dist > current_dist)
      {
        min_dist = current_dist;
        pos_min_source = v_sources[j];
      }
    }
    if(std::abs(current_distance - min_dist) / std::max(current_distance, min_dist) > 1E-4)
    {
      std::cout << "problem with the point " << pos_current << "\n";
      std::cout << "The source is " << pos_min_source << " with distance " << min_dist << "\n";
      std::cout << "Found distance is " << current_distance << "\n";
    }
    BOOST_CHECK_CLOSE(current_distance, min_dist, 1E-4);
  }
}


BOOST_AUTO_TEST_CASE(test_distance_euclidian_2D_100x100_50seeds)
{
  using namespace yayi;
  typedef s_coordinate<2> coordinate_t;
  param_distance_test< coordinate_t > p;
  p.image_size = c2D(100, 100);
  p.nb_seeds = 50;
  test_distance_exact<
    distances::s_euclidian_distance_op<
      s_coordinate<coordinate_t::static_dimensions, yaF_double>,  // these are the coordinate type of the random generation (the seeds)
      coordinate_t>
    >(p);
}

BOOST_AUTO_TEST_CASE(test_distance_euclidian_3D_50x50x50_50seeds)
{
  using namespace yayi;
  typedef s_coordinate<3> coordinate_t;
  param_distance_test< coordinate_t > p;
  p.image_size = c3D(50, 50, 50);
  p.nb_seeds = 50;
  test_distance_exact<
    distances::s_euclidian_distance_op<
      s_coordinate<coordinate_t::static_dimensions, yaF_double>,  // these are the coordinate type of the random generation (the seeds)
      coordinate_t>
    >(p);
}


BOOST_AUTO_TEST_CASE(test_distance_euclidian_generic_distance_3D_50x50x50_10seeds)
{
  using namespace yayi;
  typedef s_coordinate<3> coordinate_t;
  param_distance_test< coordinate_t > p;
  p.image_size = c3D(50, 50, 50);
  p.nb_seeds = 10;
  
  typedef s_coordinate<coordinate_t::static_dimensions, yaF_double> seed_coordinate_t;
  
  // the "generic" distance type
  typedef distances::s_generic_euclidian_norm_op<
    seed_coordinate_t, 
    coordinate_t > distance_type;
  
  // an instance of the distance
  distance_type dist(get_random_distance<seed_coordinate_t>());
  test_distance_exact(p, dist);
}


BOOST_AUTO_TEST_CASE(test_distance_euclidian_generic_distance_4D_50x50x10x10_10seeds)
{
  using namespace yayi;
  typedef s_coordinate<4> coordinate_t;
  param_distance_test< coordinate_t > p;
  p.image_size = c4D(50, 50, 10, 10);
  p.nb_seeds = 10;
  
  typedef s_coordinate<coordinate_t::static_dimensions, yaF_double> seed_coordinate_t;
  
  // the "generic" distance type
  typedef distances::s_generic_euclidian_norm_op<
    seed_coordinate_t, 
    coordinate_t > distance_type;
  
  // an instance of the distance
  distance_type dist(get_random_distance<seed_coordinate_t>());
  test_distance_exact(p, dist);
}




