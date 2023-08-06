#ifndef YAYI_COMMON_PIXELS_T_HPP__
#define YAYI_COMMON_PIXELS_T_HPP__



/*!@file
 * This file contains the definitions for the template pixels
 */

#include <functional>
#include <boost/mpl/int.hpp>
#include <boost/utility/enable_if.hpp>
#include <boost/type_traits.hpp>
#include <yayiCommon/common_errors.hpp>


namespace yayi
{
  /*!@addtogroup common_pixel_grp
   * @{
   */

  using namespace boost;

  template <class T, class dimension_>
  struct s_compound_pixel_t;
  template <class T>
  struct s_compound_pixel_t<T, mpl::int_<3> >;



  /*!@brief Template structure for storing multichannel pixels.
   *
   * @note Monochannel pixels are encoded in native types (as much as possible.)
   *
   * @tparam T the type encoded in each channel of the pixel
   * @tparam dimension_ the dimension of the pixel, ie. its number of channels
   * @author Raffi Enficiaud
   */
  template <class T, class dimension_ = mpl::int_<1> >
  struct s_compound_pixel_t
  {
  public:
    typedef dimension_                        dimension;
    typedef s_compound_pixel_t<T, dimension>  this_type;
    typedef T                                 value_type;


  public:
    T array_pixel[dimension::value];

  public:

    //! Default constructor
    s_compound_pixel_t(){}

    //! Constant assignment constructor
    s_compound_pixel_t(const T& r_)
    {
      for(int i = 0; i < dimension::value; i++) array_pixel[i] = r_;
    }

    //! Copy constructor
    s_compound_pixel_t(const this_type& r_)
    {
      for(int i = 0; i < dimension::value; i++) array_pixel[i] = r_[i];
    }

    //! Constructor from another pixel of same dimension but of different type
    template <class U>
    s_compound_pixel_t(const s_compound_pixel_t<U, dimension>& r_, typename boost::enable_if<boost::is_convertible<U, T> >::type* dummy = 0)
    {
      // We should assert U can be transformed into T (see enable_if for constructors)
      for(int i = 0; i < dimension::value; i++) array_pixel[i] = static_cast<T>(r_[i]);
    }

    //! Assignment operator
    this_type& operator=(const this_type& r_) throw()
    {
      for(int i = 0; i < dimension::value; i++) array_pixel[i] = r_[i];
      return *this;
    }

    //! Index operator for channel access
    //! @param i the desired channel
    T& operator[](const int i) YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(i < dimension::value && i >= 0, "Unsupported dimension");
      return array_pixel[i];
    }

