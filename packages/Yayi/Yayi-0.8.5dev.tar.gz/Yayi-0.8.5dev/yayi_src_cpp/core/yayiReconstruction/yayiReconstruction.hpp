#ifndef YAYI_RECONSTRUCTION_MAIN_HPP__
#define YAYI_RECONSTRUCTION_MAIN_HPP__



#include <yayiCommon/common_config.hpp>


#ifdef YAYI_EXPORT_REC_
#define YRec_ MODULE_EXPORT
#else
#define YRec_ MODULE_IMPORT
#endif

 /*!@defgroup reconstruction_grp Morphological reconstruction algorithms
  * @brief Morphological reconstruction and related algorithms. 
  *
  * The reconstruction is a powerful and intensively used operator in Mathematical Morphology. The definition of the 
  * original reconstruction notion dates back to Lantuejoul & Maisonneuve in @cite lantuejoul_maisonneuve:1984. Reconstructions
  * may be seen as an extension of the elementary @b geodesic erosion/dilation (see @ref llm_details_geodesic_grp).
  *
  * We denote by @f$K^{(n)}@f$ the operation @f$K@f$ iterated @f$n@f$ times: 
  *  @f[K^{(n)} = K \circ K^{(n-1)}@f]
  * 
  * Given a dilation @f$\delta@f$, an initial set @f$X@f$ (or probe) and a restriction set @f$M@f$, the morphological opening by reconstruction of @f$M@f$ is defined as
  *  @f[\delta_{rec}^X(M)= \lim_{n\rightarrow +\infty} \left(\delta(X) \cap M\right)^{(n)} @f]
  *
  * It is indeed an opening since:
  * - it is increasing in @f$M@f$: @f[M \in M' \Rightarrow \delta_{rec}^X(M) \subset \delta_{rec}^X(M')@f]
  * - it is anti-extenive: @f[\delta_{rec}^X(M) \subset M @f]
  * - it is idempotent: @f[\delta_{rec}^X(\delta_{rec}^X(M)) = \delta_{rec}^X(M)@f]
  */


#endif /* YAYI_RECONSTRUCTION_MAIN_HPP__ */

