



# main library
set(YayiNeighborhoodProcessingSubdirectory ${YAYI_CORE_DIR}/yayiNeighborhoodProcessing)

set(YayiNeighborhoodProcessingSRC
  ${YayiNeighborhoodProcessingSubdirectory}/yayiNeighborhoodProcessing.hpp
  ${YayiNeighborhoodProcessingSubdirectory}/include/np_operators_adapters_t.hpp

  ${YayiNeighborhoodProcessingSubdirectory}/np_local_statistics.hpp
  ${YayiNeighborhoodProcessingSubdirectory}/include/np_local_statistics_t.hpp
  ${YayiNeighborhoodProcessingSubdirectory}/src/np_local_statistics.cpp
)

add_library(YayiNeighborhoodProcessing ${YayiNeighborhoodProcessingSRC})
target_include_directories(YayiNeighborhoodProcessing 
                           PRIVATE ${YayiNeighborhoodProcessingSubdirectory}
                           PRIVATE ${YayiNeighborhoodProcessingSubdirectory}/include)

target_link_libraries(YayiNeighborhoodProcessing YayiImageCore YayiCommon)
set_target_properties(YayiNeighborhoodProcessing 
                      PROPERTIES 
                        DEFINE_SYMBOL "YAYI_EXPORT_NeighborhoodProcessing_"
                        FOLDER "Core/")
install_yayi_targets(
  TARGET YayiNeighborhoodProcessing 
  CONFIGURATION Release 
  HEADER_FILES ${YayiNeighborhoodProcessingSRC})



# Test project
set(yayiNeighborhoodProcessingTestsSubdirectory ${YAYI_CORE_TEST_DIR}/yayiNeighborhoodProcessingTests)
set(yayiNeighborhoodProcessingTestsSRC
  ${yayiNeighborhoodProcessingTestsSubdirectory}/main.cpp
  ${yayiNeighborhoodProcessingTestsSubdirectory}/main.hpp

  ${yayiNeighborhoodProcessingTestsSubdirectory}/np_test_mean.cpp
)
include_directories(${yayiNeighborhoodProcessingTestsSubdirectory})
add_executable(YayiNeighborhoodProcessingTests ${yayiNeighborhoodProcessingTestsSRC})
target_link_libraries(YayiNeighborhoodProcessingTests YayiNeighborhoodProcessing YayiStructuringElement ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY})
add_test(NAME yayiNeighborhoodProcessingTests-1 
         COMMAND YayiNeighborhoodProcessingTests)
set_property(TARGET YayiNeighborhoodProcessingTests PROPERTY FOLDER "UnitTests/")
test_environment_setup(yayiNeighborhoodProcessingTests-1)

# Python project
set(yayiNeighborhoodProcessingPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiNeighborhoodProcessingPython)
set(yayiNeighborhoodProcessingPythonSRC
 ${yayiNeighborhoodProcessingPythonSubdirectory}/neighborhoodprocessing_python.hpp
 ${yayiNeighborhoodProcessingPythonSubdirectory}/neighborhoodprocessing_python.cpp

 ${yayiNeighborhoodProcessingPythonSubdirectory}/neighbor_statistics.cpp
)



add_python_library(YayiNeighborhoodProcessingPython "${yayiNeighborhoodProcessingPythonSRC}" "YayiNeighborhoodProcessing")
target_include_directories(YayiNeighborhoodProcessingPython
                           PRIVATE ${yayiNeighborhoodProcessingPythonSubdirectory}/include)
add_to_python_packaging(YayiNeighborhoodProcessingPython)

add_test(NAME yayiNeighborhoodProcessingTestsPython-1
         COMMAND ${PYTHON_EXECUTABLE} ${yayiNeighborhoodProcessingPythonSubdirectory}/neighborhoodprocessing_python.py $<TARGET_FILE_DIR:YayiNeighborhoodProcessingPython>)
test_environment_setup(yayiNeighborhoodProcessingTestsPython-1)
