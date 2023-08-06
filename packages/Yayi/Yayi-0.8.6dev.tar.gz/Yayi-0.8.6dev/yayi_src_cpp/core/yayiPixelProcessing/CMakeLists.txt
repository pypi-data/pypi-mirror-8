


# main library
set(YayiPixelProcessingSubdirectory ${YAYI_CORE_DIR}/yayiPixelProcessing)

set(YayiPixelProcessingSRC
  ${YayiPixelProcessingSubdirectory}/yayiPixelProcessing.hpp

  # utilities
  ${YayiPixelProcessingSubdirectory}/image_constant.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_constant_T.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_constant.cpp

  # copy
  ${YayiPixelProcessingSubdirectory}/image_copy.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_copy_T.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_copy.cpp
  ${YayiPixelProcessingSubdirectory}/src/image_copy_windowed.cpp

  # channels
  ${YayiPixelProcessingSubdirectory}/image_channels_process.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_channels_process_T.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_channels_process.cpp

  # color
  ${YayiPixelProcessingSubdirectory}/image_color_process.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_color_process_hls_T.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_color_process_hls.cpp

  ${YayiPixelProcessingSubdirectory}/include/image_color_process_luma_t.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_color_process_luma.cpp

  ${YayiPixelProcessingSubdirectory}/include/image_color_process_yuv_t.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_color_process_yuv.cpp

  ${YayiPixelProcessingSubdirectory}/include/image_color_process_xyz_t.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_color_process_xyz.cpp

  ${YayiPixelProcessingSubdirectory}/include/image_color_process_lab_t.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_color_process_lab.cpp

  #${YayiPixelProcessingSubdirectory}/include/image_color_process_cmyk_t.hpp


  # compare
  ${YayiPixelProcessingSubdirectory}/image_compare.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_compare_T.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_compare.cpp
  ${YayiPixelProcessingSubdirectory}/src/image_compare_1.cpp

  # arithmetics
  ${YayiPixelProcessingSubdirectory}/image_arithmetics.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_arithmetics_t.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_arithmetics.cpp

  # logics
  ${YayiPixelProcessingSubdirectory}/image_logics.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_logics_t.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_logics.cpp

  # mathematical
  ${YayiPixelProcessingSubdirectory}/image_math.hpp
  ${YayiPixelProcessingSubdirectory}/include/image_math_t.hpp
  ${YayiPixelProcessingSubdirectory}/src/image_math.cpp

  #borders
  ${YayiPixelProcessingSubdirectory}/include/image_borders_t.hpp
)

add_library(YayiPixelProcessing ${YayiPixelProcessingSRC})
target_include_directories(YayiPixelProcessing 
                           PRIVATE ${YayiPixelProcessingSubdirectory}
                           PRIVATE ${YayiPixelProcessingSubdirectory}/include)
target_link_libraries(YayiPixelProcessing YayiImageCore YayiCommon)
set_target_properties(YayiPixelProcessing 
                      PROPERTIES 
                        DEFINE_SYMBOL "YAYI_EXPORT_PIXELPROC_"
                        FOLDER "Core/")
                        
install_yayi_targets(
  TARGET YayiPixelProcessing 
  CONFIGURATION Release 
  HEADER_FILES ${YayiPixelProcessingSRC})                        





# Test project
set(yayiPixelProcessingTestsSubdirectory ${YAYI_CORE_TEST_DIR}/yayiPixelProcessingTests)
set(yayiPixelProcessingTestsSRC
  ${yayiPixelProcessingTestsSubdirectory}/simple_functions_through_interfaces.cpp
  ${yayiPixelProcessingTestsSubdirectory}/binary_operators_tests.cpp
  ${yayiPixelProcessingTestsSubdirectory}/border_tests.cpp
  ${yayiPixelProcessingTestsSubdirectory}/copy_test.cpp
  #${yayiPixelProcessingTestsSubdirectory}/arith_tests.cpp

  ${yayiPixelProcessingTestsSubdirectory}/main.cpp
  ${yayiPixelProcessingTestsSubdirectory}/main.hpp
)

add_executable(YayiPixelProcessingTests ${yayiPixelProcessingTestsSRC})
target_include_directories(YayiPixelProcessingTests PRIVATE ${yayiPixelProcessingTestsSubdirectory})
target_link_libraries(YayiPixelProcessingTests YayiPixelProcessing ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY})
add_test(NAME yayiPixelProcessingTests-1 
         COMMAND YayiPixelProcessingTests)
set_property(TARGET YayiPixelProcessingTests PROPERTY FOLDER "UnitTests/")
test_environment_setup(yayiPixelProcessingTests-1)

# Python project
set(yayiPixelProcessingPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiPixelProcessingPython)
set(yayiPixelProcessingPythonSRC
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_python.hpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_python.cpp

 ${yayiPixelProcessingPythonSubdirectory}/pixel_processing_channel_color.cpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_unary_pointwise.cpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_compare.cpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_arithmetic.cpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_logic.cpp
 ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_math.cpp
)

add_python_library(YayiPixelProcessingPython "${yayiPixelProcessingPythonSRC}" "YayiPixelProcessing")
target_include_directories(YayiPixelProcessingPython
                           PRIVATE ${yayiPixelProcessingPythonSubdirectory}/include)
add_to_python_packaging(YayiPixelProcessingPython)

add_test(NAME yayiPixelProcessingTestsPython-1 COMMAND ${PYTHON_EXECUTABLE} ${yayiPixelProcessingPythonSubdirectory}/pixelprocessing_python.py $<TARGET_FILE_DIR:YayiPixelProcessingPython>)
test_environment_setup(yayiPixelProcessingTestsPython-1)

