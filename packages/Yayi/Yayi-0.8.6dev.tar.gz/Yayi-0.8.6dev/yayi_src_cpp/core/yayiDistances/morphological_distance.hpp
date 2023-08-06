#ifndef YAYI_MORPHOLOGICAL_DISTANCES_HPP__
#define YAYI_MORPHOLOGICAL_DISTANCES_HPP__

/*!@file
 * This file defines the classical morphological distances. The implementation is based
 * on the simple queue propagation
 * @author Raffi Enficiaud
 */


#include <yayiDistances/yayiDistances.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace distances
  {
    /*!@defgroup morphologicaldistance_grp "Classical" morphological distances
     * @ingroup distances_grp
     * @{
     */


    /*!@brief Morphological distance on input image (from sets boundary).
     *
     * Also known as grid distance transform.
     * @author Raffi Enficiaud
     */
    YDist_ yaRC DistanceFromSetsBoundary(const IImage* input, const se::IStructuringElement* se, IImage* output_distance);


    /*!@brief Morphological geodesic distance on input image (from sets boundary).
     *
     * Roughly the same as @ref DistanceFromSetsBoundary, but the distance is computed in a geodesic manner inside the image mask.
     *
     * @author Raffi Enficiaud
     */
    YDist_ yaRC GeodesicDistanceFromSetsBoundary(const IImage* input, const IImage* mask, const se::IStructuringElement* se, IImage* output_distance);

    //! @} //morphologicaldistance_grp

  }

}

#endif /* YAYI_MORPHOLOGICAL_DISTANCES_HPP__ */
