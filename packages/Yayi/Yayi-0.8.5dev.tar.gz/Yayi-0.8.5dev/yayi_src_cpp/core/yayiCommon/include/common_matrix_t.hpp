#ifndef YAYI_COMMON_MATRIX_T_HPP__
#define YAYI_COMMON_MATRIX_T_HPP__

/*!@file
 * This file contains matrices definitions (normal, squarred, symmetrical, fixed size)
 * @author Raffi Enficiaud
 */

#include <boost/accumulators/accumulators.hpp>
#include <boost/operators.hpp>



#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/triangular.hpp>
#include <boost/numeric/ublas/symmetric.hpp>
#include <boost/numeric/ublas/matrix_sparse.hpp>
#include <boost/numeric/ublas/io.hpp>



namespace yayi
{

  /*!@defgroup common_matrix_grp Matrix
   * @ingroup common_grp
   * @brief Matrix structures and operations.
   * @{
   */

  /*!@brief Matrix template class with columns and rows specified at compilation time.
   *
   * The dimensions of the matrix being known at compilation time, some classical checks on size become unnecessary.
   * @author Raffi Enficiaud
   */
  template <class T, int I_row, int J_columns>
  struct s_fixed_size_matrix :
    boost::additive< s_fixed_size_matrix<T, I_row, J_columns> >
  {
  public:
    //! Type of the stored elements
    typedef T value_type;
    
    //! Type of the reference
    typedef typename boost::add_reference<T>::type reference;

    //! Type of the const reference
    typedef typename boost::add_reference<typename boost::add_const<T>::type>::type const_reference;
    
    //! Type of this matrix
    typedef s_fixed_size_matrix<T, I_row, J_columns> this_type;
    
    //! Type of a minor matrix where exactly one row and one column have been removed
    typedef s_fixed_size_matrix<T, I_row-1, J_columns-1> unitary_submatrix_type;
    
    //! Type of the transposed matrix
    typedef s_fixed_size_matrix<T, J_columns, I_row> transposed_type;
    
    typedef unsigned int size_type;

  private:
    BOOST_STATIC_ASSERT(I_row > 0);
    BOOST_STATIC_ASSERT(J_columns > 0);

    // The shared_ptr prevents from some waste copies
    T data[I_row * J_columns];

  public:
    //! Default contructor
    s_fixed_size_matrix() {}

    #if 0
    // raffi: no need
    //! Copy constructor
    s_fixed_size_matrix(const this_type& r_)
    {
      for(int i = 0; i < I_row * J_columns; i++)
        data[i] = r_.data[i];
    }
    #endif

    //! Value constructor
    s_fixed_size_matrix(int i_row, int j_colums, T const& value)
    {
      assert(i_row == I_row && j_colums == J_columns);
      for(int i = 0; i < I_row * J_columns; i++)
        data[i] = value;
    }

    //!@name Element access
    //!@{
    reference operator()(int i_row, int j_colums)
    {
      assert(i_row >= 0 && i_row < I_row);
      assert(j_colums >= 0 && j_colums < J_columns);
      return data[i_row * J_columns + j_colums];
    }
    const_reference operator()(int i_row, int j_colums) const
    {
      assert(i_row >= 0 && i_row < I_row);
      assert(j_colums >= 0 && j_colums < J_columns);
      return data[i_row * J_columns + j_colums];
    }
    //!@}

    //! Resize the matrix
    //! This method does nothing, but test the given shape is the same as the one
    //! defined at compilation time. The method exists in order to have the same
    //! interface as other matrices
    bool resize(int i, int j) const
    {
      return i == I_row && j == J_columns;
    }


    //! @name Arithmetic operators
    //! @{
    
    //! Matrix addition
    this_type& operator+=(const this_type& r_)
    {
      for(int i = 0, j = I_row * J_columns; i < j; i++)
        data[i] += r_.data[i];

      return *this;
    }

    //! Matrix subtraction
    this_type& operator-=(const this_type& r_)
    {
      for(int i = 0, j = I_row * J_columns; i < j; i++)
        data[i] -= r_.data[i];

      return *this;
    }


    /*! Matrix multiplication
     *  The right operand should be of compatible dimension, which is checked at compilation time.
     *  @todo check the returned storage type 
     *  @note the internal computations are made in "double", which is false in many cases.
     */
    template <class K, int L_colums>
    s_fixed_size_matrix<K, I_row, L_colums>
      operator*(const s_fixed_size_matrix<K, J_columns, L_colums>  & r_) const
    {
      s_fixed_size_matrix<K, I_row, L_colums> out;
      for(int i = 0; i < I_row; i++)
      {
        for(int j = 0; j < L_colums; j++)
        {
          double acc(0);
          for(int k = 0; k < J_columns; k++)
          {
            acc += (*this)(i, k) * r_(k, j);
          }
          out(i,j) = acc;
        }
      }
      return out;
    }
    
    /*! Multiplication by a scalar
     *  @note the fact that U is scalar is not checked here, which could lead to some compilation error
     *  during the compilation of an expression such as @c "m *= matrix_expression", where matrix_expression
     *  is eg. an ublas matrix. 
     */
    template <class U>
    this_type& operator*=(U const& scalar)
    {
      for(int i = 0, j = I_row * J_columns; i < j; i++)
        data[i] *= scalar;
      return *this;
    }

    //! @}

    //! @name Submatrices
    //! @{

    //! Returns a submatrix, without row i and column j
    unitary_submatrix_type unitary_submatrix(int i, int j) const
    {
      unitary_submatrix_type out;

      for(int ii = 0, iii = 0; ii < I_row; ii++)
      {
        if(ii == i)
          continue;
        for(int jj = 0, jjj = 0; jj < j; jj ++, jjj++)
        {
          out(iii, jjj) = (*this)(ii, jj);
        }
        for(int jj = j+1, jjj = j; jj < J_columns; jj ++, jjj++)
        {
          out(iii, jjj) = (*this)(ii, jj);
        }
        iii ++;
      }

      return out;
    }
    //! @}

    //! @name Transpose
    //! @{
    transposed_type transpose() const
    {
      transposed_type out;
      for(int i = 0; i < I_row; i++)
      {
        for(int j = 0; j < J_columns; j++)
        {
          out(j, i) = (*this)(i,j);
        }

      }
      return out;
    }

    //! @}


    //!@name Interface to boost::uBlas
    //!@{
    
    //! Number of rows
    size_type size1() const
    {
      return I_row;
    }

    //! Number of columns
    size_type size2() const
    {
      return J_columns;
    }
    
    //! Assignement from another matrix implementing the matrix_expression concept (uBlas)
    template <class matrix_t>
    this_type& assign(matrix_t const &right)
    {
      assert(right.size1() == size1());
      assert(right.size2() == size2());
      T* current = data;
      for(size_type row = 0; row < size1(); row++)
      {
        for(size_type column = 0; column < size2(); column++, current++)
        {
          *current = right(row, column);
        }        
      }
      return *this;
    }
    
    //! Assignement from another matrix implementing the matrix_expression concept (uBlas)
    template <class matrix_t>
    this_type& operator=(matrix_t const &right)
    {
      return this->template assign(right);
    }
    
    /*! Swap from another matrix implementing the matrix_expression concept (uBlas)
     * @warning swap is not of constant time complexity
     * @warning since this matrix is typed on its size, the swap will be possible only with matrix of the same size. An
     * assertion will be raised otherwise
     */
    template <class matrix_t>
    void swap(matrix_t const &right)
    {
      if((right.size1() != size1()) || (right.size2() == size2()))
        throw std::runtime_error("swap: incompatible matrices");
      T* current = data;
      for(size_type row = 0; row < size1(); row++)
      {
        for(size_type column = 0; column < size2(); column++, current++)
        {
          std::swap(*current, right(row, column));
        }        
      }
      return *this;
    }    

    //! Addition from another matrix implementing the matrix_expression concept (uBlas)
    template <class matrix_t>
    this_type& plus_assign(matrix_t const &right)
    {
      assert(right.size1() == size1());
      assert(right.size2() == size2());
      T* current = data;
      for(size_type row = 0; row < size1(); row++)
      {
        for(size_type column = 0; column < size2(); column++, current++)
        {
          *current += right(row, column);
        }        
      }
      return *this;
    }

    //! Addition from another matrix implementing the matrix_expression concept (uBlas)
    template <class matrix_t>
    this_type& operator+=(matrix_t const &right)
    {
      return this->template plus_assign(right);
    }   

    //! Subtraction from another matrix implementing the matrix_expression concept (uBlas)
    template <class matrix_t>
    this_type& minus_assign(matrix_t const &right)
    {
      assert(right.size1() == size1());
      assert(right.size2() == size2());
      T* current = data;
      for(size_type row = 0; row < size1(); row++)
      {
        for(size_type column = 0; column < size2(); column++, current++)
        {
          *current -= right(row, column);
        }        
      }
      return *this;
    }
    
    //! Subtraction from another matrix implementing the matrix_expression concept (uBlas)
    template <class matrix_t>
    this_type& operator-=(matrix_t const &right)
    {
      return this->template minus_assign(right);
    }      
    
    
    /*
    
    // not finished: the colmumn iterator should be done a bit differently
    template <class U, int step>
    struct internal_iterator :
      public boost::add_pointer<U>::type,
      std::iterator<std::random_access_iterator_tag, U>
    {
      typedef internal_iterator<U, step> this_type;
      U *current;
      
      internal_iterator(U* u) : current(u){}
      
      this_type& operator++()
      {
        current += step;
        return *this;
      }
    };
    
    typedef internal_iterator<T, 1> iterator2;
    typedef internal_iterator<typename boost::add_const<T>::type, 1> const_iterator2;
    iterator2 begin2()
    {
      return iterator2(data);
    }
    iterator2 end2()
    {
      return iterator2(data);
    }
    */
    
    //!@}

  };