    //! Index operator for (const) channel access
    //! @param i the desired channel
    const T& operator[](const int i) const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(i < dimension::value && i >= 0, "Unsupported dimension");
      return array_pixel[i];
    }

    /*template<class U>
    friend bool operator==(const this_type& l, const s_compound_pixel_t<U, dimension>& r) throw() {
      for(int i = 0; i < dimension_::value; i++) if(l.array_pixel[i] != r.array_pixel[i]) return false;
      return true;
    }*/

    template<class TT, class U, class dim>
    friend bool operator==(const s_compound_pixel_t<TT, dim>& l, const s_compound_pixel_t<U, dim>& r) throw();

    template<class U>
    friend bool operator!=(const this_type& l, const s_compound_pixel_t<U, dimension>& r) throw() {
      for(int i = 0; i < dimension_::value; i++) if(l.array_pixel[i] != r.array_pixel[i]) return true;
      return false;
    }

    template<class stream_t, class U, class dim>
    friend stream_t& operator<<(stream_t& o, const s_compound_pixel_t<U, dim>& r) throw();
  };



  /*!@brief Specializing of pixel for 3 dimensionnal color pixels
   *
   * @author Raffi Enficiaud
   */
  template <class T>
  struct s_compound_pixel_t<T, mpl::int_<3> >
  {
  public:
    typedef mpl::int_<3>                          dimension;
    typedef s_compound_pixel_t<T, mpl::int_<3> >  this_type;
    typedef T                                     value_type;

  public:
    T a,b,c;

  public:
    //! Default constructor
    s_compound_pixel_t(){}
    //! Constant assignment constructor
    s_compound_pixel_t(const T& a_, const T& b_, const T& c_) : a(a_), b(b_), c(c_){}
    //! Constant assignment constructor
    s_compound_pixel_t(const T& r_) : a(r_), b(r_), c(r_){}
    //! Copy constructor (needed ?)
    s_compound_pixel_t(const this_type& r_) : a(r_.a), b(r_.b), c(r_.c){}

    template <class U>
    s_compound_pixel_t(const s_compound_pixel_t<U, dimension>& r_, typename boost::enable_if<boost::is_convertible<U, T> >::type* dummy = 0):
       a(static_cast<T>(r_.a)), b(static_cast<T>(r_.b)), c(static_cast<T>(r_.c))
    {}

    this_type& operator=(const this_type& r_) throw()
    {
      a = r_.a; b = r_.b; c = r_.c;
      return *this;
    }

    T& operator[](const int i) YAYI_THROW_DEBUG_ONLY__
    {
      if(i == 0) return a;
      else if(i == 1) return b;
      DEBUG_ASSERT(i == 2, "Unsupported dimension : " + int_to_string(i) + " > #dimension=" + int_to_string(dimension::value));
      return c;
    }

    const T& operator[](const int i) const YAYI_THROW_DEBUG_ONLY__
    {
      if(i == 0) return a;
      else if(i == 1) return b;
      DEBUG_ASSERT(i == 2, "Unsupported dimension : " + int_to_string(i) + " > #dimension=" + int_to_string(dimension::value));
      return c;
    }

    //! Strict equality operator
    bool operator==(const this_type& r_) const throw() {
      return (a == r_.a) && (b == r_.b) && (c == r_.c);
    }
    //! Inequality operator
    bool operator!=(const this_type& r_) const throw() {
      return (a != r_.a) || (b != r_.b) || (c != r_.c);
    }

    template<class stream_t, class U, class dim>
    friend stream_t& operator<<(stream_t& o, const s_compound_pixel_t<U, dim >& r) throw();

  };



  //! Equality operator for pixels defined as @ref s_compound_pixel_t
  template<class T, class U, class dimension_>
  inline bool operator==(const s_compound_pixel_t<T, dimension_>& l, const s_compound_pixel_t<U, dimension_>& r) throw() {
    for(int i = 0; i < dimension_::value; i++) if(l.array_pixel[i] != r.array_pixel[i]) return false;
    return true;
  }



  //! Streaming function
  template <class stream_t, class T, class dimension>
  inline stream_t& operator<<(stream_t& o, const s_compound_pixel_t<T, dimension>& r) throw() {
    for(int i = 0; i < dimension::value; i++) {
      o << r[i];
      o << ", ";
    }
    return o;
  }



  typedef s_compound_pixel_t< yaUINT8,  mpl::int_<3> > pixel8u_3;     //!< Type for 3 channels pixels, 8 bits unsigned
  typedef s_compound_pixel_t< yaUINT8,  mpl::int_<4> > pixel8u_4;     //!< Type for 4 channels pixels, 8 bits unsigned

  typedef s_compound_pixel_t< yaUINT16, mpl::int_<3> > pixel16u_3;    //!< Type for 3 channels pixels, 16 bits unsigned
  typedef s_compound_pixel_t< yaUINT16, mpl::int_<4> > pixel16u_4;    //!< Type for 4 channels pixels, 16 bits unsigned

  typedef s_compound_pixel_t< yaUINT32, mpl::int_<3> > pixel32u_3;    //!< Type for 3 channels pixels, 32 bits unsigned
  typedef s_compound_pixel_t< yaUINT32, mpl::int_<4> > pixel32u_4;    //!< Type for 4 channels pixels, 32 bits unsigned

  typedef s_compound_pixel_t< yaUINT64, mpl::int_<3> > pixel64u_3;    //!< Type for 3 channels pixels, 64 bits unsigned
  typedef s_compound_pixel_t< yaUINT64, mpl::int_<4> > pixel64u_4;    //!< Type for 4 channels pixels, 64 bits unsigned

  typedef s_compound_pixel_t< yaINT8,  mpl::int_<3> > pixel8s_3;     //!< Type for 3 channels pixels, 8 bits signed
  typedef s_compound_pixel_t< yaINT8,  mpl::int_<4> > pixel8s_4;     //!< Type for 4 channels pixels, 8 bits signed

  typedef s_compound_pixel_t< yaINT16, mpl::int_<3> > pixel16s_3;    //!< Type for 3 channels pixels, 16 bits signed
  typedef s_compound_pixel_t< yaINT16, mpl::int_<4> > pixel16s_4;    //!< Type for 4 channels pixels, 16 bits signed

  typedef s_compound_pixel_t< yaINT32, mpl::int_<3> > pixel32s_3;    //!< Type for 3 channels pixels, 32 bits signed
  typedef s_compound_pixel_t< yaINT32, mpl::int_<4> > pixel32s_4;    //!< Type for 4 channels pixels, 32 bits signed

  typedef s_compound_pixel_t< yaINT64, mpl::int_<3> > pixel64s_3;    //!< Type for 3 channels pixels, 64 bits signed
  typedef s_compound_pixel_t< yaINT64, mpl::int_<4> > pixel64s_4;    //!< Type for 4 channels pixels, 64 bits signed

  typedef s_compound_pixel_t< yaF_simple,  mpl::int_<3> > pixelFs_3;  //!< Type for 3 channels pixels, float simple precision
  typedef s_compound_pixel_t< yaF_simple,  mpl::int_<4> > pixelFs_4;  //!< Type for 4 channels pixels, float simple precision

  typedef s_compound_pixel_t< yaF_double,  mpl::int_<3> > pixelFd_3;  //!< Type for 3 channels pixels, float double precision
  typedef s_compound_pixel_t< yaF_double,  mpl::int_<4> > pixelFd_4;  //!< Type for 4 channels pixels, float double precision


  /*!@brief Returns the dimension of a pixel.
   *
   * Returns obviously 1 for scalar types.
   */
  template <class pixel_t>
  struct s_get_pixel_dimension
  {
    static const int dimension = 1;
  };

  //! Specialization of s_get_pixel_dimension for complex pixels.
  template <class U>
  struct s_get_pixel_dimension< std::complex<U> >
  {
    static const int dimension = 2;
  };

  //! Specialization of s_get_pixel_dimension for s_compound_pixel_t pixels.
  template <class U, class V>
  struct s_get_pixel_dimension< s_compound_pixel_t<U, V> >
  {
    static const int dimension = s_compound_pixel_t<U, V>::dimension::value;
  };



  /*!@brief Meta-function returning the scalar type of a pixel.
   *
   * The scalar type indicates somewhat the type of each channel of the pixel.
   * @tparam pixel_t the type of the (possibly) compound pixel.
   *
   * This meta-function may be used for eg. casting:
   * @code
   * typedef ... pixel_t;
   * Image<pixel_t> im;
   * /// ...
   * im.pixel(c2D(10,10)) = static_cast<s_get_pixel_scalar_type<pixel_t>::type>(v); // works the same way for s_compound_pixel_t or eg. yaUINT32.
   * @endcode
   */
  template <class pixel_t>
  struct s_get_pixel_scalar_type
  {
    typedef pixel_t type;
  };

  //! Specialisation of s_get_pixel_scalar_type for s_compound_pixel_t pixels.
  template <class U>
  struct s_get_pixel_scalar_type< std::complex<U> >
  {
    typedef U type;
  };


  //! Specialisation of s_get_pixel_scalar_type for s_compound_pixel_t pixels.
  template <class U, class V>
  struct s_get_pixel_scalar_type< s_compound_pixel_t<U, V> >
  {
    typedef U type;
  };

  //! @} // defgroup common_pixel_grp
}

namespace std
{

  /*!@brief Lexicographical comparison of pixels
   *
   * This function is provided for convenience when an ordering on the pixel is required.
   * @author Raffi Enficiaud.
   */
  template <class U, class dim>
  struct less< yayi::s_compound_pixel_t<U, dim> > :
    public binary_function<yayi::s_compound_pixel_t<U, dim>, yayi::s_compound_pixel_t<U, dim>, bool>
  {
    typedef yayi::s_compound_pixel_t<U, dim> pixel_t;
    bool operator()(pixel_t const& l_, pixel_t const &r_) const throw()
    {
      for(typename dim::value_type i = 0; i < dim::value; i++)
      {
        if(l_[i] != r_[i]) return l_[i] < r_[i];
      }
      return false;

    }

  };


}


#endif


