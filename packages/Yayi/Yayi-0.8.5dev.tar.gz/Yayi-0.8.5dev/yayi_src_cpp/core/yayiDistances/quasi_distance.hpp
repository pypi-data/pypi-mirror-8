#ifndef YAYI_QUASI_DISTANCES_HPP__
#define YAYI_QUASI_DISTANCES_HPP__

#include <yayiDistances/yayiDistances.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace distances
  {
    /*!@defgroup quasidistance_grp QuasiDistances (Residual Gray Level Morphology Operator)
     * @ingroup distances_grp
     *
     * Quasi-distances are an extension of the morphological distance to gray level images. Quasi-distances were defined
     * by Beucher @cite beucher:residues:2005.
     * The algorithm used for the quasi-distance computation is detailed in @cite enficiaud:qd:2010.
     * @{
     */

    /*!@brief Quasi distance on input image
     *
     * The implementation follows the one specified in the PhD of Raffi Enficiaud
     * @author Raffi Enficiaud
     */
    YDist_ yaRC quasi_distance(const IImage* input, const se::IStructuringElement* se, IImage* output_distance, IImage* output_residual);


    /*!@brief Weighted quasi distance on input image
     *
     * The weights are applied to the residue on each step. The algorithms stops when either no more weights are found or
     * idempotency is reached.
     * @author Raffi Enficiaud
     */
    YDist_ yaRC quasi_distance_weighted(const IImage* input, const se::IStructuringElement* se, const variant& v_weights, IImage* output_distance, IImage* output_residual);



    /*! Regularization of the result given by the quasi-distances residual algorithm
     *  @author Raffi Enficiaud
     *  @see quasi_distance
     */
    YDist_ yaRC DistancesRegularization(const IImage* input_distance, const se::IStructuringElement* se, IImage* output_distance);

  }
  //! @} //quasidistance_grp
}


#endif /* YAYI_QUASI_DISTANCES_HPP__ */
