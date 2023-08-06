
#include <yayiImageCorePython/imagecore_python.hpp>
#include <yayiImageCore/yayiImageCoreFunctions.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>

#include <boost/python/class.hpp>
#include <boost/python/manage_new_object.hpp>
#include <boost/python/return_internal_reference.hpp>
#include <boost/python/return_value_policy.hpp>
#include <boost/python/make_function.hpp>
#include <boost/python/iterator.hpp>
#include <boost/python/suite/indexing/indexing_suite.hpp>


namespace yayi {
  IImage::pixel_reference_type::element_type* pixel_method_wrapper(IImage * im, const IImage::coordinate_type& c) {
    if(im == 0)
      throw errors::yaException(yaRC_E_null_pointer);
    
    IImage::pixel_reference_type v_ret = im->pixel(c);
    if(v_ret.get() == 0)
      throw errors::yaException(yaRC_E_allocation);

    return v_ret.release();
  }

  IIteratorWrapper image_range(IImage*im) {
    return IIteratorWrapper(im->begin(), im->end());
  }
  

}


namespace array_details
{
  /*!@brief Proxy object for emulating the slices
   * @tparam iterator_t should be a model of random access iterator
   */
  template <typename iterator_t>
  class array_proxy
  {
  public:
    // Types
    typedef iterator_t iterator;
    typedef typename iterator_t::value_type       value_type;
    typedef typename iterator_t::reference        reference;
    typedef typename iterator_t::difference_type  difference_type;
    typedef std::size_t size_type;
    

    //! @brief Empty constructor.
    array_proxy() : it_begin(), it_end(), length_(0)
    {}

    //! @brief Construct with iterators.
    array_proxy(iterator_t const &begin, iterator_t const& end) : it_begin(begin), it_end(end), length_(std::distance(begin, end))
    {}

    // Iterator support.
    iterator begin() const
    {
      return it_begin;
    }
    iterator end() const
    {
      return it_end;
    }

    // Element access
    reference operator[](size_t i) const
    {
      return it_begin[i];
    }

    // Capacity.
    size_type size() const
    {
      return length_;
    }

  private:
    iterator_t it_begin, it_end;
    std::size_t length_;
  };
  


  /*!@brief Policy type for referenced indexing, meeting the DerivedPolicies
   *        requirement of boost::python::index_suite.
   *
   * @note Requires Container to support:
   *         - value_type and size_type types,
   *         - value_type is default constructable and copyable,
   *         - element access via operator[],
   *         - Default constructable, iterator constructable,
   *         - begin(), end(), and size() member functions
   */
  template <typename container_t>
  class ref_index_suite :
    public boost::python::indexing_suite<container_t, ref_index_suite<container_t> >
  {
  public:

    typedef typename container_t::value_type data_type;
    typedef typename container_t::size_type  index_type;
    typedef typename container_t::size_type  size_type;
    typedef typename container_t::iterator   iterator;

    // Element access and manipulation.

    /// @brief Get element from container_t.
    static data_type& get_item(container_t& container, index_type index)
    {
      return *(container.begin() + index);
    }

    /// @brief Set element from container.
    static void set_item(container_t& container, index_type index, const data_type& value)
    {
      *(container.begin() + index) = value;
    }

    /// @brief Reset index to default value.
    static void delete_item(container_t& container, index_type index)
    {
      set_item(container, index, data_type());
    };


    //!@name Slice support.
    //!@{

    //! @brief Get slice from container.
    //! @return Python object containing the elements within the indexes
    static boost::python::object get_slice(container_t& container, index_type from, index_type to)
    {
      using boost::python::list;
      if (from > to) return list();

      // Return copy, as container only references its elements.
      list l;
      iterator it(container.begin() + from);
      while (from != to)
      {
        l.append(*it++);
        from++;
      }
      return l;
    };

    //! @brief Set a slice in container with a given value.
    static void set_slice(container_t& container, index_type from, index_type to, const data_type& value)
    {
      // If range is invalid, return early.
      if (from > to) return;

      // Populate range with value.
      iterator it(container.begin() + from);
      while (from < to)
      {
        *it++ = value;
        from++;
      }
    }

    //! @brief Set a slice in container with another range.
    template <class Iterator>
    static void set_slice(container_t& container, index_type from, index_type to, Iterator first, Iterator last)
    {
      // If range is invalid, return early.
      if (from > to) return;

      // Populate range with other range.
      while (from < to) container[from++] = *first++;   
    }

    //! @brief Reset slice to default values.
    static void delete_slice(container_t& container, index_type from, index_type to)
    {
      set_slice(container, from, to, data_type());
    }
    
    //!@}

    //!@name Capacity
    //!@{

    //! @brief Get size of container.
    static std::size_t size(container_t const& container)
    {
      return container.size();
    }

    //! @brief Check if a value is within the container.
    template <class T>
    static bool contains(container_t const& container, const T& value)
    {
      return std::find(container.begin(), container.end(), value) != container.end();
    }

    //! @brief Minimum index supported for container.
    static index_type get_min_index(container_t const& /*container*/)
    {
      return 0;
    }

    //! @brief Maximum index supported for container.
    static index_type get_max_index(container_t const& container)
    {
      return container.size();
    }
    
    static bool compare_index(container_t const& /*container*/, index_type a, index_type b)
    {
      return a < b;
    }


    //!@}

    // Misc.

    /// @brief Convert python index (could be negative) to a valid container
    ///        index with proper boundary checks.
    static index_type convert_index(container_t& container, PyObject* object)
    {
      namespace python = boost::python;
      python::extract<long> py_index(object);

      // If py_index cannot extract a long, then type the type is wrong so
      // set error and return early.
      if (!py_index.check()) 
      {
        PyErr_SetString(PyExc_TypeError, "Invalid index type");
        python::throw_error_already_set(); 
        return index_type();
      }

      // Extract index.
      long index = py_index();

      // Adjust negative index.
      if (index < 0)
          index += container.size();

      // Boundary check.
      if (index >= long(container.size()) || index < 0)
      {
        PyErr_SetString(PyExc_IndexError, "Index out of range");
        python::throw_error_already_set();
      }

      return index;
    }

  };



