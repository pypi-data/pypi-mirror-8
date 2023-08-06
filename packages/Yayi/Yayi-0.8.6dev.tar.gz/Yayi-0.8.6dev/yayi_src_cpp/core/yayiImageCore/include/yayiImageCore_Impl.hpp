#ifndef YAYI_IMAGE_CORE_IMPL_HPP__
#define YAYI_IMAGE_CORE_IMPL_HPP__

/*@file
 * Main Image structure template implementation.
 *
 */


#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiImageCore/include/yayiImageIterator.hpp>
#include <yayiImageCore/include/yayiImageAllocators_T.hpp>
#include <yayiImageCore/include/yayiImageUtilities_T.hpp>
#include <yayiCommon/common_errors.hpp>

#include <yayiCommon/common_pixels.hpp>
#include <yayiCommon/common_pixels_T.hpp>

#include <boost/call_traits.hpp>


namespace yayi
{
  /*!@defgroup image_details_core_grp Image template structure
   * @ingroup image_core_grp
   * @brief Template image structure and associated iterators. 
   * @{
   */

  template <class pixel_type_t, class coordinate_type_t, class allocator_type> class Image;
  template <class pixel_type_t, class coordinate_type_t, class allocator_type> class ImageIterator;


  //! Utility class for locking sections of the image
  //! @todo make this fully thread safe
  template <class T> struct s_simple_lock
  {
    T& r_counter;
    bool b_explicitely_unlocked;
    s_simple_lock(T &p) : r_counter(++p), b_explicitely_unlocked(false) {}
    void unlock() {b_explicitely_unlocked = true; r_counter--; }
    ~s_simple_lock() { if(!b_explicitely_unlocked) r_counter--; }
  };


  /*!@brief Template image implementation
   *
   * This structure implements an image type that is abstract in the spanned dimension and the pixel types. 
   *
   * @tparam pixel_type_t the type of the pixels
   * @tparam coordinate_type_t the type of the image's coordinate system
   * @tparam allocator_type_t the type of the allocator
   *
   * @author Raffi Enficiaud
   */
  template <
    class pixel_type_t, 
    class coordinate_type_t = s_coordinate<2>, 
    class allocator_type_t  = s_default_image_allocator<pixel_type_t, coordinate_type_t> >
  class Image : public IImage
  {
  public:
    typedef Image<pixel_type_t, coordinate_type_t, allocator_type_t> this_type;

    //! The underlying coordinate system type
    typedef coordinate_type_t                     coordinate_type;

    typedef IImage                                interface_type;
    typedef IImage::coordinate_type               interface_coordinate_type;
    typedef IImage::pixel_value_type              interface_pixel_value_type;
    typedef IImage::pixel_reference_type          interface_pixel_reference_type;


    //!@name Interface iterator types
    //!@{
    typedef IImage::iterator                      interface_iterator;
    typedef IImage::const_iterator                interface_const_iterator;
    //!@}
    
    //!@name Pixel types
    //!@{
    typedef pixel_type_t                          pixel_type;         //!< Type of the pixel
    typedef pixel_type const                      const_pixel_type;   //!< Type of immutable pixels
    //!@}
    
    //!@name Container 
    typedef pixel_type                            value_type;         //!< Type of the stored pixels, as for STL containers
    typedef pixel_type*                           pointer;            //!<
    typedef pixel_type&                           reference;          //!< Mutable reference to pixel
    typedef const_pixel_type&                     const_reference;    //!< Immutable reference to pixel
    //!@}
    
    typedef allocator_type_t                      allocator_type;
    typedef typename allocator_type::offset_type  offset_type;
    typedef offset_type                           size_type;
    //typedef ptrdiff_t                             difference_type;

    //!@name Block iterator
    //!@{
    typedef ImageIteratorNonWindowed<pixel_type, coordinate_type, allocator_type>             iterator;
    typedef ImageIteratorNonWindowedConst<pixel_type const, coordinate_type, allocator_type>  const_iterator;
    //!@}
    
