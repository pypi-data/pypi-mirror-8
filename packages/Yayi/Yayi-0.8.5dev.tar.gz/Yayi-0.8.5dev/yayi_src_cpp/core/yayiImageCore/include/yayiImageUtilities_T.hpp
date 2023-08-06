#ifndef YAYI_IMAGE_UTILITIES_HPP__
#define YAYI_IMAGE_UTILITIES_HPP__


/*!@file
 * Utility file for images. Includes the utilities for coordinates.
 *
 * @author Raffi Enficiaud
 */

#include <yayiCommon/common_types.hpp>
#include <yayiCommon/common_errors.hpp>
#include <yayiCommon/common_coordinates.hpp>
#include <yayiCommon/common_hyperrectangle.hpp>
#include <yayiCommon/common_pixels_T.hpp>
#include <yayiCommon/common_coordinates_operations_t.hpp>

namespace yayi
{

  /*!@defgroup image_utilities_core Image core Utilities
   * @ingroup  image_core_grp
   * @{
   */


  /*!@brief Returns the total number of points in the specified coordinate
   *
   * @author Raffi Enficiaud
   */
  template <class coordinate_t>
  offset total_number_of_points(const coordinate_t& coord)
  {
    offset ret = 1;
    for(int i = coord.dimension() - 1; i >= 0; i--)
    {
      ret *= coord[i];
    }
    return ret;
  }

  /*!@brief Returns the total number of points in the specified hyperrectangle
   * @todo move to the common functions.
   * @author Raffi Enficiaud
   */
  template <int dim>
  offset total_number_of_points(s_hyper_rectangle<dim> const& r)
  {
    return total_number_of_points(r.Size());
  }

  /*!@brief Returns the last non void dimension of the size (encoded as a coordinate).
   *
   * Returns -1 if the coordinate has no size in any dimension
   * @author Raffi Enficiaud
   */
  template <class coordinate>
  int get_last_dimension(const coordinate& coord)
  {
    for(int i = coord.dimension() - 1; i >= 0; i--)
    {
      if(coord[i] != 0) return i + 1;
    }
    return -1;
  }



  /*!@brief Transforms a point in a regular grid to an offset
   *
   * @param[in]		size	the regular grid size
   * @param[in]		point	the position of the point of interest
   * @return the offset of the point
   *
   * @author Raffi Enficiaud
   * @anchor from_coordinate_to_offset
   */
  template <class coordinate>
  offset from_coordinate_to_offset(const coordinate &size, const coordinate& point)
  {
    offset ret = 0;
    for(int i = point.dimension() - 1; i > 0; i--)
      {
        ret += point[i];
        ret *= size[i-1];
      }
    ret += point[0];
    return ret;
  }

  /*!@brief Returns the offset (in bytes) of the current point
   * Please refer @ref from_coordinate_to_offset for more details
   * @author Raffi Enficiaud
   */
  template <class coordinate, class T>
  offset from_coordinate_to_byte_offset(const coordinate &size, const coordinate& point)
  {
    offset ret = 0;
    for(int i = point.dimension() - 1; i > 0; i--)
      {
        ret += point[i];
        ret *= size[i-1];
      }
    ret += point[0];
    return ret * sizeof(T);
  }



  /*!@brief Returns the coordinate of the specified offset
   * @author Raffi Enficiaud
   */
  template <class coordinate>
  coordinate from_offset_to_coordinate(const coordinate &size, offset off)
  {
    coordinate ret;
    const int j = size.dimension();
    int i = 0;
    DEBUG_ASSERT(off >= 0, "Negative offset are unsupported");
    for(; i < j && off != 0; i++)
    {
      const typename coordinate::scalar_coordinate_type ith_index = size[i];
      DEBUG_ASSERT(ith_index > 0, "The size is null or negative ! component " + int_to_string(i) + ", size = " + int_to_string(ith_index));
      ret[i] = off % ith_index;
      off   /= ith_index;
    }
    for(; i < j; i++)
    {
      ret[i] = 0;
    }
    return ret;
  }


  //!Specializing of from_offset_to_coordinate for interface coordinate type.
  inline s_coordinate<0> from_offset_to_coordinate(const s_coordinate<0> &size, offset off)
  {
    typedef s_coordinate<0> coordinate;
    coordinate ret;
    const int j = size.dimension();
    ret.set_dimension(j);
    int i = 0;
    DEBUG_ASSERT(off >= 0, "Negative offset are unsupported");
    for(; i < j && off != 0; i++)
    {
      const coordinate::scalar_coordinate_type ith_index = size[i];
      DEBUG_ASSERT(ith_index > 0, "The size is null or negative ! component " + int_to_string(i) + ", size = " + int_to_string(ith_index));
      ret[i] = off % ith_index;
      off   /= ith_index;
    }
    for(; i < j; i++)
    {
      ret[i] = 0;
    }
    return ret;
  }

  //! Same as from_offset_to_coordinate, but for a set of coordinates.
  template <class coordinate>
  std::vector<coordinate> from_offsets_to_coordinate(const coordinate &size, std::vector<offset> const &v_off)
  {
    std::vector<coordinate> out;
    for(std::vector<offset>::const_iterator it(v_off.begin()), ite(v_off.end()); it != ite; ++it)
      out.push_back(from_offset_to_coordinate(size, *it));
    return out;
  }

  template <class coordinate, class it_t>
  std::vector<coordinate> from_offsets_to_coordinate(const coordinate &size, it_t it, it_t ite)
  {
    std::vector<coordinate> out;
    for(; it != ite; ++it)
      out.push_back(from_offset_to_coordinate(size, *it));
    return out;
  }



  /*!@brief Returns the coordinate of the specified offset (pointer difference)
   * @author Raffi Enficiaud
   */
  template <class coordinate, class T>
  coordinate from_byte_offset_to_coordinate(const coordinate &size, const offset& byte_offset)
  {
    return from_offset_to_coordinate(size, static_cast<offset>( byte_offset / sizeof(T) ) );
  }


  namespace {
    /*!Utility function for testing images' dimension
     * @author Raffi Enficiaud */
    template <class coordinate1, class coordinate2>
    struct s_are_same_geometry                          { template <class image1, class image2> bool operator()(const image1&,     const image2&) const throw()    {return false;}};
    template <class coordinate>
    struct s_are_same_geometry <coordinate, coordinate> { template <class image1, class image2> bool operator()(const image1& im1,  const image2& im2) const throw()  {return im1.Size() == im2.Size();}};
  }


  /*!@brief Returns true if the images are of the same geometry, false otherwise
   *
   * @author Raffi Enficiaud
   */
  template <class image1, class image2>
  bool are_same_geometry(const image1& im1, const image2& im2)
  {
    typedef s_are_same_geometry<typename image1::coordinate_type, typename image2::coordinate_type> op_t;
    op_t op;// = op_t();
    return op(im1, im2);
  }

  //! Returns true if the images are of the same type
  template <class image1, class image2>
  bool are_images_same_type(const image1&, const image2&)
  {
    return false;
  }

  template <class image>
  bool are_images_same_type(const image&, const image&)
  {
    return true;
  }


  //! Returns true if the images are the same, false otherwise
  template <class image1, class image2>
  bool are_images_same(const image1& im1, const image2& im2)
  {
    return false;
  }

  template <class image>
  bool are_images_same(const image& im1, const image& im2)
  {
    return im1 == im2;
  }

  //!@} //defgroup image_utilities_core
}



#endif /* YAYI_IMAGE_UTILITIES_HPP__ */


