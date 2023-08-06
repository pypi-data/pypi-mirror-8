#ifndef YAYI_HIGHLEVEL_MORPHOLOGY_MINIMAMAXIMA_T_HPP__
#define YAYI_HIGHLEVEL_MORPHOLOGY_MINIMAMAXIMA_T_HPP__

#include <yayiReconstruction/highlevel_minima_maxima.hpp>
#include <yayiPixelProcessing/include/image_arithmetics_t.hpp>
#include <yayiPixelProcessing/include/image_compare_T.hpp>
#include <yayiReconstruction/include/morphological_reconstruction_t.hpp>
#include <yayiCommon/common_errors.hpp>
#include <yayiPixelProcessing/include/image_copy_T.hpp>


namespace yayi { namespace hlmm {

  /*!@defgroup high_level_morphology_details_group Simple compound morphological operators view as High level operators Implementation Details
   * @ingroup high_level_morphology_group
   * @{
   */

  /*!@brief h_minima template function
   *
   * @author Thomas Retornaz
   */
  template <class image_in, class se_t, class image_out>
  yaRC image_h_minima_t(const image_in& imin, const se_t& se,typename image_in::pixel_type const& v, image_out& imout)
  {
    image_in imtemp;
    yaRC res = imtemp.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in set_same" << res);
      return res;
    }

