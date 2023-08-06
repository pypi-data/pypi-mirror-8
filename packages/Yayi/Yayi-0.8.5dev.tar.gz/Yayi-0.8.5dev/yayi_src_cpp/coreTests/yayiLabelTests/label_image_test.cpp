#include "main.hpp"

#include <yayiLabel/include/yayi_label_t.hpp>
#include <yayiLabel/include/yayi_label_with_adjacency_graph_t.hpp>
#include <yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <yayiCommon/include/common_graph.hpp>



BOOST_AUTO_TEST_CASE(label_simple) 
{
  using namespace yayi;
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_test_lab, im_out_lab;
  image_type* p_im[] = {&im_in, &im_test_lab, &im_out_lab};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE_EQUAL(p_im[i]->SetSize(coord), yaRC_ok);
    BOOST_REQUIRE_EQUAL(p_im[i]->AllocateImage(), yaRC_ok);
  }
  
  // input image
  {
    static const std::string s = 
      "1 2 3 2 "
      "1 1 3 2 "
      "1 3 3 2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // theoretical label image
  {
    static const std::string s = 
      "1 2 3 4 "
      "1 1 3 4 "
      "1 3 3 4 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_lab, "Error during the input streaming of the image");
  }

  
  yaRC res = label::image_label_t(im_in, se::SESquare2D, im_out_lab);
  BOOST_REQUIRE(res == yaRC_ok);
  
  // check des sorties
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out_lab.pixel(i) == im_test_lab.pixel(i), "Label error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_lab.pixel(i) << " != " << (int)im_test_lab.pixel(i));
  }
  
  
}

BOOST_AUTO_TEST_CASE(label_with_graph) 
{
  using namespace yayi;
  typedef Image<yaUINT8> image_type;
  
  image_type im_in, im_test_lab, im_out_lab;
  image_type* p_im[] = {&im_in, &im_test_lab, &im_out_lab};
  image_type::coordinate_type coord;
  coord[0] = 4; coord[1] = 3;
  
  for(unsigned int i = 0; i < sizeof(p_im) / sizeof(p_im[0]); i++) {
    BOOST_REQUIRE_EQUAL(p_im[i]->SetSize(coord), yaRC_ok);
    BOOST_REQUIRE_EQUAL(p_im[i]->AllocateImage(), yaRC_ok);
  }
  
  // input image
  {
    static const std::string s = 
      "1 2 3 2 "
      "1 1 3 2 "
      "1 3 3 2 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_in, "Error during the input streaming of the image");
  }

  // theoretical label image
  {
    static const std::string s = 
      "1 2 3 4 "
      "1 1 3 4 "
      "1 3 3 4 "
    ;
    std::istringstream is(s);

    BOOST_CHECK_MESSAGE(is >> im_test_lab, "Error during the input streaming of the image");
  }

  s_graph<yaUINT16> graph;

  BOOST_REQUIRE_EQUAL(label::image_label_with_adjacency_graph_t(im_in, se::SESquare2D, im_out_lab, graph), yaRC_ok);
  
  // check des sorties
  for(offset i = 0, j = total_number_of_points(coord); i < j; i++) {
    BOOST_CHECK_MESSAGE(im_out_lab.pixel(i) == im_test_lab.pixel(i), "Label error on pixel " << i << " position " << from_offset_to_coordinate(coord, i) << "\n\tresult != test : " << (int)im_out_lab.pixel(i) << " != " << (int)im_test_lab.pixel(i));
  }

  std::stringstream s;
  
  BOOST_CHECKPOINT("write graph");
  write_graph(s, graph, "label", "weight");
  
  std::cout << s.str() << std::endl;

  std::stringstream ss;
  write_graph(ss, graph.remove_parallel_edges(), "label", "weight");
  std::cout << ss.str() << std::endl;

  BOOST_CHECK_MESSAGE(graph.are_vertices_adjacent(0, 1), "Error: vertices 0 and 1 (connected components 1 and 2) are not adjacent");
  BOOST_CHECK_MESSAGE(graph.are_vertices_adjacent(2, 0), "Error: vertices 2 and 0 (connected components 3 and 1) are not adjacent");
  BOOST_CHECK_MESSAGE(graph.are_vertices_adjacent(3, 2), "Error: vertices 3 and 2 (connected components 4 and 3) are not adjacent");
  BOOST_CHECK_MESSAGE(graph.are_vertices_adjacent(2, 1), "Error: vertices 2 and 1 (connected components 3 and 2) are not adjacent");
  
  //s_graph<yaUINT32> graph32;
  //read_graph(ss, graph32);
}



