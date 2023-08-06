#ifndef YAYI_DISTANCES_OP_T_HPP__
#define YAYI_DISTANCES_OP_T_HPP__

/*!@file
 * This file contains the basic operations for computing distances
 * @author Raffi Enficiaud
 */

#include <yayiCommon/common_types.hpp>
#include <functional>

#include <boost/static_assert.hpp>
#include <boost/mpl/has_xxx.hpp>
#include <boost/mpl/if.hpp>
#include <boost/mpl/and.hpp>
#include <boost/type_traits/is_integral.hpp>

BOOST_MPL_HAS_XXX_TRAIT_NAMED_DEF(distance_has_storage_tag, storage_type, false);

 
namespace yayi
{
  namespace distances 
  {
    /*!@defgroup distances_details_grp Distance operators
     * @ingroup distances_grp
     * @{
     */    
  
    /*!@brief Squared euclidian distance between two points
     * 
     * This functor computes the squared euclidian distance between two points. The function returns
     * an integer type if the coordinates are integer.
     */
    template <class source_coordinate_type, class coordinate_type>
    struct s_squared_euclidian_distance_op : 
      std::binary_function<
        source_coordinate_type, 
        coordinate_type, 
        typename mpl::if_< 
          typename mpl::and_<
            boost::is_integral<typename source_coordinate_type::scalar_coordinate_type>, 
            boost::is_integral<typename coordinate_type::scalar_coordinate_type> 
          >,
          yaUINT64, 
          yaF_double>::type
      >
    {
      BOOST_STATIC_ASSERT(static_cast<int>(source_coordinate_type::static_dimensions) == static_cast<int>(coordinate_type::static_dimensions));
      
      //! The type used for accumulating the computations
      typedef typename mpl::if_< 
        typename mpl::and_<
          boost::is_integral<typename source_coordinate_type::scalar_coordinate_type>, 
          boost::is_integral<typename coordinate_type::scalar_coordinate_type> 
        >,
        scalar_coordinate, 
        yaF_double>::type storage_type;
      
      typedef std::binary_function<source_coordinate_type, coordinate_type, storage_type> parent_type;
      typedef typename parent_type::result_type result_type;
      
      result_type operator()(const source_coordinate_type& p1, const coordinate_type &p2) const throw()
      {
        yaF_double acc = 0;
        for(unsigned int i = 0; i < coordinate_type::static_dimensions; i++)
        {
          storage_type const c = p1[i] - p2[i];
          acc += c * c;
        }
        return acc;
      }
    };

    /*!@brief Euclidian distance between two points
     * 
     * This functor computes the euclidian distance between two points
     * @see s_squared_euclidian_distance_op
     */
    template <class source_coordinate_type, class coordinate_type>
    struct s_euclidian_distance_op : s_squared_euclidian_distance_op<source_coordinate_type, coordinate_type>
    {
      BOOST_STATIC_ASSERT(static_cast<int>(source_coordinate_type::static_dimensions) == static_cast<int>(coordinate_type::static_dimensions));
            
      typedef s_squared_euclidian_distance_op<source_coordinate_type, coordinate_type> parent_type;
      typedef yaF_double result_type;
      
      result_type operator()(const source_coordinate_type& p1, const coordinate_type &p2) const throw()
      {
        using namespace std;
        return sqrt(parent_type::operator()(p1, p2));
      }
    };


    /*!@brief l_5 distance between two points
     * 
     * This functor computes the @f$\ell_5@f$ distance between two points.
     * @note this has not practical use appart from testing the exact distance computation algorithm.
     * @see s_squared_euclidian_distance_op
     */
    template <class source_coordinate_type, class coordinate_type>
    struct s_l5_distance_op : std::binary_function<source_coordinate_type, coordinate_type, yaF_double>
    {
      BOOST_STATIC_ASSERT(static_cast<int>(source_coordinate_type::static_dimensions) == static_cast<int>(coordinate_type::static_dimensions));
      
      typedef typename mpl::if_< 
        typename mpl::and_<
          boost::is_integral<typename source_coordinate_type::scalar_coordinate_type>, boost::is_integral<typename coordinate_type::scalar_coordinate_type> >,
          scalar_coordinate, 
          yaF_double>::type computation_type;
      
      typedef std::binary_function<source_coordinate_type, coordinate_type, yaF_double> parent_type;
      typedef typename parent_type::result_type result_type;
          
      result_type operator()(const source_coordinate_type& p1, const coordinate_type &p2) const throw()
      {
        yaF_double acc = 0;
        for(int i = 0; i < coordinate_type::static_dimensions; i++)
        {
          computation_type c = p1[i] - p2[i];
          if(c < 0) c = -c;
          acc += c * c * c * c * c;
        }
        return pow(acc, 0.2);
      }
    };


    /*!@brief Generic l^p distance
     * Functor computing a distance of @f$\ell_p@f$ type, with p = p/q
     *
     * @todo Add compilation time dispatching in case p/q is integer
     * @todo Do less tests in case p and q are of the same sign
     */
    template <class source_coordinate_type, class coordinate_type, int p, int q>
    struct s_lp_distance_op : std::binary_function<source_coordinate_type, coordinate_type, yaF_double>
    {
      BOOST_STATIC_ASSERT(static_cast<int>(source_coordinate_type::static_dimensions) == static_cast<int>(coordinate_type::static_dimensions));
            
      typedef std::binary_function<source_coordinate_type, coordinate_type, yaF_double> parent_type;
      typedef typename parent_type::result_type result_type;

      const double pow1, pow2;