  //! @brief Conditionally register a type with Boost.Python.
  template <typename iterator_t>
  void register_array_proxy()
  {
    typedef array_proxy<iterator_t> proxy_type;

    // If type is already registered, then return early.
    namespace python = boost::python;
    bool is_registered = (0 != python::converter::registry::query(python::type_id<proxy_type>())->to_python_target_type());
    if (is_registered) return;

    // Otherwise, register the type as an internal type.
    std::string type_name = std::string("_ImageSliceProxy") + typeid(iterator_t).name();
    python::class_<proxy_type>(type_name.c_str(), python::no_init)
      .def(ref_index_suite<proxy_type>())
      ;
  }

  /*!@brief Create a callable Boost.Python object that will return an
   *        array_proxy type when called.
   *
   * @note This function will conditionally register array_proxy types
   *       for conversion within Boost.Python.  The array_proxy will
   *       extend the life of the object from which it was called.
   *       For example, if `foo` is an object, and `vars` is an array,
   *       then the object returned from `foo.vars` will extend the life
   *       of `foo`.
   */
  template <typename image_t>
  boost::python::object make_array_aux(image_t& image)
  {
    // Register an array proxy.
    register_array_proxy<typename image_t::iterator>();

    array_proxy<typename image_t::iterator> proxy(image.begin_block(), image.end_block());
    return boost::python::object(proxy);
  }

} // namespace array_details


template <enum yayi::type::e_compound_type C, enum yayi::type::e_scalar_type S>
boost::python::object make_array_from_image_stage3(yayi::IImage *input_image)
{
  using namespace yayi;
  typedef typename from_type<C, S>::type image_pixel_t;
  switch(input_image->GetDimension())
  {
  case 2:
  {
    typedef Image<image_pixel_t, s_coordinate<2> > image_t;
    image_t * image = dynamic_cast<image_t*>(input_image);
    if(!image)
      break;
    return array_details::make_array_aux(*image);
  }
  default:
    break;
  }
  
  return boost::python::object();

}

