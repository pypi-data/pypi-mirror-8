
#include <yayiStructuringElement/yayiStructuringElement.hpp>
#include <yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>

namespace yayi { namespace se {

  template <int dim>
  IStructuringElement * NeighborlistFactoryHelper(const variant& shape_element, structuring_element_subtype se_sub_t)
  {
    typedef s_coordinate<dim> coordinate_type;
    std::vector<typename coordinate_type::scalar_coordinate_type> coordinates_as_continuous_list;
    
    try
    {
      coordinates_as_continuous_list = shape_element;
    }
    catch(errors::yaException & DEBUG_ONLY_VARIABLE(e))
    {

      std::vector< coordinate_type > coordinates_as_packed_vectors;

      try
      {
        coordinates_as_packed_vectors = shape_element;
      }
      catch(errors::yaException & DEBUG_ONLY_VARIABLE(ee))
      {
        DEBUG_INFO("Caught exception while trying to extract the shape element: " << e.what() << " and also " << ee.what());
        return 0;
      }
      
      coordinates_as_continuous_list.clear();
      for(size_t i = 0; i < coordinates_as_packed_vectors.size(); i++)
      {
        for(int j = 0; j < dim; j++) coordinates_as_continuous_list.push_back(coordinates_as_packed_vectors[i][j]);
      }

    }
    
    switch(se_sub_t)
    {
    case e_sest_neighborlist_generic_single:
      return new s_neighborlist_se< coordinate_type >(coordinates_as_continuous_list);
    case e_sest_neighborlist_hexa:
      return new s_neighborlist_se_hexa_x< coordinate_type >(coordinates_as_continuous_list);
    default:
      DEBUG_INFO("Unsupported subtype of structuring element");
      return 0;    
    }
  }


  IStructuringElement * IStructuringElement::Create(
    structuring_element_type se_t, 
    yaUINT8 dimension, 
    const variant& shape_element,
    structuring_element_subtype se_sub_t/*= e_sest_neighborlist_generic_single*/)
  {
  
    switch(se_t)
    {
    case e_set_neighborlist:
    {
      switch(dimension)
      {
      case 2: return NeighborlistFactoryHelper<2>(shape_element, se_sub_t);
      case 3: return NeighborlistFactoryHelper<3>(shape_element, se_sub_t);
      case 4: return NeighborlistFactoryHelper<4>(shape_element, se_sub_t);
      default:
        DEBUG_INFO("Unsupported dimension of structuring element");
        return 0;
      }
    }
    
    default:
      DEBUG_INFO("Unsupported type of structuring element");
      return 0;
    }
  }
  
  
  template <int dimension>
  std::vector< s_coordinate<dimension> > ball_create_helper(const double metric, const double radius)
  {
    typedef s_coordinate<dimension> coordinate_type;
    coordinate_type const center(static_cast<typename coordinate_type::scalar_coordinate_type>(std::ceil(radius)));
    coordinate_type const size(2*center[0]);
    
    std::vector< coordinate_type > out;
    
    // ballade sur un hypercube de dimension "dimension"
    for(offset o = 0, o_end = total_number_of_points(size); o < o_end; o++)
    {
      coordinate_type current = from_offset_to_coordinate(size, o) - center;
      double dist(0);
      for(int i = 0; i < dimension; i++)
      {
        dist += std::pow(std::abs(current[i]), metric);
      }
      dist = std::pow(dist, 1./metric);
      if(dist <= radius)
        out.push_back(current);
      
    } 
    
    return out;
  
  }
  
  
  IStructuringElement * CreateBallSE(yaUINT8 dimension, const yaUINT8 metric, const double radius)
  {  
    variant v;
    switch(dimension)
    {
    case 2: v = ball_create_helper<2>(metric, radius); break;
    case 3: v = ball_create_helper<3>(metric, radius); break;
    case 4: v = ball_create_helper<4>(metric, radius); break;
    
    default:
      DEBUG_INFO("Unsupported dimension of structuring element");
      return 0;
    }

    return IStructuringElement::Create(e_set_neighborlist, dimension, v, e_sest_neighborlist_generic_single);
  }
}}

