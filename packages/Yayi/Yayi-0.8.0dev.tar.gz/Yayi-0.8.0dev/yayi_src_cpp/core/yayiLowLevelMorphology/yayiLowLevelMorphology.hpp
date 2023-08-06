#ifndef YAYI_LOWLEVEL_MORPHOLOGY_MAIN_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_MAIN_HPP__

#include <yayiCommon/common_config.hpp>
#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiStructuringElement/yayiStructuringElement.hpp>

#ifdef YAYI_EXPORT_LLMM_
#define YLLMM_ MODULE_EXPORT
#else
#define YLLMM_ MODULE_IMPORT
#endif


/*@namespace llmm
 *@brief Defines basic morphological operations.
 *
 *
 *@author Raffi Enficiaud
 */
namespace yayi
{
  namespace llmm
  {
    /*!@defgroup llm_grp Low level morphological functions.
     * @brief Low level and basic morphological functions.
     *
     * This group of function defines the most commonly used morphological operations on images. These operations
     * tend to be the simplest also, in that they involve only a local information on the image. They rely on
     * a structuring element that encodes the topology/neighborhood of the input image, and which is used to perform the computations.
     * Several functions are defined in this group:
     * - Erosion and dilations
     * - Openings and closings
     * - Morphological gradients
     * - Hit or miss operations
     * - Geodesic erosions and dilations
     *
     * For each of the interface function, the template function containing the implementation is defined and follows the naming conventions.
     * @todo Alternate sequential filters.
     * @todo Morphology along line structuring elements.
     */

    /*!@defgroup llm_details_grp Low level morphological template functions.
     * @ingroup llm_grp
     * @brief Template layer and implementation details.
     *
     *
     */
  }
}

#endif /* YAYI_LOWLEVEL_MORPHOLOGY_MAIN_HPP__ */
