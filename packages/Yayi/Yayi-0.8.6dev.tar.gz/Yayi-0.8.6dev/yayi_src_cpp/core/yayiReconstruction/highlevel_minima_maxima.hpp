#ifndef YAYI_HIGHLEVEL_MORPHOLOGY_MINIMAMAXIMA_HPP__
#define YAYI_HIGHLEVEL_MORPHOLOGY_MINIMAMAXIMA_HPP__


/*!@file
 * This file defines opening and closing/closure functions
 * @author Thomas Retornaz
 */

#include <yayiReconstruction/yayiReconstruction.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>




namespace yayi 
{ 
  namespace hlmm 
  {
    using namespace yayi::se;

    /*!@defgroup high_level_morphology_group Compound morphological operators
     * @ingroup reconstruction_grp
     *
     * These functions are built on the low level and geodesic morphological operators to provide high level filters.
     * @{
     */

    /*!@brief The H-minima transform
     *
     * The h-minima transformation suppresses all minima whose depth is greater than a given threshold c.
     * @author Thomas Retornaz
     */
    YRec_ yaRC image_h_minima(const IImage* imin, const IStructuringElement* se, variant c, IImage* imout);

    /*!
     * @brief TopHat Black with contrast criteria
     * @code
     * ABS(the h-minima transformation - imin).
     * @endcode
     *
     * @author Thomas Retornaz
     */
    YRec_ yaRC image_h_concave(const IImage* imin, const IStructuringElement* se,variant c, IImage* imout);

    /*!@brief The h-maxima transformation suppresses all maxima whose depth is lower than a given level threshold c.
     * @author Thomas Retornaz
     */
    YRec_ yaRC image_h_maxima(const IImage* imin, const IStructuringElement* se,variant c, IImage* imout);

    /*!@brief TopHat White with contrast criteria
     * @code
     * ABS(the h-maxima transformation - imin).
     * @endcode
     *
     * @author Thomas Retornaz
     */
    YRec_ yaRC image_h_convex(const IImage* imin, const IStructuringElement* se,variant c, IImage* imout);

    /*!@brief Pseudo dynamic opening
     *
     * The pseudo-dynamic opening transform suppresses all maxima whose depth is under a given threshold level c
     * similar to H-maxima transformation but the remaining maxima don't loose their dynamic value.
     * The transformation is idempotent and anti-extensive, but not increasing (hence this is not an algebraic opening).
     * @author Thomas Retornaz
     */
    YRec_ yaRC image_pseudo_dynamic_opening(const IImage* imin, const IStructuringElement* se,variant c, IImage* imout);


    /*!@brief Pseudo dynamic closing
     *
     * The pseudo-dynamic closing transform suppresses all minima whose depth is below than a given level threshold (c)
     * similar to H-minima transform but the remaining minima don't loose their dynamic value.
     * The transformation is idempotent and anti-extensive, but not increasing (hence this is not an
     * algebraic closing).
     *
     * @author Thomas Retornaz
     */
    YRec_ yaRC image_pseudo_dynamic_closing(const IImage* imin, const IStructuringElement* se,variant c, IImage* imout);

    //! @}

  }
}


#endif /* YAYI_HIGHLEVEL_MORPHOLOGY_MINIMAMAXIMA_HPP__ */
