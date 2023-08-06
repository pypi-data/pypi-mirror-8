#ifndef YAYI_IMAGE_CORE_HPP__
#define YAYI_IMAGE_CORE_HPP__

/*! @file
 *  @brief Global definition for the image core library
 *  @author Raffi Enficiaud
 */


#include <yayiCommon/common_config.hpp>
#include <yayiCommon/common_types.hpp>
#include <yayiCommon/common_pixels.hpp>
#include <yayiCommon/include/common_object.hpp>
#include <yayiCommon/common_coordinates.hpp>
#include <yayiCommon/common_variant.hpp>
#include <yayiCommon/common_colorspace.hpp>

#include <memory>


#ifdef YAYI_EXPORT_CORE_
#define YCor_ MODULE_EXPORT
#else
#define YCor_ MODULE_IMPORT
#endif



namespace yayi
{
  /*!@defgroup image_core_grp Image Core
   * @brief Image structures, iterators and low level utilities.
   *
   * This module defines the main structures for image and their accesses, as well as the "pixel processing" functor (application of
   * a functor to all or subset of the pixels of the image.)
   *
   * IImage is the main image interface. This class provides a generic access to its pixels, in the sense that
   * the pixels are weakly typed (variant) and the coordinate system is multidimensional. Any instance of IImage is (currently) an implementation
   * of the template Image class. The static method IImage::Create is the IImage factory and should be used to create any image of any type.
   *
   * @author Raffi Enficiaud
   * @{
   */

  class IImage;
  class IIterator;
  class IConstIterator;




  /*!@brief A simple interface to special pixels returned by the interface layer of images.
   *
   * This object is intended to be a reference to a particular pixel of an image, at the interface level.
   * Since the pixels are encoded in variants at the interface level, a direct use of the pixel value cannot be used.
   * 
   * The class is not copyable (referenced pixel cannot be changed) but can be used in an lvalue expression. 
   * @warning Currently accessing the proxy after deleting/freeing the image triggers a violation access (no lifetime 
   * dependency handling).
   * @author Raffi Enficiaud
   */
  struct YCor_ IVariantProxy
  {
    //! Type of the pixels
    typedef variant pixel_value_type;
    typedef IVariantProxy this_type;
  private:
    IVariantProxy& operator=(const IVariantProxy&);

  public:
    virtual ~IVariantProxy() {}
    virtual pixel_value_type const& operator=(const pixel_value_type& v)
    {
      setPixel(v);
      return v;
    }

    pixel_value_type operator*() const
    {
      return getPixel();
    }

    //!@name Pixel comparison operators
    //!@{

    //!@brief True if the given pixel value is equal to the one of the current instance.
    //! Being at the interface level, the two values may be encoded in different types in the
    //! underlying variants. The call though performs the conversion to the referenced image
    //! pixel type prior to the comparison.
    virtual bool operator==(const pixel_value_type&v) const
    {
      return isEqual(v);
    }
    virtual bool operator==(const this_type&v) const
    {
      return isEqual(v);
    }

    virtual bool operator!=(const pixel_value_type&v) const
    {
      return isDifferent(v);
    }
    virtual bool operator!=(const this_type&v) const
    {
      return isDifferent(v);
    }
    //!@}

    virtual pixel_value_type getPixel () const = 0;
    virtual yaRC    setPixel          (const pixel_value_type &) = 0;
    virtual bool    isEqual           (const pixel_value_type &) const = 0;
    virtual bool    isEqual           (const this_type &) const = 0;
    virtual bool    isDifferent       (const pixel_value_type &) const = 0;
    virtual bool    isDifferent       (const this_type &) const = 0;
  };



  /*!
   * @brief Image interface
   *
   * Main image interface
   * @author Raffi Enficiaud
   */
  class IImage : public IObject
  {
  public:
    //! Coordinate type of the interface Image
    typedef s_coordinate<0>                 coordinate_type;

    //! Offset type
    typedef offset                          offset_type;

    //! Pixel valye type of the interface image
    typedef variant                         pixel_value_type;

    //! Pixel reference type of the interface image
    typedef std::auto_ptr<IVariantProxy>    pixel_reference_type;

    //! Iterator type
    typedef IIterator*                       iterator;

    //! Const iterator type
    typedef IConstIterator*                  const_iterator;

  public:
    virtual ~IImage(){}

    /*!@brief Images factory
     *
     * Creates a new instance of image with the specified type. The returned image implements the IImage interface.
     *
     * @param pixel_type the pixel type of the image to create.
     * @param dimension  the dimension spanned by the coordinate space of the image.
     * @snippet yayiImageCoreTests/image_creation.cpp test_interface_creation
     */
    YCor_ static IImage*  Create(type pixel_type, yaUINT8 dimension);

    /*!@brief Allocates the image.
     *
     * The size should have been previously specified.
     *
     * @return yaRC_ok on success, an error code otherwise.
     * @pre The image is not allocated (IsAllocated() returns false)
     * @post If the call succeeded, IsAllocated() returns true and the pixel buffer is allocated.
     * @see IsAllocated(), FreeImage()
     */
    virtual yaRC    AllocateImage()	= 0;

