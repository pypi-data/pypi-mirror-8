#ifndef YAYIIMAGEITERATOR_HPP__
#define YAYIIMAGEITERATOR_HPP__


#include <yayiImageCore/include/yayiImageCore.hpp>
#include <yayiImageCore/include/yayiImageUtilities_T.hpp>

#include <boost/type_traits/add_const.hpp>
#include <boost/type_traits/remove_reference.hpp>
#include <boost/type_traits/add_reference.hpp>
#include <boost/operators.hpp> 
#include <iterator>

namespace yayi
{
  /*!@addtogroup iterators_grp
   * @{
   */

  template <class pixel_type_t, class coordinate_type_t>                          struct s_default_image_allocator;
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>  class ImageIteratorWindowBase;
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>  class ImageIteratorContinuousBase;

  namespace
  {

    //! Iterator strategy based on the allocator (continuous vs. non continous maps)
    template <class pixel_type_t, class coordinate_type_t, class allocator_type>
    struct s_iterator_choice_strategy {
      // by default, we use the windowed iterator (the more generic)
      typedef ImageIteratorWindowBase<
        typename allocator_type::pixel_type,
        typename allocator_type::coordinate_type,
        allocator_type
        > type;
    };

    template <class pixel_type_t, class coordinate_type_t, class T1, class C1>
    struct s_iterator_choice_strategy  < pixel_type_t, coordinate_type_t, s_default_image_allocator<T1, C1> > {
      // the default image allocator allocates continous memory
      typedef ImageIteratorContinuousBase<
        pixel_type_t,
        coordinate_type_t,
        s_default_image_allocator<T1, C1>
        > type;
    };
  }

  /*!@defgroup iterators_block_grp Block iterators
   * @ingroup iterators_grp
   * @brief Iterators spanning all pixels of an image in "video" order.
   *
   * Block iterators span all the pixels of an image in the "video" order, which means 
   * - from lowest to highest dimension index (x, then y, then z, then ...)
   * - from smallest to highest coordinate in each of the dimensions ((x,y)=(0,0),(1,0),(2,0)...(0,1), (1,1), (2,1)...)
   *
   * @note The iterators of this category all implement the <a href="http://www.sgi.com/tech/stl/RandomAccessIterator.html">random access</a> 
   * iterator concept. 
   * @{
   */


