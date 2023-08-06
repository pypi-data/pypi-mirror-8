


set(YayiSegmentationSubdirectory ${YAYI_CORE_DIR}/yayiSegmentation)

set(YayiSegmentationSRC
  ${YayiSegmentationSubdirectory}/yayiSegmentation.hpp

  #${YayiSegmentationSubdirectory}/include/local_flooding_constraints_t.hpp
  #${YayiSegmentationSubdirectory}/include/viscous_watershed_T.hpp
  #${YayiSegmentationSubdirectory}/src/viscous_watershed.cpp

  ${YayiSegmentationSubdirectory}/include/isotropic_watershed_t.hpp
  ${YayiSegmentationSubdirectory}/src/isotropic_watershed.cpp
)


add_library(YayiSegmentation ${YayiSegmentationSRC})
target_include_directories(YayiSegmentation
                           PRIVATE ${YayiSegmentationSubdirectory}
                           PRIVATE ${YayiSegmentationSubdirectory}/include 
                           PRIVATE ${YayiSegmentationSubdirectory}/src)
target_link_libraries(YayiSegmentation YayiCommon YayiImageCore)
set_target_properties(YayiSegmentation PROPERTIES 
                      DEFINE_SYMBOL "YAYI_EXPORT_SEGMENTATION_"
                      FOLDER "Core/")

install_yayi_targets(
  TARGET YayiSegmentation 
  CONFIGURATION Release 
  HEADER_FILES ${YayiSegmentationSRC})                        




set(yayiSegmentationTestsSubdirectory ${YAYI_CORE_TEST_DIR}/yayiSegmentationTests)
set(yayiSegmentationTestsSRC
  ${yayiSegmentationTestsSubdirectory}/main.hpp
  ${yayiSegmentationTestsSubdirectory}/main.cpp

  ${yayiSegmentationTestsSubdirectory}/isotropic_watershed_test.cpp
)
add_executable(YayiSegmentationTests ${yayiSegmentationTestsSRC})
target_link_libraries(YayiSegmentationTests YayiSegmentation YayiStructuringElement ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY})
add_test(NAME yayiSegmentationTests-1 
         COMMAND YayiSegmentationTests)
set_property(TARGET YayiSegmentationTests PROPERTY FOLDER "UnitTests/")
test_environment_setup(yayiSegmentationTests-1)




set(YayiSegmentationPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiSegmentationPython)
set(YayiSegmentationPythonSRC
  ${YayiSegmentationPythonSubdirectory}/segmentation_python.hpp
  ${YayiSegmentationPythonSubdirectory}/segmentation_python.cpp
  ${YayiSegmentationPythonSubdirectory}/watershed.cpp
)

add_python_library(YayiSegmentationPython "${YayiSegmentationPythonSRC}" "YayiSegmentation")
target_include_directories(YayiSegmentationPython
                           PRIVATE ${YayiSegmentationPythonSubdirectory}/include)
add_to_python_packaging(YayiSegmentationPython)

add_test(NAME yayiSegmentationTestsPython-1 COMMAND ${PYTHON_EXECUTABLE} ${YayiSegmentationPythonSubdirectory}/segmentation_python.py $<TARGET_FILE_DIR:YayiSegmentationPython>)
test_environment_setup(yayiSegmentationTestsPython-1)

