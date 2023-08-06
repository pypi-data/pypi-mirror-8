#ifndef YAYI_COMMON_MATRIX_INVERSION_T_HPP__
#define YAYI_COMMON_MATRIX_INVERSION_T_HPP__

/*!@file
 * This file defines some functions for matrix inversion. Cofactor (small matrices) and Householder (large matrices) methods
 * @author Raffi Enficiaud
 */

#include <yayiCommon/include/common_matrix_t.hpp>
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/matrix_proxy.hpp>
#include <boost/numeric/ublas/vector_proxy.hpp>

namespace yayi
{
  /*!@addtogroup common_matrix_grp
   * @{
   */

  // forward definitions are currently compulsory due to some VC++ limitations
  // the order of the declarations does matter
  template <class T>
  bool determinant(s_fixed_size_matrix<T, 2, 2> const &m, T& determinant_);
  template <class T>
  bool determinant(s_fixed_size_matrix<T, 1, 1> const &m, T& determinant_);
  template <class T, int I>
  bool determinant(s_fixed_size_matrix<T, I, I> const &m, T& determinant_);
  template <class matrix_t>
	bool determinant(matrix_t const &m, typename matrix_t::value_type &determinant_);
  template <class T, int I, int J>
  bool determinant(s_fixed_size_matrix<T, I, J> const &m, T& determinant_);


  //!@brief Computes the determinant of a matrix using the Laplace method (relevant for small matrices).
  //!@todo adapt the internal @c unitary_submatrix calls to external function (with a specialisation for general matrices).
  template <class matrix_t>
	bool determinant(matrix_t const &m, typename matrix_t::value_type &determinant_)
  {
    // only for square matrices
	  if(get_nblines(m) != get_nbcolumns(m))
    {
      return false;
    }
    assert(get_nblines(m) != 0);

    if(get_nblines(m) == 2)
    {
      determinant_ = m(0, 0) * m(1, 1) - m(1, 0) * m(0, 1);
      return true;
    }
    if(get_nblines(m) == 1)
    {
      determinant_ = m(0,0);
      return true;
    }

    typename matrix_t::value_type det = 0;
    for(int i = 0; i < get_nblines(m); i++)
    {
      typename s_unitary_submatrix_t<matrix_t>::type submatrix_i_0(m.unitary_submatrix(i, 0));
      typename matrix_t::value_type det_curr;
      if(!determinant(submatrix_i_0, det_curr))
        return false;
      det += (i % 2 == 0 ? 1:-1) * m(i, 0) * det_curr;
    }

    determinant_ = det;
    return true;
  }

  //! Default determinant implementation for fixed size matrices. 
  template <class T, int I, int J>
  bool determinant(s_fixed_size_matrix<T, I, J> const &m, T& determinant_)
  {
    return false;
  }
  
  //!@brief Determinant of a matrix using the Laplace method.
  //!@note This method is highly inefficient for large matrices.
  template <class T, int I>
  bool determinant(s_fixed_size_matrix<T, I, I> const &m, T& determinant_)
  {
    typedef s_fixed_size_matrix<T, I, I> matrix_t;
    T det = 0;
    for(int i = 0; i < get_nbrows(m); i++)
    {
      typename s_unitary_submatrix_t<matrix_t>::type submatrix_i_0(m.unitary_submatrix(i, 0));
      T det_curr;
      if(!determinant(submatrix_i_0, det_curr))
        return false;
      det += (i % 2 == 0 ? 1:-1) * m(i, 0) * det_curr;
    }
    determinant_ = det;
    return true;
  }
  template <class T>
  bool determinant(s_fixed_size_matrix<T, 2, 2> const &m, T& determinant_)
  {
    determinant_ = m(0, 0) * m(1, 1) - m(1, 0) * m(0, 1);
    return true;
  }
  template <class T>
  bool determinant(s_fixed_size_matrix<T, 1, 1> const &m, T& determinant_)
  {
    determinant_ = m(0, 0);
    return true;
  }



  //! Returns the inverse of the current matrix
  template <class matrix_t, class matrix_out_t/* = typename s_inverse_matrix_t<matrix_t>::type*/ >
  bool inverse_matrix(matrix_t const& m, matrix_out_t& mout)
  {
    // only square matrices
	  if(get_nblines(m) != get_nbcolumns(m))
    {
      return false;
    }
    assert(get_nblines(m) != 0);
      
    if( get_nblines(mout) != get_nblines(m) || 
        get_nbcolumns(mout) != get_nblines(m) || 
        !mout.resize(get_nblines(m), get_nblines(m)) )
    {
      // shape error
      return false;
    }
	      
    if(get_nblines(m) == 1)
    {
      mout(0,0) = 1./m(0,0);
      return true;
    }
    else if(get_nblines(m) == 2)
    {
      typename matrix_t::value_type det;
      if(!determinant(m, det) || det == 0)
        return false;
      mout(0,0) = m(1,1);
      mout(1,0) = -m(1,0);
      mout(0,1) = -m(0,1);
      mout(1,1) = m(0,0);
        
      mout *= 1./det;
      return true;
    }


    typename matrix_t::value_type det;
    if(!determinant(m, det) || det == 0)
      return false;
      
	  matrix_out_t comatrix(get_nblines(m), get_nblines(m));
	      
	  for(unsigned i = 0; i < get_nblines(m); i++)
	  {
		  for(unsigned j = 0; j < get_nblines(m); j++)
		  {
        typename s_unitary_submatrix_t<matrix_t>::type submatrix_i_j(m.unitary_submatrix(i, j));
        typename matrix_t::value_type det_sub;
        if(!determinant(submatrix_i_j, det_sub))
          return false;
			  comatrix(i, j) = ((i+j) % 2 == 0 ? 1:-1) * det_sub;
		  }
	  }

	  mout = comatrix.transpose();
    mout*= 1./det;

    return true;
  }