  /*!@brief Images' block iterator base class.
   *
   * This is the base implementation class of the block iterator concept. 
   * @note Most of the operations are implemented using the "operators" library of boost (boost::random_access_iterator_helper).
   * @author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>
  class ImageIteratorContinuousBase :
    public IConstIterator,
    public boost::random_access_iterator_helper<
      ImageIteratorContinuousBase<pixel_type_t, coordinate_type_t, allocator_type_t>, // current type
      pixel_type_t,   // value type
      offset>         // difference type
  {
  public:
    
    //! This instance type
    typedef ImageIteratorContinuousBase<pixel_type_t, coordinate_type_t, allocator_type_t> this_type;

    typedef coordinate_type_t                               coordinate_type;
    

    //!@name Types related to iterator interface
    //!@{
    typedef IConstIterator                                  interface_type;
    typedef interface_type::coordinate_type                 interface_coordinate_type;
    typedef interface_type::pixel_type                      interface_pixel_value_type;
    //!@}
    

    //!@name Types related to iterator traits
    //!@{
    typedef boost::iterator<std::random_access_iterator_tag, pixel_type_t, offset> iterator_traits_t;
    typedef typename iterator_traits_t::iterator_category iterator_category;
    typedef typename iterator_traits_t::value_type        value_type;
    typedef typename iterator_traits_t::pointer           pointer;
    typedef typename iterator_traits_t::difference_type   difference_type;
    typedef typename iterator_traits_t::reference         reference;
    //!@}



  private:
  
    //! Pointer to the current pixel in the image
    pointer            p_;
    
    //! Pointer to the origin pixel of the image
    pointer            p_0;
    
    //! Size of the grid (necessary to get the positions from the offsets)
    coordinate_type    grid_size;

    // The const and non const versions are friends.
    friend class ImageIteratorContinuousBase<
      typename boost::mpl::if_<
        boost::is_const<pixel_type_t>,
        typename boost::remove_const<pixel_type_t>::type,
        typename boost::add_const<pixel_type_t>::type
      >::type,
      coordinate_type_t,
      allocator_type_t>;
  public:

    //! Default constructor
    ImageIteratorContinuousBase() : p_(0), p_0(0), grid_size()
    {}

    //! Constructor from image information
    ImageIteratorContinuousBase(
      value_type&             initial_pixel,
      const coordinate_type&  init_coord,
      const coordinate_type&  grid_size_,
      const coordinate_type&  ,
      const coordinate_type&  ) :
      p_(&initial_pixel + from_coordinate_to_offset(grid_size_, init_coord)), p_0(&initial_pixel), grid_size(grid_size_)
    {}


    //! Template constructor from another type
    template <typename v_type>
    ImageIteratorContinuousBase(const ImageIteratorContinuousBase<v_type, coordinate_type_t, allocator_type_t>& it) :
      p_(it.p_), p_0(it.p_0), grid_size(it.grid_size)
    {}

    //!@name Iterator motion
    //!@{

    //! Moves the iterator forward to the next position
    this_type& operator++() throw()
    {
      ++p_;
      return *this;
    }

    //! Moves the iterator backward to the previous position
    this_type& operator--() throw()
    {
      --p_;
      return *this;
    }

    //! Moves the iterator forward to the current position + d
    this_type& operator+=(difference_type d) throw()
    {
      p_ += d;
      return *this;
    }

    //! Moves the iterator backward to the current position - d
    this_type& operator-=(difference_type d) throw()
    {
      p_ -= d;
      return *this;
    }
    //!@}

    //! Difference / signed distance between iterators
    difference_type operator-(this_type const &it2) const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(this->p_0 == it2.p_0 && this->grid_size == it2.grid_size , "Trying to compare iterators on different geometries or different images");
      return this->p_ - it2.p_;
    }

    //!@name Iterator comparison
    //!@{


    //!@brief Iterator equality
    //! Two iterators are equal if they point to the same pixel. 
    bool operator==(const this_type& r) const throw()
    {
      return p_ == r.p_;
    }

    //! Less-than comparable concept
    bool operator<(const this_type& r) const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(p_0 == r.p_0 && grid_size == r.grid_size , "Trying to compare iterators on different geometries or different images");
      return p_ < r.p_;
    }

    //!@}


    //! Position
    coordinate_type Position() const
    {
      return from_offset_to_coordinate<coordinate_type>(grid_size, Offset());
    }

    //! Returns the pixel index in the image
    offset Offset() const {
      return p_ - p_0;
    }


    //! Dereference operator
    reference operator*() const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(p_ < p_0 + total_number_of_points(grid_size) , "Trying to deference an iterator outside the image");
      DEBUG_ASSERT(p_0 <= p_ , "Trying to deference an iterator outside the image");
      return *p_;
    }

    //! Dereference operator array style
    //!@note This index operator seems more efficient than the one provided by boost.
    reference operator[](difference_type d) const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(p_0 <= p_ +d , "Trying to deference an iterator outside the image");
      DEBUG_ASSERT(p_ + d < p_0 + total_number_of_points(grid_size) , "Trying to deference an iterator outside the image");
      return p_[d];
    }

    /*!@name Interface methods
     * @{
     */
    //! Position retrieval (@ref IIterator interface)
    virtual interface_coordinate_type GetPosition() const throw()
    {
      return interface_coordinate_type(Position());
    }

    virtual offset GetOffset() const throw() {
      return Offset();
    }

    //!@todo implement this method (since it is rather easy) 
    virtual yaRC SetPosition(const interface_coordinate_type&) throw()
    {
      return yaRC_E_not_implemented;
    }

    virtual bool is_equal(const interface_type* const& it_interface) const
    {
      const this_type* it_ = dynamic_cast<const this_type*>(it_interface);
      if(!it_)
        throw yayi::errors::yaException("argument iterator of wrong type");
      return (*this) == (*it_);
    }
    virtual bool is_different(const interface_type* const& it_interface) const
    {
      const this_type* it_ = dynamic_cast<const this_type*>(it_interface);
      if(!it_)
        throw yayi::errors::yaException("argument iterator of wrong type");
      return (*this) != (*it_);
    }

