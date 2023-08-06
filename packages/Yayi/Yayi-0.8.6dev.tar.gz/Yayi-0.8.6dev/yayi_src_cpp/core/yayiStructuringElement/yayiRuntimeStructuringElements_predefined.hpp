#ifndef YAYI_STRUCTURING_ELEMENT_PREDEFINED_HPP__
#define YAYI_STRUCTURING_ELEMENT_PREDEFINED_HPP__

/*!@file
 * This file defines some usual structuring elements
 *
 * @author Raffi Enficiaud
 */

#include <yayiCommon/common_coordinates.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_t.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>



namespace yayi { namespace se {
  /*!
   * @defgroup se_predefined_grp Common Predined Structuring Element
   * @ingroup se_grp
   * @{
   */

  /*!@brief Hexagonal alternating structuring element
   *
   * This SE changes its shape according to the line on which it is centered. The two shapes are ("x" represents a neighbor and "." an adjacent point not in the
   * neighborhood):
   *
   * . x x      x x . @n
   * x x x      x x x @n
   * . x x      x x . @n
   *
   * @remark This se "approximates" the unit euclidian ball
   */
  YSE_ extern const s_neighborlist_se_hexa_x< s_coordinate<2> > SEHex2D;



  /*!@brief Square structuring element (2D)
   * Square rigid structuring element (2D)
   *
   * x x x  @n
   * x x x  @n
   * x x x  @n
   *
   * @remark This se is the unit ball for \f$L_\infty\f$ distance on 2D
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<2> > SESquare2D;

  /*!@brief Cross structuring element (2D)
   * Cross rigid structuring element (2D)
   *
   * . x .   @n
   * x x x   @n
   * . x .   @n
   *
   * @remark This se is the unit ball for \f$L_1\f$ distance on 2D
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<2> > SECross2D;



  /*! Line structuring element / segment of unit size along X (1D)
   *
   * x x x
   *
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<1> > SESegmentX1D;

  /*! Line structuring element / segment of unit size along X (2D)
   *
   * x x x
   *
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<2> > SESegmentX2D;

  /*! Line structuring element / segment of unit size along Y (2D)
   *   x  @n
   *   x  @n
   *   x  @n
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<2> > SESegmentY2D;



  /*! Line structuring element / segment of unit size along X (3D)
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<3> > SESegmentX3D;

  /*! Line structuring element / segment of unit size along Y (3D)
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<3> > SESegmentY3D;

  /*! Line structuring element / segment of unit size along Z (3D)
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<3> > SESegmentZ3D;

  /*!@brief Square structuring element (3D)
   * Square rigid structuring element (3D), having a thickness of 3 and is a SESquare2D along z axis
   *
   * @remark This se is the unit ball for \f$L_\infty\f$ distance on 3D
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<3> > SESquare3D;

//! @} // se_predefined_grp
}}

#endif /* YAYI_STRUCTURING_ELEMENT_PREDEFINED_HPP__ */