  /*!@brief A class representing an upper tringular matrix
   *
   * For any instance M of this kind of matrix, if i > j, M[i,j] = 0. Note that the number of stored elements is I*J / 2 
   * (interesting for very large matrices).
   * @author Raffi Enficiaud
   */
  template <class T>
  struct s_upper_triangular_matrix : boost::numeric::ublas::triangular_matrix<T, boost::numeric::ublas::upper>
  {
  private:
    typedef boost::numeric::ublas::triangular_matrix<T, boost::numeric::ublas::upper> parent_type;

  public:
    typedef s_upper_triangular_matrix<T> this_type;
    typedef T value_type;

  public:
    //! Default contructor
    s_upper_triangular_matrix() : parent_type() {}

    //! Copy constructor
    s_upper_triangular_matrix(const this_type& r_) : parent_type(static_cast<parent_type>(r_)){}

    //! Copy constructor
    s_upper_triangular_matrix(const int i_row, int j_colum) : parent_type(i_row, j_colum){}

    bool resize(const int i_row) {
      parent_type::resize (i_row, i_row);
      return true;
    }

    int size() const {
      return parent_type::size1();
    }

  };



  /*!@brief A class representing a (square) symmetric matrix
   *
   * For any instance M of this kind of matrix, M(i,j) = M(j, i). Note that the number of stored elements is I*J / 2 (interesting for very large matrices).
   * This is a proxy from boost::numeric::ublas::symmetric_matrix
   * @author Raffi Enficiaud
   */
  template <class T, class storage_type = boost::numeric::ublas::lower>
  struct s_symmetric_matrix : boost::numeric::ublas::symmetric_matrix<T, storage_type>
  {
  private:
    typedef boost::numeric::ublas::symmetric_matrix<T, storage_type> parent_type;