    virtual type DynamicType () const
    {
      // @TODO proper type setting
      static const type t(type::c_iterator, type::s_image);
      return t;
    }

    virtual string_type Description() const
    {
      return "Continuous iterator";
    }


  protected:
    virtual interface_pixel_value_type getPixel() const {
      return interface_pixel_value_type(*p_);
    }

    virtual yaRC next() {
      this->operator++();
      return yaRC_ok;
    }
    virtual yaRC previous() {
      this->operator--();
      return yaRC_ok;
    }
    virtual this_type* clone() const throw() {
      // this works because the children classes do not have special copy constructors ?
      return new this_type(*this);
    }
    //!@} // Interface methods

  };

  //!@} // iterators_block_grp









  /*!@defgroup iterators_windows_grp Windowed iterators
   * @ingroup iterators_grp
   * @brief Iterators spanning a subset of an image, the subset defined by an hyperrectangle.
   *
   * Within the subset, the iterators span all the pixels in the "video" order, which means 
   * - from lowest to highest dimension index (x, then y, then z, then ...)
   * - from smallest to highest coordinate in each of the dimensions ((x,y)=(0,0),(1,0),(2,0)...(0,1), (1,1), (2,1)...)
   *
   * @note It is the responsibility of the caller to ensure the subset is properly defined.
   * @note The iterators of this category all implement the <a href="http://www.sgi.com/tech/stl/RandomAccessIterator.html">random access</a> 
   * iterator concept. 
   * @{
   */

  /*!@brief Image windowed iterator type
   *
   * @author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>
  class ImageIteratorWindowBase :
    public IConstIterator,
    public boost::random_access_iterator_helper<
      ImageIteratorWindowBase<pixel_type_t, coordinate_type_t, allocator_type_t>, // current type
      pixel_type_t, // value type
      offset> // difference type
  {


  public:
    //! This instance type
    typedef ImageIteratorWindowBase<pixel_type_t, coordinate_type_t, allocator_type_t> this_type;

    //!@name Types related to iterator interface
    //!@{
    typedef IConstIterator                                  interface_type;
    typedef coordinate_type_t                               coordinate_type;
    typedef interface_type::coordinate_type                 interface_coordinate_type;
    typedef interface_type::pixel_type                      interface_pixel_value_type;
    //!@}

    //!@name Types related to iterator traits
    //!@{
    typedef boost::iterator<std::random_access_iterator_tag, pixel_type_t, offset> iterator_traits_t;
    typedef typename iterator_traits_t::iterator_category iterator_category;
    typedef typename iterator_traits_t::value_type        value_type;
    typedef typename iterator_traits_t::pointer           pointer;
    typedef typename iterator_traits_t::difference_type   difference_type;
    typedef typename iterator_traits_t::reference         reference;
    //!@}


  private:
    pointer  p_;
    pointer  p_0;

    coordinate_type                                         coord, grid_size;
    coordinate_type                                         window_begin, window_end;

    friend class ImageIteratorWindowBase<
      typename boost::mpl::if_<
        boost::is_const<pixel_type_t>, 
        typename boost::remove_const<pixel_type_t>::type, 
        typename boost::add_const<pixel_type_t>::type>::type,
      coordinate_type_t,
      allocator_type_t>;


  public:

    //! Default constructor
    ImageIteratorWindowBase() :
      p_(0), p_0(0), coord(), grid_size(), window_begin(), window_end()
    {}

    //! Constructor
    ImageIteratorWindowBase(
      reference               initial_pixel,
      const coordinate_type&  init_coord,
      const coordinate_type&  grid_size_,
      const coordinate_type&  window_begin_,
      const coordinate_type&  window_size_) :
    p_(&initial_pixel + from_coordinate_to_offset(grid_size_, init_coord)),
      p_0(&initial_pixel),
      coord(init_coord), grid_size(grid_size_),
      window_begin(window_begin_), window_end(window_begin_+window_size_)
    {
      // assert coord is inside
    }

    //! Template constructor from another type
    template <typename v_type>
    ImageIteratorWindowBase(const ImageIteratorWindowBase<v_type, coordinate_type_t, allocator_type_t>& it) :
      p_(it.p_), p_0(it.p_0),
      coord(it.coord),
      grid_size(it.grid_size),
      window_begin(it.window_begin), window_end(it.window_end)
    {}


    //! Advance the iterator to the next position
    this_type& operator++()
    {
      offset hyperplan_size = 1;
      for(unsigned int i = 0, j = coord.dimension(); i < j; i ++)
      {
        typename coordinate_type::scalar_coordinate_type& current = coord[i];
        current++;
        if(current < window_end[i])
        {
          p_++;
          break;
        }

        // ici ajout padding ?
        if(i == coord.dimension() - 1)
          break;

        current = window_begin[i];
        p_ += hyperplan_size*(grid_size[i] - (window_end[i] - current)); // Raffi : +1 ?? je ne sais jamais... à tester
        hyperplan_size *= grid_size[i];
      }


      return *this;
    }

    //! Advance the iterator to the next position
    this_type& operator--()
    {
      offset hyperplan_size = 1;
      for(unsigned int i = 0; i < coord.dimension(); i ++)
      {
        typename coordinate_type::scalar_coordinate_type& current = coord[i];
        current--;
        if(current >= window_begin[i])
        {
          p_--;
          break;
        }
        if(i == coord.dimension() - 1)
          break;

        // ici ajout padding ?
        current = window_end[i]-1;
        p_ -= hyperplan_size*(grid_size[i] - (current - window_begin[i]));
        hyperplan_size *= grid_size[i];
      }
      return *this;
    }

    //! Advance the iterator to the current position + d
    this_type& operator+=(difference_type d) throw()
    {
      offset hyperplan_size = 1;
      for(unsigned int i = 0, j = coord.dimension(); i < j; i ++)
      {
        typename coordinate_type::scalar_coordinate_type& current = coord[i];
        difference_type current_dimension_advance = d % (window_end[i] - window_begin[i]);
        d /= (window_end[i] - window_begin[i]);
        if(current + current_dimension_advance >= window_end[i])
        {
          current_dimension_advance -= window_begin[i];
          d++;
        }
        current += current_dimension_advance;
        p_ += hyperplan_size*current_dimension_advance;
        hyperplan_size *= grid_size[i];
      }
      return *this;
    }

    //! Reverses the iterator to the current position + d
    this_type& operator-=(difference_type d) throw()
    {
      offset hyperplan_size = 1;
      for(unsigned int i = 0, j = coord.dimension(); i < j; i ++)
      {
        typename coordinate_type::scalar_coordinate_type& current = coord[i];
        difference_type current_dimension_advance = d % (window_end[i] - window_begin[i]);
        d /= (window_end[i] - window_begin[i]);
        if(current - current_dimension_advance < window_begin[i])
        {
          current_dimension_advance += window_end[i];
          d++;
        }
        current -= current_dimension_advance;
        p_ -= hyperplan_size*current_dimension_advance;
        hyperplan_size *= grid_size[i];
      }
      return *this;
    }

    //! Index operator (very inefficient)
    reference operator[](difference_type d) const
    {
      this_type t = *this + d;
      return *t;
    }


    //! Difference
    difference_type operator-(this_type const &r) const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(this->p_0 == r.p_0 && this->grid_size == r.grid_size , "Trying to compare iterators on different geometries");
      offset pave_size = 1, diff = 0;
      for(unsigned int i = 0, j = coord.dimension(); i < j; i ++)
      {
        diff += (coord[i] - r.coord[i]) * pave_size;
        pave_size *= window_end[i] - window_begin[i] + 1;
      }
      return diff;
    }

    //! Comparaison operator
    bool operator<(this_type const& r) const
    {
      for(int i = coord.dimension()-1; i >= 0; i --)
      {
        if(coord[i] < r.coord[i])
          return true;
      }
      return false;
    }




    //! Dereference operator
    reference operator*() const
    {
      DEBUG_ASSERT(p_ < p_0 + total_number_of_points(grid_size) , "Trying to deference an iterator after the end of the image");
      return *p_;
    }

    //! Comparison operator
    bool operator==(const this_type& r) const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(r.window_begin == window_begin && r.window_end == window_end && grid_size == r.grid_size, "Comparison between incompatible iterators (different ranges)");
      return coord == r.coord;
    }

    const coordinate_type& Position() const
    {
      return coord;
    }
    
    offset Offset() const
    {
      return p_ - p_0;
    }

    virtual interface_coordinate_type GetPosition() const throw()
    {
      return interface_coordinate_type(Position());
    }
    virtual yaRC SetPosition(const interface_coordinate_type&) throw()
    {
      return yaRC_E_not_implemented;
    }
    virtual offset GetOffset() const throw() {
      return Offset();
    }


    /*!@name Interface Methods
     * @{
     */
    virtual bool is_equal(const interface_type*const& it_interface) const throw()
    {
      const this_type* it_this = dynamic_cast<const this_type*>(it_interface);
      if(!it_this)
        return false;
      return this->operator ==(*it_this);
    }
    virtual bool is_different(const interface_type*const& it_interface) const throw()
    {
      const this_type* it_this = dynamic_cast<const this_type*>(it_interface);
      if(!it_this)
        return true;
      return ((*this) != (*it_this));
    }

    virtual type DynamicType() const
    {
      // @TODO proper type setting
      static const type t(type::c_iterator, type::s_image);
      return t;
    }

    virtual string_type Description() const
    {
      return "Hyperrectangle iterator";
    }

    //!@}

  protected:
    virtual interface_pixel_value_type getPixel() const {
      return interface_pixel_value_type(value_type(0));
    }
    virtual yaRC next() {
      this->operator++();
      return yaRC_ok;
    }
    virtual yaRC previous() {
      this->operator--();
      return yaRC_ok;
    }

    virtual this_type* clone() const throw() {
      // this works because the children classes do not have special copy constructors ?
      return new this_type(*this);
    }
  };
  //!@} // iterators_windows_grp




  /*!@addtogroup iterators_block_grp
   * @{
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>
  class ImageIteratorNonWindowed;

  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>
  class ImageIteratorNonWindowedConst;


  /*!@brief Non windowed iterator
   *
   *@author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>
  class ImageIteratorNonWindowed :
    public s_iterator_choice_strategy<pixel_type_t, coordinate_type_t, allocator_type_t>::type,
    public IIterator
  {
    typedef typename s_iterator_choice_strategy<pixel_type_t, coordinate_type_t, allocator_type_t>::type parent_type;

  public:
    typedef typename parent_type::coordinate_type             coordinate_type;
    typedef typename parent_type::reference                   reference;
    typedef typename parent_type::value_type                  value_type;
    typedef typename parent_type::interface_pixel_value_type  interface_pixel_value_type;

  public:
    //! Constructor from image information
    ImageIteratorNonWindowed(reference               initial_pixel,
                             const coordinate_type&  init_coord,
                             const coordinate_type&  grid_size_,
                             const coordinate_type&  window_begin_,
                             const coordinate_type&  window_size_) : parent_type(initial_pixel, init_coord, grid_size_, window_begin_, window_size_)
    {}

    //! Default constructor
    ImageIteratorNonWindowed() : parent_type()
    {}

    //! Construction from parent
    ImageIteratorNonWindowed(parent_type const &p) : parent_type(p)
    {}


    reference operator*() const
    {
      return this->parent_type::operator*();
    }


  protected:
    virtual yaRC setPixel(const interface_pixel_value_type& v) {
      this->operator*() = v.operator value_type();
      return yaRC_ok;
    }

  };


  /*!@brief Non windowed const iterator
   *
   *@author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>
  class ImageIteratorNonWindowedConst :
    public s_iterator_choice_strategy<typename boost::add_const<pixel_type_t>::type, coordinate_type_t, allocator_type_t>::type
  {
    typedef typename s_iterator_choice_strategy<typename boost::add_const<pixel_type_t>::type, coordinate_type_t, allocator_type_t>::type parent_type;

  public:
    typedef typename parent_type::coordinate_type             coordinate_type;
    typedef typename
    boost::add_reference<
      typename boost::add_const<
        typename boost::remove_reference<typename parent_type::reference>::type
        >::type
        >::type reference;
    typedef typename parent_type::value_type                  value_type;
    typedef typename parent_type::interface_pixel_value_type  interface_pixel_value_type;

  public:
    //! Default constructor
    ImageIteratorNonWindowedConst() : parent_type() {}

    //! Default constructor
    ImageIteratorNonWindowedConst(parent_type const &p) : parent_type(p) {}

    //! Constructor from image information
    ImageIteratorNonWindowedConst(
      reference               initial_pixel,
      const coordinate_type&  init_coord,
      const coordinate_type&  grid_size_,
      const coordinate_type&  window_begin_,
      const coordinate_type&  window_size_)
      : parent_type(initial_pixel, init_coord, grid_size_, window_begin_, window_size_)
    {}

    //! Constructor from non const similar iterator
    template <class pix_t>
    ImageIteratorNonWindowedConst(ImageIteratorContinuousBase<pix_t, coordinate_type_t, allocator_type_t> const& it) :
      parent_type(it)
    {}

    reference operator*() const
    {
      return this->parent_type::operator*();
    }
  };


  //!@}






  /*!@addtogroup iterators_windows_grp
   * @{
   */

  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>
  class ImageIteratorWindowed;
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>
  class ImageIteratorWindowedConst;

  /*!@brief Windowed iterator
   *
   *@author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>
  class ImageIteratorWindowed :
    public ImageIteratorWindowBase<pixel_type_t, coordinate_type_t, allocator_type_t>,
    public IIterator
  {
    typedef ImageIteratorWindowBase<pixel_type_t, coordinate_type_t, allocator_type_t> parent_type;
    //friend class ImageIteratorWindowedConst<typename boost::add_const<pixel_type_t>::type, coordinate_type_t, allocator_type_t>;

  public:
    typedef typename parent_type::coordinate_type coordinate_type;
    typedef typename parent_type::reference       reference;
    typedef typename parent_type::value_type      value_type;
    typedef typename parent_type::interface_pixel_value_type  interface_pixel_value_type;

  public:
    ImageIteratorWindowed(
      reference               initial_pixel,
      const coordinate_type&  init_coord,
      const coordinate_type&  grid_size_,
      const coordinate_type&  window_begin_,
      const coordinate_type&  window_size_) :
    parent_type(initial_pixel, init_coord, grid_size_, window_begin_, window_size_)
    {}

    ImageIteratorWindowed(parent_type const &r) : parent_type(r)
    {}

    reference operator*() const
    {
      return this->parent_type::operator*();
    }

  protected:
    virtual yaRC setPixel(const interface_pixel_value_type& v) {
      this->operator*() = v.operator value_type();
      return yaRC_ok;
    }

  };

  /*!@brief Windowed const iterator
   *
   *@author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>
  class ImageIteratorWindowedConst :
    public ImageIteratorWindowBase<pixel_type_t, coordinate_type_t, allocator_type_t>
  {
    typedef ImageIteratorWindowBase<pixel_type_t, coordinate_type_t, allocator_type_t> parent_type;
  public:
    typedef typename parent_type::coordinate_type coordinate_type;
    //typedef typename parent_type::reference  reference;
    typedef typename
    boost::add_reference<
      typename boost::add_const<
        typename boost::remove_reference<typename parent_type::reference>::type
        >::type
        >::type reference;
    typedef typename parent_type::value_type      value_type;
    typedef ImageIteratorWindowedConst<pixel_type_t, coordinate_type_t, allocator_type_t> this_type;

  public:
    ImageIteratorWindowedConst(parent_type const &r) : parent_type(r)
    {}


    ImageIteratorWindowedConst(
      reference               initial_pixel,
      const coordinate_type&  init_coord,
      const coordinate_type&  grid_size_,
      const coordinate_type&  window_begin_,
      const coordinate_type&  window_size_) :
      parent_type(initial_pixel, init_coord, grid_size_, window_begin_, window_size_)
    {}

    //! Constructor from non const similar iterator
    template <class pix_t>
    ImageIteratorWindowedConst(ImageIteratorWindowBase<pix_t, coordinate_type_t, allocator_type_t> const& it) :
      parent_type(it)
    {}

    //template <class pix_t>
    //this_type& operator=(ImageIteratorWindowed<pix_t, coordinate_type_t, allocator_type_t> const& it);

    reference operator*() const
    {
      return this->parent_type::operator*();
    }
  };
  //! @} //iterators_windows_grp

  //! @} //iterators
}


#endif