    //! @brief Returns the state of allocation of the pixel buffer
    virtual bool    IsAllocated()	const = 0;


    /*!@brief Frees the content of the image
     *
     * @pre  IsAllocated returns true.
     * @post IsAllocated returns false.
     */
    virtual	yaRC    FreeImage()			= 0;


    /*!@name Size management
     * @{
     */

    //! Returns the actual size of the image
    virtual coordinate_type   GetSize() const	= 0;

    //! @brief Changes the size of the image
    //! It is not possible to change the size when the image is allocated
    virtual yaRC              SetSize(const coordinate_type&)	= 0;

    //! Returns the dimension of the image
    virtual unsigned int      GetDimension() const = 0;

    //! @}

    //! @brief Returns the color space assiciated to the image.
    //! Defaults to undertermined
    virtual yaColorSpace GetColorSpace() const = 0;

    //! Sets the color space associated to the image
    virtual yaRC         SetColorSpace(yaColorSpace const &) = 0;

    /*!@name Iterators
     * @{
     */

    //! Returns a block-iterator to the beginning of the image (the pixel's map)
    virtual iterator begin() throw() = 0;

    //! Returns a block-iterator to the end of the image (the pixel's map)
    virtual iterator end() throw() = 0;

    //! Returns a const block-iterator to the beginning of the image (the pixel's map)
    virtual const_iterator begin() const throw() = 0;

    //! Returns a const block-iterator to the end of the image (the pixel's map)
    virtual const_iterator end() const throw() = 0;
    //! @} //iterators

    /*!@name Pixel access methods
     * @{
     */

    //! Returns the value of the pixel at the specified coordinate
    virtual pixel_value_type      pixel(const coordinate_type& ) const  = 0;

    /*! Returns a reference to the pixel at the specified coordinate
     *
     * @warning Currently no reference is kept on the containing image, which means that accessing the pixel
     * after image deletion/pixel map free may result in an access violation.
     */
    virtual pixel_reference_type  pixel(const coordinate_type& )        = 0;

    //! @} //pixel



  };

  /*!@defgroup iterators_grp Iterators
   * @ingroup image_core_grp
   * @brief Iterators on images.
   *
   * Iterators on images allow to access the content of images without actually knowing the internal storage of pixels, nor 
   * its coordinate space or its geometry, or the subset of pixels of the image spanned by the iteration. It is hence 
   * a bit more than the usual iterator concept (abstraction of the storage).
   *
   * There are currently two types of iterators:
   * - @ref iterators_block_grp "block iterators": these are the classical iterators that span all the pixels of the image in a specific "video" order (left to right,
   *   top to bottom, front to back, etc)
   * - @ref iterators_windows_grp "windowed iterators": same as block iterators but restricted to an hyperrectangle on the image. 
   *
   * Currently, only block-iterators are exposed at the interface level. 
   * @{
   */

  /*!@brief Iterator interface with const accesses.
   *
   * Main image iterator interface with const access to the pixels of the image
   *
   * @todo implement the concepts of random access iterators.
   * @author Raffi Enficiaud
   */
  class IConstIterator : public IObject
  {
  public:
    //! Type of the image on which the iteration is performed
    typedef IImage                            image_type;

    //! Coordinate type of the iterator
    typedef image_type::coordinate_type       coordinate_type;

    //! Pixel value type returned by the iterator
    typedef image_type::pixel_value_type      pixel_type;

    //! This type
    typedef IConstIterator                    this_type;

  public:
    //! Returns true if the iterators refers to the same pixel
    virtual bool is_equal(const this_type* const& ) const = 0;

    //! Returns true if the iterators do not refer to the same pixel
    virtual bool is_different(const this_type* const& ) const = 0;

    //! Returns the actual position of the iterator
    virtual coordinate_type GetPosition() const throw() = 0;

    virtual offset          GetOffset() const throw() = 0;

    //! Set the actual position of the iterator
    virtual yaRC            SetPosition(const coordinate_type&) throw() = 0;

    //! Returns the value of the pixel
    virtual pixel_type      getPixel() const  = 0;

    //! Iterates to the next element
    virtual yaRC            next()            = 0;

    //! Iterates to the previous element
    virtual yaRC            previous()        = 0;

    //! Clones the current iterator
    virtual this_type*      clone() const     = 0;


  };



  /*!@brief Iterator interface with non const accesses
   *
   * Adds the pixels writing capabilities to the IConstIterator
   * @author Raffi Enficiaud
   */
  class IIterator
  {
  public:
    typedef IImage                            image_type;
    typedef image_type::pixel_value_type      pixel_type;
    typedef IIterator                         this_type;

    virtual ~IIterator(){}
    virtual yaRC      setPixel(const pixel_type&) = 0;
  };

  //!@} iterators_grp

  //!@} image_core_grp


} // namespace yayi

#endif