    //!@name Window iterator
    //!@{
    typedef ImageIteratorWindowed<pixel_type, coordinate_type, allocator_type>                window_iterator;
    typedef ImageIteratorWindowedConst<pixel_type const, coordinate_type, allocator_type>     const_window_iterator;
    //!@}

  private:
    allocator_type                                allocator;
    typename allocator_type::pixel_map_type       pixel_map;

    int                                           read_counter;
    int                                           write_lock;
    
    yaColorSpace                                  cs;

    // Avoid copy construct
    Image(this_type const&);

  public:
    
    
    //! Default constructor
    Image() : allocator(), pixel_map(0), read_counter(0), write_lock(0), cs()
    {}

    //! Sets the current image resolution and allocation to the same as the reference image
    //! @todo ajouter la gestion du comptage de références
    template <class image_t>
    yaRC set_same(const image_t& im_ref)
    {
      yaRC res(yaRC_ok);
      bool size_are_different = (Size() != im_ref.Size());
      if(size_are_different)
      {
        if(IsAllocated() && im_ref.IsAllocated())
        {
          res = FreeImage();
          if(res != yaRC_ok)
          {
            DEBUG_INFO("Error while freeing the image");
            return res;
          }
        }
        res = SetSize(im_ref.Size());
        if(res != yaRC_ok)
        {
          DEBUG_INFO("Error while setting the size");
          return res;      
        }
      }
      
      
      if(im_ref.IsAllocated() && !IsAllocated())
      {
        yaRC res = AllocateImage();
        if(res != yaRC_ok)
        {
          DEBUG_INFO("Error during the allocation of the image");
          return res;
        }
      }
      
      return res;
    }

    virtual ~Image()
    {
      if(IsAllocated())
      {
        if(FreeImage() != yaRC_ok)
        {
          DEBUG_INFO("Error during the destruction of the image: there is still a reference preventing freeing the space");        
        }
      }
    }


    /*!@name Pixel buffer allocation management
     * @{
     */

    //! @copydoc IImage::AllocateImage
    virtual yaRC AllocateImage()
    {
      if(IsAllocated()) {
        return yaRC_E_already_allocated;
      }
      
      pixel_map = allocator.allocate(Size());
      return (pixel_map == 0 ? yaRC_E_allocation : yaRC_ok);
    }

    //! @copydoc IImage::FreeImage
    //! @todo add a critical section
    virtual yaRC FreeImage()
    {
      if(!IsAllocated()) {
        return yaRC_E_not_allocated;
      }
      
      if(!CanWriteLock())
        return yaRC_E_locked;
      
      pixel_map = allocator.deallocate(pixel_map);
      return yaRC_ok;
    }
    
    //! @copydoc IImage::IsAllocated
    virtual bool IsAllocated() const
    {
      return allocator.is_allocated(pixel_map);
    }

    //!@} //Pixel buffer allocation management


    bool operator==(const this_type& r_) const
    { 
      //  && r_.pixel_map == pixel_map
      // for now, no sharing of pix map
      return this == &r_;
    }


    /*!@name Image's size management
     * @{
     */

    yaRC SetSize(const coordinate_type &s) throw()
    {
      if(IsAllocated())
        return yaRC_E_already_allocated;
      if(!allocator.checkCoordinate(s))
        return yaRC_E_bad_parameters;
      
      allocator.size = s;
      return yaRC_ok;
    }
    
    virtual yaRC SetSize(const interface_coordinate_type& s)
    {
      return SetSize(coordinate_type(s));
    }
    
    virtual unsigned int GetDimension() const {
      return allocator.size.dimension();
    }

    virtual interface_coordinate_type GetSize() const 
    {
      return Size();
    }
    const coordinate_type& Size() const throw()
    {
      return allocator.size;
    }
    
    //! @}


    /*!@name Color space management
     * @{
     */
    virtual yaColorSpace GetColorSpace() const
    {
      return cs;
    }
    
    virtual yaRC SetColorSpace(yaColorSpace const & cs_)
    {
      cs = cs_;
      return yaRC_ok;
    }
    //! @}



