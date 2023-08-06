
# This module contains the structuring element definitions in Yayi.


set(yayiStructuringElementSubdirectory ${YAYI_CORE_DIR}/yayiStructuringElement)



# 
# Main module
#
set(YayiSESRC
  ${yayiStructuringElementSubdirectory}/yayiStructuringElement.hpp
  ${yayiStructuringElementSubdirectory}/src/yayiStructuringElement.cpp
  ${yayiStructuringElementSubdirectory}/src/yayiStructuringElementFactory.cpp
  ${yayiStructuringElementSubdirectory}/src/yayiStructuringElementNeighborListFactory.cpp

  ${yayiStructuringElementSubdirectory}/yayiStructuringElementChain.hpp

  ${yayiStructuringElementSubdirectory}/include/yayiRuntimeNeighborhood_t.hpp
  ${yayiStructuringElementSubdirectory}/include/yayiRuntimeStructuringElement_t.hpp
  ${yayiStructuringElementSubdirectory}/include/yayiRuntimeStructuringElement_hexagon_t.hpp
  ${yayiStructuringElementSubdirectory}/include/yayiStructuringElement_t.hpp
  ${yayiStructuringElementSubdirectory}/include/yayiNeighborhoodStrategy_t.hpp

  ${yayiStructuringElementSubdirectory}/include/yayiDisjointPairedStructuringElement_t.hpp

  ${yayiStructuringElementSubdirectory}/yayiRuntimeStructuringElements_predefined.hpp
  ${yayiStructuringElementSubdirectory}/src/yayiStructuringElements_predefined.cpp

  ${yayiStructuringElementSubdirectory}/include/se_dispatcher.hpp
  ${yayiStructuringElementSubdirectory}/include/yayiStructuringElementUtilities_t.hpp

)


add_library(YayiStructuringElement ${YayiSESRC})
target_include_directories(YayiStructuringElement
                           PRIVATE ${yayiStructuringElementSubdirectory}
                           PRIVATE ${yayiStructuringElementSubdirectory}/include)
target_link_libraries(YayiStructuringElement YayiImageCore YayiCommon)
set_target_properties(YayiStructuringElement PROPERTIES 
                      DEFINE_SYMBOL "YAYI_EXPORT_SE_"
                      FOLDER "Core/")
                        
install_yayi_targets(
  TARGET YayiStructuringElement 
  CONFIGURATION Release 
  HEADER_FILES ${YayiSESRC})



# 
# Unit tests
#
set(yayiStructuringElementTestsSubdirectory ${YAYI_CORE_TEST_DIR}/yayiStructuringElementTests)
set(yayiSETestsSRC
  ${yayiStructuringElementTestsSubdirectory}/iterator_covering.cpp
  ${yayiStructuringElementTestsSubdirectory}/se_tests_basic.cpp
  ${yayiStructuringElementTestsSubdirectory}/se_runtime_tests.cpp
  ${yayiStructuringElementTestsSubdirectory}/se_neighborhood_runtime_tests.cpp
  ${yayiStructuringElementTestsSubdirectory}/neigh_factory.cpp

  ${yayiStructuringElementTestsSubdirectory}/main.cpp
  ${yayiStructuringElementTestsSubdirectory}/main.hpp
)

add_executable(YayiStructuringElementTests ${yayiSETestsSRC})
target_link_libraries(YayiStructuringElementTests 
                      YayiStructuringElement 
                      YayiIO
                      ${Boost_SYSTEM_LIBRARY} ${Boost_FILESYSTEM_LIBRARY} ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY})
add_test(NAME yayiStructuringElementTests-1 
         COMMAND YayiStructuringElementTests)
set_target_properties(YayiStructuringElementTests PROPERTIES FOLDER "UnitTests/")
test_environment_setup(yayiStructuringElementTests-1)


# 
# Python extensions
#
set(yayiStructuringElementSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiStructuringElementPython)
set(yayiStructuringElementPythonSRC
 ${yayiStructuringElementSubdirectory}/structuringelement_python.hpp
 ${yayiStructuringElementSubdirectory}/structuringelement_python.cpp
 ${yayiStructuringElementSubdirectory}/structuring_element_declares.cpp
 ${yayiStructuringElementSubdirectory}/structuring_element_neighborhoods.cpp
 ${yayiStructuringElementSubdirectory}/structuring_element_predefined.cpp
)
add_python_library(YayiStructuringElementPython "${yayiStructuringElementPythonSRC}" "YayiStructuringElement")
target_include_directories(YayiStructuringElementPython PRIVATE ${yayiStructuringElementSubdirectory}/include)

add_to_python_packaging(YayiStructuringElementPython)

# python unit tests
add_test( NAME yayiStructuringElementTestsPython-1 
          COMMAND ${PYTHON_EXECUTABLE} ${yayiStructuringElementSubdirectory}/structuringelements_python.py $<TARGET_FILE_DIR:YayiStructuringElementPython>)
test_environment_setup(yayiStructuringElementTestsPython-1)
