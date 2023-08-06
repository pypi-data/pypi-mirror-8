#ifndef YAYI_MEASUREMENTS_T_HPP__
#define YAYI_MEASUREMENTS_T_HPP__

#include <vector>
#include <map>
#include <functional>


namespace yayi
{
  namespace measurements
  {
    /*!@defgroup measurement_functor_concepts Measurement function objects
     * @ingroup yayiconcepts
     * @{
     * @par Description
     * A measurement function object is used to compute a measurement on an image. The computation is made in two steps: the accumulation and the
     * computation of the result.
     *
     * @par Notations
     * Let @c F be the type of the function object, and @c f an instance.
     *
     * @par Requirements
     * A measurement function objects should meet the following requirements:
     * - @c f function object is callable, and the type given as parameter is the type on which the measurement is being made. Nothing is
     *   returned (@c void).
     * - the @c f object implements a function @c result with no parameter. The returned type is given by @c F::result_type.
     * - the @c f object implements a function @c clear_result, which initializes the state of @c f.
     * @}
     */



    /*!@defgroup meas_helper_grp Measurements helper functions
     * @ingroup meas_grp
     * @{
     */

    /*!@brief Adaptor for computing measurements on regions.
     *
     * This binary functor associates a measurement to each region of the image. The measurement is performed on the first image, while the
     * region (index) is given by a second image. The function object hence implements the @ref binary_pixel_processing_functor_concepts concept.
     * The update of the measurements is performed as the operator() is called, respectively with the pixel value to accumulate in the 
     * measurement and a region index. 
     * As other measurements, the accumulation is performed during this call.
     * The final value is computed during the call to the @b result member function. The functor object hence implements the @ref measurement_functor_concepts
     * concept.
     *
     * @tparam image_pixel_t the pixel type of the image on which the measurement will be performed.
     * @tparam region_index_t the index type of the regions. 
     * @tparam op_region_t the measurement to perform on each region.
     *
     * @note region_index_t should be <a href="http://www.sgi.com/tech/stl/EqualityComparable.html">equality comparable</a> and 
     * <a href="http://www.sgi.com/tech/stl/LessThanComparable.html">LessThan comparable</a> (requirement of @c std::map).
     * @note op_region_t should implement the @ref measurement_functor_concepts concept.
     * @author Raffi Enficiaud.
     
     * @concept{binary_pixel_processing_functor_concepts}
     * @concept{measurement_functor_concepts}
     */
    template <class image_pixel_t, class region_index_t, class op_region_t>
    struct s_measurement_on_regions: public std::binary_function<image_pixel_t, region_index_t, void>
    {
      //!@internal
      //! The type used to store the intermediate computations.
      typedef std::map<region_index_t, op_region_t> map_meas_t;
      map_meas_t map_;

      //! The associative map type containing the measurements indexed by the region index.
      typedef std::map<region_index_t, typename op_region_t::result_type> result_type;

      s_measurement_on_regions() : map_() {}

      //! Updates the measurement of region @b r with a new value p.
      void operator()(const image_pixel_t& p, const region_index_t& r) throw()
      {
        map_[r](p);
      }

      //! Computes the final results and returns the map of measurements.
      result_type result() const
      {
        result_type out;
        for(typename map_meas_t::const_iterator it(map_.begin()), ite(map_.end());
            it != ite;
            ++it)
        {
          out[it->first] = it->second.result();
        }
        return out;
      }

      //! Clears the results.
      void clear_result() throw()
      {
        map_.clear();
      }

    };


    /*!@brief Performs a measurement on a unique region of an image. 
     *
     * The region is given by a binary predicate over the pixel values of the mask image.
     * @note op_region_t should implement the @ref measurement_functor_concepts concept.
     * 
     * @concept{measurement_functor_concepts}
     */
    template <
      class image_pixel_t, 
      class mask_t, 
      class op_region_t,
      class binary_predicate_t = std::equal_to<mask_t> 
    >
    struct s_measurement_on_mask: public std::binary_function<image_pixel_t, mask_t, void>
    {
      typedef typename op_region_t::result_type result_type;
      op_region_t op_;
      const mask_t value_;
      const binary_predicate_t predicate;
      s_measurement_on_mask(binary_predicate_t const& predicate_ = binary_predicate_t()) 
        : op_(), value_(), predicate(predicate_)
      {}
      
      s_measurement_on_mask(const mask_t & value, binary_predicate_t const& predicate_ = binary_predicate_t()) 
        : op_(), value_(value), predicate(predicate_)
      {}
      
      void operator()(const image_pixel_t& p, const mask_t& r) throw()
      {
        if(predicate(r, value_))
          op_(p);
      }
      result_type result() const
      {
        return op_.result();
      }

      //! Clears the results.
      void clear_result() throw()
      {
        op_.clear();
      }

    };

    //! @} //meas_details_grp

  }
}



#endif /* YAYI_MEASUREMENTS_T_HPP__ */