    static const type& Type()
    {
      static const type t(type_description::type_desc<pixel_type>::compound, type_description::type_desc<pixel_type>::scalar);
      return t;
    }


    /*!@name IObject interface
     * @{
     */
    
    //! Type of this object
    virtual type DynamicType() const
    {
      static const type t(type_description::type_desc<pixel_type>::compound, type_description::type_desc<pixel_type>::scalar);
      return t;
    }
    
    //! Object description
    virtual string_type Description() const
    {
      std::ostringstream out;
      out << "Image" << std::endl;
      out << "\ttype: " << this->Type() << std::endl;
      out << "\tdimension: " << this->GetSize() << std::endl;
      out << "\tcolor space: " << this->GetColorSpace() << std::endl;
      out << "\t" << (this->IsAllocated() ? "allocated": "non allocated") << std::endl;
      
      return out.str();
    }

    //! @} //IObject





    /*!@name Block iterators
     * @{
     */
    
    /*! Returns a "block" const-iterator on the beginning of the image
     *
     * @pre The image is allocated.
     */
    const_iterator begin_block() const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(IsAllocated(), "image should be allocated before requesting an iterator on it. Type is " + errors::demangle(typeid(this_type).name()));
      return const_iterator(*pixel_map, coordinate_type(0), Size(), coordinate_type(0), Size());
    }

