

set(YayiLLMSubdirectory ${YAYI_CORE_DIR}/yayiLowLevelMorphology)
set(YayiLLMMSRC
  ${YayiLLMSubdirectory}/yayiLowLevelMorphology.hpp

  ${YayiLLMSubdirectory}/include/lowlevel_neighborhoodProcessing_t.hpp
  ${YayiLLMSubdirectory}/include/lowlevel_neighbor_operators_t.hpp
  ${YayiLLMSubdirectory}/include/neighbor_operators_traits_t.hpp

  ${YayiLLMSubdirectory}/lowlevel_erosion_dilation.hpp
  ${YayiLLMSubdirectory}/include/lowlevel_erosion_dilation_t.hpp
  ${YayiLLMSubdirectory}/src/lowlevel_erosion_dilation.cpp

  ${YayiLLMSubdirectory}/lowlevel_morpho_gradient.hpp
  ${YayiLLMSubdirectory}/include/lowlevel_morpho_gradient_t.hpp
  ${YayiLLMSubdirectory}/src/lowlevel_gradient.cpp

  ${YayiLLMSubdirectory}/lowlevel_opening_closing.hpp
  ${YayiLLMSubdirectory}/include/lowlevel_opening_closing_t.hpp
  ${YayiLLMSubdirectory}/src/lowlevel_opening_closing.cpp

  ${YayiLLMSubdirectory}/lowlevel_geodesic.hpp
  ${YayiLLMSubdirectory}/include/lowlevel_geodesic_t.hpp
  ${YayiLLMSubdirectory}/src/lowlevel_geodesic.cpp

  ${YayiLLMSubdirectory}/include/lowlevel_hit_or_miss_t.hpp
  ${YayiLLMSubdirectory}/lowlevel_hit_or_miss.hpp
  ${YayiLLMSubdirectory}/src/lowlevel_hit_or_miss.cpp

  ${YayiLLMSubdirectory}/highlevel_alternate.hpp
  ${YayiLLMSubdirectory}/include/highlevel_alternate_t.hpp
  ${YayiLLMSubdirectory}/src/highlevel_alternate.cpp

  ${YayiLLMSubdirectory}/include/lowlevel_attribute_t.hpp
)


add_library(YayiLowlevelMorphology ${YayiLLMMSRC})
target_include_directories(YayiLowlevelMorphology 
                           PRIVATE ${YayiLLMSubdirectory}
                           PRIVATE ${YayiLLMSubdirectory}/include)
target_link_libraries(YayiLowlevelMorphology 
                      YayiIO YayiStructuringElement YayiPixelProcessing YayiImageCore YayiCommon)
set_target_properties(YayiLowlevelMorphology 
                      PROPERTIES 
                        DEFINE_SYMBOL "YAYI_EXPORT_LLMM_"
                        FOLDER "Core/")
install_yayi_targets(
  TARGET YayiLowlevelMorphology 
  CONFIGURATION Release 
  HEADER_FILES ${YayiLLMMSRC})




# Test project
set(yayiLowLevelMorphologyTestsSubdirectory ${YAYI_CORE_TEST_DIR}/yayiLowlevelMorphologyTests)
set(yayiLowLevelMorphologyTestsSRC
  ${yayiLowLevelMorphologyTestsSubdirectory}/simple_operators_interface_tests.cpp
  ${yayiLowLevelMorphologyTestsSubdirectory}/erosion_dilation_test.cpp
  ${yayiLowLevelMorphologyTestsSubdirectory}/hit_or_miss_test.cpp
  ${yayiLowLevelMorphologyTestsSubdirectory}/highlevel_alternate_tests.cpp
  ${yayiLowLevelMorphologyTestsSubdirectory}/lowlevel_attribute_tests.cpp

  ${yayiLowLevelMorphologyTestsSubdirectory}/main.cpp
  ${yayiLowLevelMorphologyTestsSubdirectory}/main.hpp
)
add_executable(YayiLowLevelMorphologyTests ${yayiLowLevelMorphologyTestsSRC})
target_link_libraries(YayiLowLevelMorphologyTests 
  YayiLowlevelMorphology 
  YayiIO YayiStructuringElement 
  YayiPixelProcessing 
  YayiImageCore 
  YayiCommon
  ${Boost_DATE_TIME_LIBRARY} ${Boost_FILESYSTEM_LIBRARY} ${Boost_SYSTEM_LIBRARY} ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY} )
add_test(NAME yayiLowLevelMorphologyTests-1 
         COMMAND YayiLowLevelMorphologyTests)
set_property(TARGET YayiLowLevelMorphologyTests PROPERTY FOLDER "UnitTests/")
test_environment_setup(yayiLowLevelMorphologyTests-1)



# Python project
set(yayiLowLevelMorphologyPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiLowLevelMorphologyPython)
set(yayiLowLevelMorphologyPythonPythonSRC
  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_python.hpp
  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_python.cpp

  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_rank.cpp
  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_gradient.cpp
  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_geodesic.cpp
  ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevelmm_hit_or_miss.cpp
  ${yayiLowLevelMorphologyPythonSubdirectory}/highlevelmm_alternate.cpp
)


add_python_library(YayiLowLevelMorphologyPython "${yayiLowLevelMorphologyPythonPythonSRC}" "YayiLowlevelMorphology")
add_to_python_packaging(YayiLowLevelMorphologyPython)

add_test(
  NAME yayiLowLevelMorphologyTestsPython-1 
  COMMAND ${PYTHON_EXECUTABLE} ${yayiLowLevelMorphologyPythonSubdirectory}/lowlevel_morphology_test.py $<TARGET_FILE_DIR:YayiLowLevelMorphologyPython>
)
test_environment_setup(yayiLowLevelMorphologyTestsPython-1)
