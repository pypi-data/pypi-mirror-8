

#include <yayiStructuringElement/yayiStructuringElement.hpp>


namespace yayi { namespace se {
  
  IConstNeighborhood* NeighborListCreate(const IImage& im, const IStructuringElement& se);

  
  IConstNeighborhood* IConstNeighborhood::Create(const IImage& im, const IStructuringElement& se) {
  
    switch(se.GetType()) {
    
    case e_set_neighborlist:
      return NeighborListCreate(im, se);
    
    default:
      YAYI_THROW("Undefined se type requested");
      return 0;
    }
  
  }


}}