  public:
    typedef s_symmetric_matrix <T> this_type;
    typedef T value_type;

  public:
    //! Default contructor
    s_symmetric_matrix () : parent_type() {}

    //! Copy constructor
    s_symmetric_matrix (const this_type& r_) : parent_type(static_cast<parent_type>(r_)){}

    //! Copy constructor
    s_symmetric_matrix (const int i_row) : parent_type(i_row, i_row){}

    bool resize(const int i_row) {
      parent_type::resize (i_row);
      return true;
    }

    int size() const {
      return parent_type::size1();
    }
  };


  /*!@brief A class representing a (square) anti-symmetric matrix
   *
   * For any instance M of this kind of matrix, M(i, j) = - M(j, i). Note that the number of stored elements is I*J / 2 (interesting for very large matrices).
   * This is a proxy from boost::numeric::ublas::symmetric_matrix
   * @author Raffi Enficiaud
   */
  template <class T, class storage_type = boost::numeric::ublas::lower>
  struct s_antisymmetric_matrix : boost::numeric::ublas::symmetric_matrix<T, storage_type>
  {
  private:
    typedef boost::numeric::ublas::symmetric_matrix<T, storage_type> parent_type;

    const T diag;
    typedef typename parent_type::const_reference const_reference;
    typedef typename parent_type::reference reference;

  public:
    typedef s_antisymmetric_matrix <T, storage_type> this_type;
    typedef T value_type;