      s_lp_distance_op() : pow1(double(p) / q), pow2(double(q) / p){}
      
      result_type operator()(const source_coordinate_type& p1, const coordinate_type &p2) const throw()
      {
        yaF_double acc = 0;
        for(unsigned int i = 0; i < coordinate_type::static_dimensions; i++)
        {
          typename source_coordinate_type::scalar_coordinate_type c = p1[i] - p2[i];
          if(c < 0)
            acc += std::pow(-c, pow1);
          else
            acc += std::pow(c, pow1);
        }
        return std::pow(acc, pow2);
      }
    };

    //! Specializing of s_lp_distance_op for l^1 norm case.
    template <class source_coordinate_type, class coordinate_type, int p>
    struct s_lp_distance_op<source_coordinate_type, coordinate_type, p, p> : std::binary_function<source_coordinate_type, coordinate_type, yaF_double>
    {
      BOOST_STATIC_ASSERT(static_cast<int>(source_coordinate_type::static_dimensions) == static_cast<int>(coordinate_type::static_dimensions));
            
      typedef std::binary_function<source_coordinate_type, coordinate_type, yaF_double> parent_type;
      typedef typename parent_type::result_type result_type;

      result_type operator()(const source_coordinate_type& p1, const coordinate_type &p2) const throw()
      {
        yaF_double acc = 0;
        for(unsigned int i = 0; i < coordinate_type::static_dimensions; i++)
        {
          acc += std::abs(p1[i] - p2[i]);
        }
        return acc;
      }
    };




    /*!@brief Axis scaled euclidian distance between two points
     * 
     * This functor computes the euclidian distance between two points. The axis of the points are scaled. 
     * @note this is used to compute non isometric distances.
     * @pre the scaling matrix should be of the same size of the dimension of the points. 
     */
    template <class source_coordinate_type, class coordinate_type>
    struct s_non_isometric_l2_distance_op : std::binary_function<source_coordinate_type, coordinate_type, yaF_double>
    {
      BOOST_STATIC_ASSERT(static_cast<int>(source_coordinate_type::static_dimensions) == static_cast<int>(coordinate_type::static_dimensions));
            
      typedef yaF_double storage_type;

      s_non_isometric_l2_distance_op(const std::vector<yaF_double> &f)
      {
        YAYI_DEBUG_ASSERT(f.size() != coordinate_type::static_dimensions, "bad size for the factors");

        for(unsigned int i = 0; i < (unsigned int)coordinate_type::static_dimensions; i++)
        {
          d_factor[i] = f[i];
        }
      }
      
      s_non_isometric_l2_distance_op(const s_non_isometric_l2_distance_op& r)
      {
        for(unsigned int i = 0; i < (unsigned int)coordinate_type::static_dimensions; i++)
        {
          d_factor[i] = r.f[i];
        }        
      }

      storage_type operator()(const source_coordinate_type& p1, const coordinate_type &p2) const throw()
      {

        yaF_double acc = 0;
        for(int i = 0; i < coordinate_type::static_dimensions; i++)
        {
          yaF_double v = p1[i] - p2[i];
          v *= d_factor[i];
          v*= v;
          acc += v;
        }
        return sqrt(acc);
      }

    private:
      yaF_double d_factor[coordinate_type::static_dimensions];
    };


    /*!@brief Scaled and rotated euclidian distance between two points
     * 
     * This functor computes the euclidian distance between two points. Prior to the computation, the points are 
     * transformed through a matrix. 
     * @note this is used to compute non isometric and non axis aligned distances. The matrix does not need to be a 
     * rotation matrix (determinant 1).
     * @pre the matrix should be of the square size of the dimension of the points. 
     */
    template <class source_coordinate_type, class coordinate_type>
    struct s_generic_euclidian_norm_op : std::binary_function<source_coordinate_type, coordinate_type, yaF_double>
    {
      BOOST_STATIC_ASSERT(static_cast<int>(source_coordinate_type::static_dimensions) == static_cast<int>(coordinate_type::static_dimensions));
            
      typedef yaF_double storage_type;

      s_generic_euclidian_norm_op(const std::vector<yaF_double> &f)
      {
        DEBUG_ASSERT(f.size() == coordinate_type::static_dimensions*coordinate_type::static_dimensions, "bad size for the factors");
        for(unsigned int i = 0; i < (unsigned int)coordinate_type::static_dimensions*coordinate_type::static_dimensions; i++)
        {
          d_factor[i] = f[i];
        }
      }
      
      s_generic_euclidian_norm_op(const s_generic_euclidian_norm_op& r)
      {
        for(unsigned int i = 0; i < (unsigned int)coordinate_type::static_dimensions*coordinate_type::static_dimensions; i++)
        {
          d_factor[i] = r.d_factor[i];
        }        
      }

      storage_type operator()(const source_coordinate_type& p1, const coordinate_type &p2) const throw()
      {

        yaF_double acc = 0;
        const yaF_double *p_f = d_factor;
        for(int i = 0; i < coordinate_type::static_dimensions; i++)
        {
          yaF_double v = 0;
          for(int j = 0; j < coordinate_type::static_dimensions; j++, p_f++)
          {
            v += (p1[j] - p2[j]) * (*p_f);
          }
          v *= (p1[i] - p2[i]);
          acc += v;
        }
        return sqrt(acc);
      }

    private:
      yaF_double d_factor[coordinate_type::static_dimensions*coordinate_type::static_dimensions];
    };


    
  //! @} // distances_details_grp    
  }
}
 
#endif /* YAYI_DISTANCES_OP_T_HPP__ */