    res = yayi::add_images_constant_upper_bound_t(imin, v, boost::numeric::bounds<typename image_in::pixel_type>::highest(), imtemp);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in add_images_constant_upper_bound_t"<< res);
      return res;
    }
    return yayi::reconstructions::closing_by_reconstruction_t(imtemp,imin,se,imout);
  }

  /*!@brief h_maxima template function
   *
   * @author Thomas Retornaz
   */
  template <class image_in, class se_t, class image_out>
  yaRC image_h_maxima_t(const image_in& imin, const se_t& se,typename image_in::pixel_type const& v, image_out& imout)
  {
    image_in imtemp;
    yaRC res = imtemp.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in set_same"<< res);
      return res;
    }

    res = yayi::subtract_images_constant_lower_bound_t(imin, v, boost::numeric::bounds<typename image_in::pixel_type>::lowest(), imtemp);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in subtract_images_constant_lower_bound_t"<< res);
      return res;
    }
    return yayi::reconstructions::opening_by_reconstruction_t(imtemp,imin,se,imout);
  }

  /*!@brief H-concave template function
   * @code
   * ABS(the h-minima transformation - imin).
   * @endcode
   * @author Thomas Retornaz
   * @see image_h_minima_t, image_h_convex_t
   */
  template <class image_in, class se_t, class image_out>
  yaRC image_h_concave_t(const image_in& imin, const se_t& se,typename image_in::pixel_type const& v, image_out& imout)
  {
    image_in imHminima;
    yaRC res = imHminima.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in set_same"<< res);
      return res;
    }


    res = image_h_minima_t(imin,se,v,imHminima);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in image_h_minima_t"<< res);
      return res;
    }
    return yayi::abssubtract_images_t(imHminima,imin,imout);

  }


  /*!@brief H-convex template implementation
   * @code
   * ABS(the h-maxima transformation - imin).
   * @endcode
   * @author Thomas Retornaz
   * @see image_h_maxima_t	,image_h_concave_t
   */
  template <class image_in, class se_t, class image_out>
  yaRC image_h_convex_t(const image_in& imin, const se_t& se,typename image_in::pixel_type const& v, image_out& imout)
  {
    image_in imHmaxima;
    yaRC res = imHmaxima.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in set_same"<< res);
      return res;
    }
    res = image_h_maxima_t(imin, se, v, imHmaxima);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in image_h_maxima_t"<< res);
      return res;
    }
    return yayi::abssubtract_images_t(imHmaxima, imin, imout);

  }


  /*!@brief Pseudo-dynamic opening template implementation
   * @code
   * ABS(the h-maxima transformation - imin).
   * @endcode
   *
   * @author Thomas Retornaz
   * @see image_h_maxima_t, image_h_concave_t
   */
  template <class image_in, class se_t, class image_out>
  yaRC image_h_dynamic_opening_t(const image_in& imin, const se_t& se,typename image_in::pixel_type const& v, image_out& imout)
  {
    image_in imHmaxima;
    yaRC res = imHmaxima.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in set_same"<< res);
      return res;
    }

    image_in imMask;
    res = imMask.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in set_same"<< res);
      return res;
    }
    image_in imtemp;
    res = imtemp.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in set_same"<< res);
      return res;
    }

    typedef typename image_in::pixel_type image_in_pixel_type_t;

    res = yayi::subtract_images_constant_lower_bound_t(imin, v, boost::numeric::bounds<image_in_pixel_type_t>::lowest(), imtemp);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in subtract_images_constant_lower_bound_t"<< res);
      return res;
    }

    res = yayi::reconstructions::opening_by_reconstruction_t(imtemp, imin, se, imHmaxima);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in opening_by_reconstruction_t"<< res);
      return res;
    }

    // Create marker : look for remaining maxima
    res = image_compare_ii_stub(imHmaxima, e_co_equal, imtemp, imin, boost::numeric::bounds<image_in_pixel_type_t>::lowest(), imMask);//TR lowest or smallest for signed type ?
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in image_compare_ii_stub"<< res);
      return res;
    }

    // remove test with lowest
    res = image_compare_si_stub(imHmaxima, e_co_different, boost::numeric::bounds<image_in_pixel_type_t>::lowest(), imMask, boost::numeric::bounds<image_in_pixel_type_t>::lowest(), imtemp);//TR lowest or smallest for signed type ?
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in image_compare_si_stub"<< res);
      return res;
    }
    return yayi::reconstructions::opening_by_reconstruction_t(imtemp, imin, se, imout);

  }


  /*!@brief Pseudo-dynamic opening template implementation
   * @author Raffi Enficiaud
   * @see image_h_minima_t, image_h_convex_t
   */
  template <class image_in, class se_t, class image_out>
  yaRC image_h_dynamic_closing_t(const image_in& imin, const se_t& se,typename image_in::pixel_type const& v, image_out& imout)
  {
    image_in imHminima;
    yaRC res = imHminima.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in set_same"<< res);
      return res;
    }
    image_in imMask;
    res = imMask.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in set_same"<< res);
      return res;
    }

    image_in imtemp;
    res = imtemp.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in set_same"<< res);
      return res;
    }

    typedef typename image_in::pixel_type image_in_pixel_type_t;

    res = yayi::add_images_constant_upper_bound_t(imin, v, boost::numeric::bounds<image_in_pixel_type_t>::highest(), imtemp);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in add_images_constant_upper_bound_t"<< res);
      return res;
    }

    res=yayi::reconstructions::closing_by_reconstruction_t(imtemp, imin, se, imHminima);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in closing_by_reconstruction_t"<< res);
      return res;
    }

    // Create marker : look for remaining minima
    res=image_compare_ii_stub(imHminima, e_co_equal, imtemp, imin, boost::numeric::bounds<image_in_pixel_type_t>::highest(), imMask);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in image_compare_ii_stub"<< res);
      return res;
    }

    // remove test with highest
    res=image_compare_si_stub(imHminima, e_co_different, boost::numeric::bounds<image_in_pixel_type_t>::highest(),imMask, boost::numeric::bounds<image_in_pixel_type_t>::highest(), imtemp);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error in image_compare_si_stub"<< res);
      return res;
    }
    return yayi::reconstructions::closing_by_reconstruction_t(imtemp, imin, se, imout);

  }
  //! @}
      
}}

#endif /* YAYI_HIGHLEVEL_MORPHOLOGY_MINIMAMAXIMA_T_HPP__ */
