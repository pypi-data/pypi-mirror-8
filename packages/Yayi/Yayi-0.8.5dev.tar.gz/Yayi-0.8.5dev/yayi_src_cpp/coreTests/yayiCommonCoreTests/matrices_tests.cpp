#include "main.hpp"
#include <yayiCommon/include/common_matrix_t.hpp>
#include <yayiCommon/include/common_matrix_inversion_t.hpp>


BOOST_AUTO_TEST_SUITE(matrix)

BOOST_AUTO_TEST_CASE(fixed_size_simple_operations)
{
  typedef yayi::s_fixed_size_matrix<int, 2, 2> matrix_t;
  matrix_t m;
  m(0,0) = 1;
  m(0,1) = 2;
  m(1,0) = 3;
  m(1,1) = 4;

  BOOST_CHECK_EQUAL(get_nbrows(m), 2);
  BOOST_CHECK_EQUAL(get_nbcolumns(m), 2);


  matrix_t mm = m + m;
  BOOST_CHECK_EQUAL(mm(0,0), 2*m(0,0));
  BOOST_CHECK_EQUAL(mm(0,1), 2*m(0,1));
  BOOST_CHECK_EQUAL(mm(1,0), 2*m(1,0));
  BOOST_CHECK_EQUAL(mm(1,1), 2*m(1,1));

}

BOOST_AUTO_TEST_CASE(fixed_size_transpose)
{
  typedef yayi::s_fixed_size_matrix<int, 2, 2> matrix_t;
  matrix_t m;
  m(0,0) = 1;
  m(0,1) = 2;
  m(1,0) = 3;
  m(1,1) = 4;

  matrix_t::transposed_type mt = m.transpose();
  BOOST_CHECK_EQUAL(mt(0,0), m(0,0));
  BOOST_CHECK_EQUAL(mt(0,1), m(1,0));
  BOOST_CHECK_EQUAL(mt(1,0), m(0,1));
  BOOST_CHECK_EQUAL(mt(1,1), m(1,1));

}

BOOST_AUTO_TEST_CASE(fixed_size_unarysubmatrix)
{
  typedef yayi::s_fixed_size_matrix<int, 3, 3> matrix_t;
  matrix_t m;

  BOOST_CHECK_EQUAL(get_nbrows(m), 3);
  BOOST_CHECK_EQUAL(get_nbcolumns(m), 3);


  for(int i = 0; i < 3; i++)
    for(int j = 0; j < 3; j++)
      m(i,j) = i + j;

  matrix_t::unitary_submatrix_type mc = m.unitary_submatrix(0, 0);
  BOOST_CHECK_EQUAL(get_nbrows(mc), 2);
  BOOST_CHECK_EQUAL(get_nbcolumns(mc), 2);

  for(int i = 0; i < 2; i++)
    for(int j = 0; j < 2; j++)
      BOOST_CHECK_EQUAL(mc(i,j), m(i+1, j+1));


  mc = m.unitary_submatrix(1, 0);

  BOOST_CHECK_EQUAL(get_nbrows(mc), 2);
  BOOST_CHECK_EQUAL(get_nbcolumns(mc), 2);

  for(int i = 0; i < 2; i++)
    for(int j = 0; j < 2; j++)
      BOOST_CHECK_EQUAL(mc(i,j), m(i < 1 ? 0:2, j+1));
}
BOOST_AUTO_TEST_CASE(fixed_size_determinant)
{
  typedef yayi::s_fixed_size_matrix<int, 3, 3> matrix_t;
  matrix_t m;

  for(int i = 0; i < 3; i++)
    for(int j = 0; j < 3; j++)
      m(i,j) = 3*i + j + 1;

  matrix_t::value_type det;
  BOOST_CHECK(determinant(m, det));
  BOOST_CHECK_EQUAL(det, 0);
}


BOOST_AUTO_TEST_CASE(qr_householder_decomposition)
{
  using namespace yayi;
  // testing the householder matrix decomposition.
  typedef boost::numeric::ublas::matrix<double> matrix_type;
  matrix_type m(3, 3);

  int values_test[] = {12, -51, 4, 6, 167, -68, -4, 24, -41};
  for(int i = 0; i < 9; i++)
  {
    m(i/3, i%3) = values_test[i];
  }

  matrix_type msave(m);
  matrix_type q;
  BOOST_CHECK(yayi::qr_householder_decomposition(m, q));

  std::cout << "A (or R)" << std::endl << m << std::endl;
  std::cout << "Q" << std::endl << q << std::endl;
  std::cout << "reconstructed matrix " << boost::numeric::ublas::prod(q, m) << std::endl;
  std::cout << "original matrix " << msave << std::endl;
  BOOST_CHECK_LE(boost::numeric::ublas::norm_frobenius(msave - boost::numeric::ublas::prod(q, m)), 1E-6);

  // checking q is orthogonal
  BOOST_CHECK_LE(
    max_norm(boost::numeric::ublas::prod(boost::numeric::ublas::trans(q), q)-
    boost::numeric::ublas::identity_matrix<double>(q.size1())), 1E-5);
  
  // checking r is upper triangular
  for(int i = 0; i < get_nbcolumns(m); i++)
  {
    for(int j = i+1; j < get_nbrows(m); j++)
    {
      BOOST_CHECK_LE(std::abs(m(j, i)), 1E-3);
    }  
  }

}

BOOST_AUTO_TEST_CASE(qr_householder_decomposition_test_hilbert_matrix)
{
  using namespace yayi;
  // testing the householder matrix decomposition.
  typedef boost::numeric::ublas::matrix<double> matrix_type;
  matrix_type m(7, 7);
  
  for(int i = 0; i < 7; i++)
  {
    for(int j = 0; j < 7; j++)
    {
      m(i, j) = 1./(i+1+j+1-1);
    }
  }


  matrix_type msave(m);
  matrix_type q;
  BOOST_CHECK(yayi::qr_householder_decomposition(m, q));

  std::cout << "A (or R)" << std::endl << m << std::endl;
  std::cout << "Q" << std::endl << q << std::endl;
  std::cout << "reconstructed matrix " << boost::numeric::ublas::prod(q, m) << std::endl;
  std::cout << "original matrix " << msave << std::endl;
  BOOST_CHECK_LE(boost::numeric::ublas::norm_frobenius(msave - boost::numeric::ublas::prod(q, m)), 1E-6);

  // checking q is orthogonal
  BOOST_CHECK_LE(
    max_norm(boost::numeric::ublas::prod(boost::numeric::ublas::trans(q), q)-
    boost::numeric::ublas::identity_matrix<double>(q.size1())), 1E-5);
  
  // checking r is upper triangular
  for(int i = 0; i < get_nbcolumns(m); i++)
  {
    for(int j = i+1; j < get_nbrows(m); j++)
    {
      BOOST_CHECK_LE(std::abs(m(j, i)), 1E-3);
    }  
  }

  // check is really the inverse:
  BOOST_CHECK_LE(
    max_norm(
      // solves R X = Q^-1 M = t(Q) M : X should be the identity
      boost::numeric::ublas::solve(
        m,
        boost::numeric::ublas::prod(boost::numeric::ublas::trans(q), msave), // t(Q) * m
        boost::numeric::ublas::upper_tag ())-
      boost::numeric::ublas::identity_matrix<double>(q.size1())),
    1E-5);

  std::cout << boost::numeric::ublas::solve(
        m,
        boost::numeric::ublas::prod(boost::numeric::ublas::trans(q), msave), // t(Q) * m
        boost::numeric::ublas::upper_tag ()) << std::endl;


}

BOOST_AUTO_TEST_SUITE_END()
