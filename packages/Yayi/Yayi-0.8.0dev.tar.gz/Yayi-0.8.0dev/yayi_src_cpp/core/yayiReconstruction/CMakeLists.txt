



# main library
set(YayiReconstructionSubdirectory ${YAYI_CORE_DIR}/yayiReconstruction)

set(YayiReconstructionSRC
  ${YayiReconstructionSubdirectory}/yayiReconstruction.hpp

  ${YayiReconstructionSubdirectory}/morphological_reconstruction.hpp
  ${YayiReconstructionSubdirectory}/include/morphological_reconstruction_t.hpp
  ${YayiReconstructionSubdirectory}/src/morphological_reconstruction.cpp

  ${YayiReconstructionSubdirectory}/morphological_fill_holes.hpp
  ${YayiReconstructionSubdirectory}/include/morphological_fill_holes_t.hpp
  ${YayiReconstructionSubdirectory}/src/morphological_fill_holes.cpp

  ${YayiReconstructionSubdirectory}/morphological_leveling.hpp
  ${YayiReconstructionSubdirectory}/include/morphological_leveling_t.hpp
  ${YayiReconstructionSubdirectory}/src/morphological_leveling.cpp

  ${YayiReconstructionSubdirectory}/highlevel_minima_maxima.hpp
  ${YayiReconstructionSubdirectory}/include/highlevel_minima_maxima_t.hpp
  ${YayiReconstructionSubdirectory}/src/highlevel_minima_maxima.cpp



)


add_library(YayiReconstruction ${YayiReconstructionSRC})
target_include_directories(YayiReconstruction
                           PRIVATE ${YayiReconstructionSubdirectory}
                           PRIVATE ${YayiReconstructionSubdirectory}/include)
target_link_libraries(YayiReconstruction YayiImageCore YayiCommon)
set_target_properties(YayiReconstruction PROPERTIES 
                      DEFINE_SYMBOL "YAYI_EXPORT_REC_"
                      FOLDER "Core/")
install_yayi_targets(
  TARGET YayiReconstruction 
  CONFIGURATION Release 
  HEADER_FILES ${YayiReconstructionSRC})                        


# Test project
set(yayiReconstructionTestsSubdirectory ${YAYI_CORE_TEST_DIR}/yayiReconstructionTests)
set(yayiReconstructionTestsSRC
  ${yayiReconstructionTestsSubdirectory}/main.cpp
  ${yayiReconstructionTestsSubdirectory}/main.hpp

  ${yayiReconstructionTestsSubdirectory}/reconstruction_test.cpp
  ${yayiReconstructionTestsSubdirectory}/fill_hole_test.cpp
  ${yayiReconstructionTestsSubdirectory}/leveling_test.cpp
  ${yayiReconstructionTestsSubdirectory}/highlevel_minima_maxima_tests.cpp
)
add_executable(YayiReconstructionTests ${yayiReconstructionTestsSRC})
target_include_directories(YayiReconstructionTests PRIVATE ${yayiReconstructionTestsSubdirectory})
target_link_libraries(YayiReconstructionTests YayiReconstruction YayiStructuringElement ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY})
add_test(NAME yayiReconstructionTests-1 
         COMMAND YayiReconstructionTests)
set_property(TARGET YayiReconstructionTests PROPERTY FOLDER "UnitTests/")
test_environment_setup(yayiReconstructionTests-1)

# Python project
set(yayiReconstructionPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiReconstructionPython)
set(yayiReconstructionPythonSRC
 ${yayiReconstructionPythonSubdirectory}/reconstruction_python.hpp
 ${yayiReconstructionPythonSubdirectory}/reconstruction_python.cpp

 ${yayiReconstructionPythonSubdirectory}/morphological_reconstructions.cpp
 ${yayiReconstructionPythonSubdirectory}/fill_holes.cpp
 ${yayiReconstructionPythonSubdirectory}/highlevelmm_minima_maxima.cpp

)

add_python_library(YayiReconstructionPython "${yayiReconstructionPythonSRC}" "YayiReconstruction")
target_include_directories(YayiReconstructionPython
                           PRIVATE ${yayiReconstructionPythonSubdirectory}/include)
add_to_python_packaging(YayiReconstructionPython)

add_test(NAME yayiReconstructionTestsPython-1 
         COMMAND ${PYTHON_EXECUTABLE} ${yayiReconstructionPythonSubdirectory}/reconstruction_python.py $<TARGET_FILE_DIR:YayiReconstructionPython>)
test_environment_setup(yayiReconstructionTestsPython-1)
