#ifndef YAYI_COMMON_CONSTANTS__HPP__
#define YAYI_COMMON_CONSTANTS__HPP__

#include <boost/math/constants/constants.hpp>


/*!@file
 * Constants used in the program.
 */

/*!
 * @defgroup common_constant_grp Constant
 * @brief Some useful constant values.
 * @ingroup general_grp
 * @{
 */

//! The magic \f$\pi\f$ number
#define yaPI      3.141592653589793238462643383279502884
//! \f$2\pi\f$
#define ya2PI     (2*yaPI)
//! \f$\pi/2\f$
#define yaPI_d2   (yaPI/2)
//! \f$\pi/3\f$
#define yaPI_d3   (yaPI/3)
//! \f$2\pi/3\f$
#define ya2PI_d3  (2*yaPI/3)

//! \f$\sqrt{3}/2\f$
#define yaSqrt3_d2 0.866025403784439

//! \f$2/\sqrt{3}\f$
#define ya2_dSqrt3 1.154700538379252
//! @} // common_constant_grp


namespace yayi
{
 /*!
  * @addtogroup common_constant_grp 
  * @{
  */

  //! Planck Constant for blackbody radiator computations
  yaF_double const PlanckConstant = 6.62606896E-34;

  //! Boltzmann constant, for the blackbody radiator computation
  yaF_double const BoltzmannConstant = 1.3806504E-23;

  //! Speed of light, for the blackbody radiator computation
  yaF_double const SpeedOfLight = 299792458;

  //! @} // addtogroup common_constant_grp
}



#endif // YAYI_COMMON_CONSTANTS__HPP__