  /*!QR decomposition of a matrix using the Householder scheme.
   *
   * The function decompose the input matrix into two matrices, Q and R, known as QR decomposition. 
   * This decomposition is known to be more stable than LU decomposition. 
   * The implementation used in the code use the Householder method.
   * The implementation is such that it limits the number of additional temporary data.
   * @warning The input matrix is modified during the computation, and will receive the R part of the decomposition. The Q part will be stored in matrix_q.
   * @warning The implementation makes use of matrix views (submatrices, column/row matrices). Currently using the boost matrix model.
   * @note the returned R matrix is upper-triangular.
   * @author Raffi Enficiaud.
   */
  template <class matrix_t>
  bool qr_householder_decomposition(matrix_t& input_matrix, matrix_t& matrix_q)
  {
    namespace bu = boost::numeric::ublas;

    typedef typename matrix_t::value_type value_type;

    typedef bu::matrix_range<matrix_t> matrix_range_t;
    typedef bu::matrix_column<matrix_range_t> column_t;
    typedef bu::matrix_row<matrix_range_t> row_t;


    const int nb_rows(get_nbrows(input_matrix)), nb_columns(get_nbcolumns(input_matrix));
    matrix_q.resize(nb_rows, nb_columns);
    matrix_q = bu::identity_matrix<value_type>(nb_columns);

    // we try to design an algorithm for the square case. If someone needs a more general case, the
    // he can tell me or give me patch. 
    assert(nb_rows == nb_columns);

    for(int current_column = 0; current_column < nb_columns-1; current_column++)
    {
      
      matrix_range_t ai(input_matrix,
        bu::range(current_column, nb_rows),
        bu::range(current_column, nb_columns));
    
      // doing a copy of the first column
      bu::vector<value_type> first_column(bu::column(ai, 0));

      double const n2 = bu::norm_2(first_column); // check the existance of norm_2 ^2
      if(n2 == 0)
      {
        // one of the column is null, the matrix is not factorisable
        return false;
      }
      
      first_column[0] -= n2 * (first_column[0] >= 0 ? 1:-1);

      assert(ai.size1() == nb_rows - current_column);
      assert(ai.size2() == nb_columns - current_column);

      double const n3 = bu::norm_2(first_column);
      double const mult_inv_norm2 = 2./(n3 * n3); // for the complex case, replace the computation of this (mostly the "2")
    
    
      // this is 2 u / |u|^2 = 2 v / |u|
      // however, using this induce less accuracy
      //bu::vector<value_type> vdiv(first_column*mult_inv_norm2);

      // computation of R=QA for the current minor A using the sparse representation of the current Q minor
      // update of Q, the first i columns are not changed

      // we can also start with i = 1, since the first column is (n2, 0...0)
      for(unsigned int i = 0; i < ai.size2(); i++)
      {
        // reference to the i column vector of A
        column_t column_i(bu::column(ai, i));
        
        // for each column ai=(a1, a2... an) of A, we should compute
        // QA = (I - 2*v*vT) * ai = ai - 2*(v*vT)*ai = ai - 2*v * dotprod(v, ai)
        column_i -= (bu::inner_prod(column_i, first_column)*mult_inv_norm2) * first_column; // may be replaced by vdiv, but seems to loose accuracy
      }
      
      
      // update of Q
      // line by line, in order to avoid storing an intermediate matrix
      matrix_range_t qminor(matrix_q, bu::range(0, nb_rows), bu::range(current_column, nb_columns));
      for(int i = 0; i < nb_rows; i++)
      {
        row_t qminorrow_i(bu::row(qminor, i));
        double const inner_prod = bu::inner_prod(qminorrow_i, first_column)*mult_inv_norm2;
        assert(first_column.size() == qminor.size2());
        for(unsigned int j = 0; j < qminor.size2(); j++)
        {
          qminorrow_i(j) -= inner_prod * first_column(j);
        }
      }
      
    }
    
    return true;
  }


  //! @}
			
}
#endif /*YAYI_COMMON_MATRIX_INVERSION_T_HPP__*/