  public:
    //! Default contructor
    s_antisymmetric_matrix () : parent_type(), diag(0) {}

    //! Copy constructor
    s_antisymmetric_matrix (const this_type& r_) : parent_type(static_cast<parent_type>(r_)), diag(0) {}

    //! Copy constructor
    s_antisymmetric_matrix (const int i_row) : parent_type(i_row, i_row), diag(0) {}

    bool resize(const int i_row) {
      parent_type::resize (i_row);
      return true;
    }

    T operator()(int i, int j) const {
      if(i == j)
        return diag;

      // erreur, il faut que cette operation soit dŽfinie pour le type T (par ex. espace vectoriel sur corps)
      return (i > j ? 1:-1) * parent_type::operator()(i, j);

    }

  };


  //! Returns the number of rows of the matrix
  //!@{
  template <class matrix_t>
  int get_nbrows(matrix_t const& m)
  {
    return static_cast<int>(m.size1());
  }
  template <class T, int I_row, int J_columns>
  int get_nbrows(s_fixed_size_matrix<T, I_row, J_columns> const&)
  {
    return I_row;
  }
  //!@}
  
  //!Returns the number of columns of the matrix
  //!@{
  template <class matrix_t>
  int get_nbcolumns(matrix_t const& m)
  {
    return static_cast<int>(m.size2());
  }
  
  template <class T, int I_row, int J_columns>
  int get_nbcolumns(s_fixed_size_matrix<T, I_row, J_columns> const&)
  {
    return J_columns;
  }
  //!@}


  //! Utility template class returning the type of the unitary submatrix (without exactly one row and one column)
  template <class matrix_t>
  struct s_unitary_submatrix_t
  {
    typedef matrix_t type;
  };

  template <class T, int I_row, int J_columns>
  struct s_unitary_submatrix_t< s_fixed_size_matrix<T, I_row, J_columns> >
  {
    typedef typename s_fixed_size_matrix<T, I_row, J_columns>::unitary_submatrix_type type;
  };


  //! Returns the type of the inverse of a matrix.
  //!@{
  template <class matrix_t>
  struct s_inverse_matrix_t
  {
    typedef matrix_t type;
  };

  template <class T, int I_row>
  struct s_inverse_matrix_t< s_fixed_size_matrix<T, I_row, I_row> >
  {
    typedef s_fixed_size_matrix<double, I_row, I_row> type;
  };
  //!@}


  //!@name Matrix norms
  //!@{
  
  /*!@brief Computes the Frobenius norm of a matrix.
   *
   * The Frobenius norm is defined as @f[\left\|A\right\| = \sqrt{\sum_{i,j} a_{i,j}^2} @f] for
   * any matrix @f$A = (a_{i,j})@f$. 
   * @note The current implementation only works for non complex types.
   * @deprecated the implementation exists in boost::uBlas. 
   */
  template <class matrix_t>
  double frobenius_norm(const matrix_t& m)
  {
    double acc = 0;
    for(int line = 0, line_max = get_nbrows(m); line < line_max; line++)
    {
      for(int column = 0, column_max = get_nbcolumns(m); column < column_max; column++)
      {
        typename matrix_t::reference v = m(line, column);
        acc += v * v;
      }
    }
    return std::sqrt(acc);
  }
  
  /*!@fn template <class matrix_t> implementation-defined max_norm(const matrix_t& m)
   * @brief Computes the Max norm of a matrix.
   *
   * The Frobenius norm is defined as @f[\left\|A\right\| = \max_{i,j} |a_{i,j}| @f] for
   * any matrix @f$A = (a_{i,j})@f$. 
   * @note The current implementation only works for non complex types.
   */
  template <class matrix_t>
  typename matrix_t::value_type max_norm(const matrix_t& m)
  {
    typename matrix_t::value_type current_max = std::numeric_limits<typename matrix_t::value_type>::min();
    for(int line = 0, line_max = get_nbrows(m); line < line_max; line++)
    {
      for(int column = 0, column_max = get_nbcolumns(m); column < column_max; column++)
      {
        typename matrix_t::value_type v = std::abs(m(line, column));
        if(current_max < v)
        {
          current_max = v;
        }
      }
    }
    return current_max;
  }
    
  //!@}

  using boost::numeric::ublas::prod;

  //!@}

}



#endif /* YAYI_COMMON_MATRIX_T_HPP__ */