template <enum yayi::type::e_compound_type C>
boost::python::object make_array_from_image_stage2(yayi::IImage *input_image)
{
  using yayi::type;
  switch(input_image->DynamicType().s_type)
  {
  case type::s_ui8:
    return make_array_from_image_stage3<C, type::s_ui8>(input_image);
  case type::s_ui16:
    return make_array_from_image_stage3<C, type::s_ui16>(input_image);
  case type::s_ui32:
    return make_array_from_image_stage3<C, type::s_ui32>(input_image);
  
  case type::s_i8:
    return make_array_from_image_stage3<C, type::s_i8>(input_image);
  case type::s_i16:
    return make_array_from_image_stage3<C, type::s_i16>(input_image);
  case type::s_i32:
    return make_array_from_image_stage3<C, type::s_i32>(input_image);
  
  default:
    return boost::python::object();
  }

}

boost::python::object make_array_from_image(yayi::IImage *input_image)
{
  using yayi::type;
  if(!input_image)
    return boost::python::object();
  
  switch(input_image->DynamicType().c_type)
  {
  case type::c_scalar:
    return make_array_from_image_stage2<type::c_scalar>(input_image);
  case type::c_3:
    return make_array_from_image_stage2<type::c_3>(input_image);
  default:
    return boost::python::object();
  }
}




void declare_image() {

  using namespace yayi;
  
  typedef IImage::pixel_reference_type (IImage::*pixel_non_const)(const IImage::coordinate_type&);
  typedef IImage::iterator (IImage::*iterator_non_const)();
  
  bpy::class_<IImage, bpy::bases<IObject>, boost::noncopyable >("Image", "Main image class", bpy::no_init)
    // size
    .add_property("Size",       &IImage::GetSize, &IImage::SetSize)
    .add_property("ColorSpace", &IImage::GetColorSpace, &IImage::SetColorSpace)
    .def("SetSize",             &IImage::SetSize,             "(dimension): sets the size of the image to the tuple 'dimension'")
    .def("GetSize",             &IImage::GetSize,             "returns the size of the image as a tuple")
    .def("GetDimension",        &IImage::GetDimension,        "returns the dimension of the support of the image")
    .def("GetColorSpace",       &IImage::GetColorSpace,       "returns the colour space of the image")
    .def("SetColorSpace",       &IImage::SetColorSpace,       "(colorspace): sets the colour space of the image")
    
    // allocation
    .def("IsAllocated",       &IImage::IsAllocated,        "returns true if the image is allocated")
    .def("AllocateImage",     &IImage::AllocateImage,      "allocates the image with the specified size")
    .def("FreeImage",         &IImage::FreeImage,          "free the content of the image (the size remains unchanged)")
    
    // pixel
    .def("pixel",
         &pixel_method_wrapper,        
         "(coordinate): returns a reference to a pixel", 
         bpy::return_value_policy<bpy::manage_new_object, bpy::with_custodian_and_ward_postcall<0, 1> >())
  
    // native iterators
    .add_property("pixels",
      bpy::make_function(
        &yayi::image_range,
        bpy::with_custodian_and_ward_postcall<0,1>()
      ),
      "returns an iterator on the pixels")

    // slice
    .add_property("slice",
      bpy::make_function(
        &make_array_from_image,
        bpy::with_custodian_and_ward_postcall<0, 1>()
      ),
      "returns a slice of the image")
    
    // utilities
    //.def(bpy::self == bpy::other<IImage>())
    //.def(bpy::self != bpy::other<IImage>())    
    
  ;

  bpy::def("ImageFactory", 
    &IImage::Create, 
    bpy::args("type", "dimension"),
    "returns a new image of the given type and dimension",
    bpy::return_value_policy<bpy::manage_new_object>());
  
  bpy::def("GetSameImage", 
    (IImage* (*)(const IImage* const &im))&GetSameImage, 
    bpy::args("image"),
    "returns a new image of the same type and dimension as the input image (does not copy the pixels). Performs also the allocation "
    "if the argument image is allocated",
    bpy::return_value_policy<bpy::manage_new_object>());

  bpy::def("GetSameImageOf", 
    (IImage* (*)(const IImage* const &im, const yayi::type& t))&GetSameImage, 
    bpy::args("image", "type"),
    "behaves as 'GetSameImage', but the type of the returned image corresponds to the one specified as argument",
    bpy::return_value_policy<bpy::manage_new_object>());



}