    /*! Returns a "block" const-iterator on the end of the image
     *
     * @pre The image is allocated.
     */
    const_iterator end_block() const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(IsAllocated(), "image should be allocated before requesting an iterator on it. Type is " + errors::demangle(typeid(this_type).name()));
      coordinate_type outsize(0);
      outsize[outsize.dimension() - 1] = Size()[Size().dimension() - 1];
      return const_iterator(*pixel_map, outsize, Size(), coordinate_type(0), Size());
    }

    iterator begin_block() YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(IsAllocated(), "image should be allocated before requesting an iterator on it. Type is " + errors::demangle(typeid(this_type).name()));
      return iterator(*pixel_map, coordinate_type(0), Size(), coordinate_type(0), Size());
    }
    iterator end_block() YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(IsAllocated(), "image should be allocated before requesting an iterator on it. Type is " + errors::demangle(typeid(this_type).name()));
      coordinate_type outsize(0);
      outsize[outsize.dimension() - 1] = Size()[Size().dimension() - 1];
      return iterator(*pixel_map, outsize, Size(), coordinate_type(0), Size());
    }
    //! @} //Block iterators

    /*!@name Windowed iterators
     * @{
     */
    const_window_iterator begin_window(const coordinate_type& window_start, const coordinate_type& window_size) const 
    {
      DEBUG_ASSERT(IsAllocated(), "image should be allocated before requesting an iterator on it. Type is " + errors::demangle(typeid(this_type).name()));
      for(unsigned int i = 0; i < coordinate_type::static_dimensions; i++)
      {
        if(window_start[i] < 0)
          throw errors::yaException("Bad window start at dimension " + any_to_string(i) + ": " + any_to_string(window_start));
        if(window_size[i] <= 0)
          throw errors::yaException("Bad window size at dimension " + any_to_string(i) + ": " + any_to_string(window_size));
      }
      const coordinate_type real_start = min_coordinate(window_start, Size());
      const coordinate_type real_size = min_coordinate(real_start + window_size, Size()) - real_start;

      return const_window_iterator(
        *pixel_map, 
        real_start, 
        Size(), 
        real_start, 
        real_size);
    }
    const_window_iterator end_window(const coordinate_type& window_start, const coordinate_type& window_size) const 
    {
      DEBUG_ASSERT(IsAllocated(), "image should be allocated before requesting an iterator on it. Type is " + errors::demangle(typeid(this_type).name()));
      for(unsigned int i = 0; i < coordinate_type::static_dimensions; i++)
      {
        if(window_start[i] < 0)
          throw errors::yaException("Bad window start at dimension " + any_to_string(i) + ": " + any_to_string(window_start));
        if(window_size[i] <= 0)
          throw errors::yaException("Bad window size at dimension " + any_to_string(i) + ": " + any_to_string(window_size));
      }
      const coordinate_type real_start = min_coordinate(window_start, Size());
      const coordinate_type real_size = min_coordinate(real_start + window_size, Size()) - real_start;
      coordinate_type outcoord(real_start);
      outcoord[outcoord.dimension() - 1] = real_start[outcoord.dimension() - 1] + real_size[outcoord.dimension() - 1];
      return const_window_iterator(
        *pixel_map, 
        outcoord, 
        Size(), 
        real_start, 
        real_size);
    }

    window_iterator begin_window(const coordinate_type& window_start, const coordinate_type& window_size) 
    {
      DEBUG_ASSERT(IsAllocated(), "image should be allocated before requesting an iterator on it. Type is " + errors::demangle(typeid(this_type).name()));
      for(unsigned int i = 0; i < coordinate_type::static_dimensions; i++)
      {
        if(window_start[i] < 0)
          throw errors::yaException("Bad window start at dimension " + any_to_string(i) + ": " + any_to_string(window_start));
        if(window_size[i] <= 0)
          throw errors::yaException("Bad window size at dimension " + any_to_string(i) + ": " + any_to_string(window_size));
      }
      //return window_iterator(*pixel_map, window_start, Size(), window_start, window_size);
      const coordinate_type real_start = min_coordinate(window_start, Size());
      const coordinate_type real_size = min_coordinate(real_start + window_size, Size()) - real_start;
      return window_iterator(
        *pixel_map, 
        real_start, 
        Size(), 
        real_start, 
        real_size);      
    }
    window_iterator end_window(const coordinate_type& window_start, const coordinate_type& window_size) 
    {
      DEBUG_ASSERT(IsAllocated(), "image should be allocated before requesting an iterator on it. Type is " + errors::demangle(typeid(this_type).name()));
      for(unsigned int i = 0; i < coordinate_type::static_dimensions; i++)
      {
        if(window_start[i] < 0)
          throw errors::yaException("Bad window start at dimension " + any_to_string(i) + ": " + any_to_string(window_start));
        if(window_size[i] <= 0)
          throw errors::yaException("Bad window size at dimension " + any_to_string(i) + ": " + any_to_string(window_size));
      }
      //coordinate_type outcoord(window_start);
      //outcoord[outcoord.dimension() - 1] = std::min(Size()[outcoord.dimension() - 1], window_start[outcoord.dimension() - 1] + window_size[outcoord.dimension() - 1]);
      //return window_iterator(*pixel_map, outcoord, Size(), window_start, window_size);
      const coordinate_type real_start = min_coordinate(window_start, Size());
      const coordinate_type real_size  = min_coordinate(real_start + window_size, Size()) - real_start;
      coordinate_type outcoord(real_start);
      outcoord[outcoord.dimension() - 1] = real_start[outcoord.dimension() - 1] + real_size[outcoord.dimension() - 1];
      return window_iterator(
        *pixel_map, 
        outcoord, 
        Size(), 
        real_start, 
        real_size);
    }
    
    //! @} //Windowed iterators


    /*!@name Iterators interface
     * @{
     */
    virtual interface_const_iterator begin() const throw() { return (!IsAllocated() ? 0 : new const_iterator(begin_block())); }
    virtual interface_const_iterator end() const throw()   { return (!IsAllocated() ? 0 : new const_iterator(end_block()));   }
    virtual interface_iterator       begin() throw()       { return (!IsAllocated() ? 0 : new iterator(begin_block()));       }
    virtual interface_iterator       end() throw()         { return (!IsAllocated() ? 0 : new iterator(end_block()));         }
    //!@}    
    





    //!@name Pixel access
    //!@{
    
    /*! Mutable pixel access from a coordinate
     *
     * @note A conversion from the coordinate to an offset is performed.
     */
    reference pixel(coordinate_type const& coord) YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(IsAllocated() && is_point_inside(this->Size(), coord), "image should be allocated before requesting a pixel");
      DEBUG_ASSERT(is_point_inside(this->Size(), coord), 
        "Trying to access to a pixel outside the support of the image : requested coord : " + any_to_string(coord) + " -- size : " + any_to_string(this->Size()));
      return *(pixel_map + allocator.from_coordinate_to_offset(coord));
    }
    /*! Non-mutable pixel access from a coordinate
     *
     * @note A conversion from the coordinate to an offset is performed.
     */
    const_reference pixel(coordinate_type const& coord) const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(IsAllocated(), "image should be allocated before requesting a pixel");
      DEBUG_ASSERT(is_point_inside(this->Size(), coord), 
        "Trying to access to a pixel outside the support of the image : requested coord : " + any_to_string(coord) + " -- size : " + any_to_string(this->Size()));
      return *(pixel_map + allocator.from_coordinate_to_offset(coord));
    }
    
    /*! Mutable pixel access from an offset
     *
     * This is the cheapest access to a specific pixel
     * @warning runtime checks are in debug only
     */
    reference pixel(offset_type const& off) YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(IsAllocated(), "image should be allocated before requesting a pixel");
      DEBUG_ASSERT(off >= 0 && off < total_number_of_points(this->Size()), 
        "Trying to access to a pixel outside the support of the image : requested offset : " + any_to_string(off) + " -- max offset : " + any_to_string(total_number_of_points(this->Size())));
      return *(pixel_map + off);
    }
    
    //! Pixel access from an offset (const)
    const_reference pixel(offset_type const& off) const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(IsAllocated(), "image should be allocated before requesting a pixel");
      DEBUG_ASSERT(off >= 0 && off < total_number_of_points(this->Size()), 
        "Trying to access to a pixel outside the support of the image : requested offset : " + any_to_string(off) + " -- max offset : " + any_to_string(total_number_of_points(this->Size())));
      return *(pixel_map + off);
    }

    //!@}



    //! A fake pixel type handling conversion
    struct pixel_proxy : public IVariantProxy
    {
      typedef pixel_proxy this_type;
      pixel_type* pixel;

      pixel_proxy(pixel_type& _pixel) : pixel(&_pixel){}


      //! Assignment operator
      this_type& operator=(const this_type& r_)
      {
        pixel = r_.pixel;
        return *this;
      }

      //! Sets the value of the pixel
      interface_pixel_value_type const& operator=(const interface_pixel_value_type& variant_ref)
      {
        *pixel = variant_ref.operator pixel_type();
        return variant_ref;
      }

      //! Returns the value of the pixel
      operator interface_pixel_value_type() const
      {
        return interface_pixel_value_type(*pixel);
      }
      
      bool operator==(const interface_pixel_value_type& variant_ref) const
      {
        return variant_ref.operator pixel_type() == *pixel;
      }
      bool operator==(const pixel_proxy& r_) const
      {
        return *pixel == *r_.pixel;
      }
      bool operator!=(const interface_pixel_value_type& variant_ref) const
      {
        return variant_ref.operator pixel_type() != *pixel;
      }
      bool operator!=(const pixel_proxy& r_) const
      {
        return *pixel != *r_.pixel;
      }      
      
    protected:
      interface_pixel_value_type  getPixel() const {return this->operator interface_pixel_value_type();}
      yaRC                        setPixel(const interface_pixel_value_type &v) 
      {
        this->operator=(v);
        return yaRC_ok;
      }
      bool    isEqual     (const interface_pixel_value_type &v) const {return this->operator==(v);}
      bool    isDifferent (const interface_pixel_value_type &v) const {return this->operator!=(v);}
      bool    isEqual     (const IVariantProxy &v) const {return this->operator==(dynamic_cast<const this_type&>(v));}
      bool    isDifferent (const IVariantProxy &v) const {return this->operator!=(dynamic_cast<const this_type&>(v));}      
      
    };

    //! Pixel access from the interface, given a generic coordinate (const version)
    virtual interface_pixel_value_type pixel(const interface_coordinate_type& coord) const
    {
      if(!IsAllocated())
        throw errors::yaException(yaRC_E_not_allocated);
      coordinate_type c(coord);
      if(!is_point_inside(this->Size(), c))
        throw errors::yaException(yaRC_E_bad_parameters);
      return interface_pixel_value_type(this->pixel(c));
    }

    //! Pixel access from the interface, given a generic coordinate
    virtual interface_pixel_reference_type  pixel(const interface_coordinate_type& coord)
    {
      if(!IsAllocated())
        throw errors::yaException(yaRC_E_not_allocated);
      coordinate_type c(coord);
      if(!is_point_inside(this->Size(), c))
        throw errors::yaException(yaRC_E_bad_parameters);
      return std::auto_ptr<interface_pixel_reference_type::element_type>(new pixel_proxy(this->pixel(c)));
      // should return a proxy to the pixel
      //return dynamic_cast<interface_pixel_reference_type&>(prox);
    }
    

    //! A scoped object
    typedef const s_simple_lock<int> read_lock_type;
    
    /*!Sets the lock on the whole image. The returned object should either be destructed or explicitly
     * unlocked to release this lock.
     * @note The current implementation does not check if the image can be read-locked. 
     * @see s_simple_lock
     */
    read_lock_type ReadLock() {
      // This should be a critical section
      return read_lock_type(read_counter);
    }
    
    //! Returns true if the image can be locked for reading.
    //! The image is available for read-locking of no write lock is set on.
    bool CanReadLock() const {
      return write_lock == 0;
    }

    typedef const s_simple_lock<int> write_lock_type;
    
    /*!@brief Sets the write-lock on the whole image. 
     * The returned object should either be destructed or explicitly unlocked to release this lock.
     * @note The current implementation does not check if the image can be read-locked. 
     * @see s_simple_lock
     */
    write_lock_type WriteLock() {
      // This should be a critical section
      return write_lock_type(write_lock);
    }
    
    //! Returns true if the image can be locked for writing.
    //! The image is available for write-locking of no read lock is set on (read counter set to 0).    
    bool CanWriteLock() const {
      return (read_counter == 0) && (write_lock == 0);
    }
    
    
    //! Swaps the content of the two images
    yaRC swap(this_type& r_) throw()
    {
      if(this == &r_)
        return yaRC_ok;
        
      if(!CanWriteLock() || !r_.CanWriteLock())
        return yaRC_E_locked;
      
      {
        write_lock_type l1(WriteLock()), l2(r_.WriteLock());
        std::swap(pixel_map, r_.pixel_map);
        std::swap(allocator, r_.allocator);
      }
      
      return yaRC_ok;
    
    }
    
    
    
    //!@name Streaming methods
    //!@{    
    
    //! Input streaming function
    template <class i_stream>
    friend bool operator>>(i_stream& is, this_type&im) {
      if(!im.IsAllocated())
        return false;
        
      pixel_type t;
      for(iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it)
      {
        if(!any_from_string(is, t))
          return false;
        *it = t;
      }
      return true;
    }
    
    //! Output streaming function
    template <class o_stream>
    friend o_stream& operator<<(o_stream& os, const this_type&im) {
      for(const_iterator it = im.begin_block(), ite = im.end_block(); it != ite; ++it) {
        os << *it;
      }
      return os;
    }
    
    //! @}

  };
  
  
  
  //! Utility template structure for transforming the type of the pixel into another (hence retaining the other parameters)
  template <class pixel_t, class image_t>
  struct s_get_same_image_of_t
  {
    typedef Image<
      pixel_t, 
      s_coordinate<image_t::coordinate_type::static_dimensions>, 
      typename s_get_same_allocator_of_t<pixel_t, typename image_t::allocator_type>::type 
    > type;
  };
  //!@}
} // namespace yayi


#endif /*YAYI_IMAGE_CORE_IMPL_HPP__*/

