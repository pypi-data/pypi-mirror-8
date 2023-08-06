

set(YayiLabelSubdirectory ${YAYI_CORE_DIR}/yayiLabel)

set(YayiLabelSRC
  ${YayiLabelSubdirectory}/yayi_Label.hpp

  ${YayiLabelSubdirectory}/include/yayi_label_t.hpp
  ${YayiLabelSubdirectory}/src/yayi_label_simple.cpp

  ${YayiLabelSubdirectory}/yayi_label_extrema.hpp
  ${YayiLabelSubdirectory}/include/yayi_label_extrema_t.hpp
  ${YayiLabelSubdirectory}/src/yayi_label_extrema.cpp

  ${YayiLabelSubdirectory}/yayi_label_binary_with_measure.hpp
  ${YayiLabelSubdirectory}/include/yayi_label_binary_with_measure_t.hpp
  ${YayiLabelSubdirectory}/src/yayi_label_binary_with_measures.cpp

  ${YayiLabelSubdirectory}/include/yayi_label_with_adjacency_graph_t.hpp
  ${YayiLabelSubdirectory}/src/yayi_label_with_adjacency_graph.cpp
)

add_library(YayiLabel ${YayiLabelSRC})
target_include_directories(YayiLabel 
                           PRIVATE ${YayiLabelSubdirectory}
                           PRIVATE ${YayiLabelSubdirectory}/include
                           PRIVATE ${YayiLabelSubdirectory}/src)

target_link_libraries(YayiLabel YayiImageCore YayiCommon)
set_target_properties(YayiLabel 
                      PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_LABEL_"
                                 FOLDER "Core/")

install_yayi_targets(
  TARGET YayiLabel 
  CONFIGURATION Release 
  HEADER_FILES ${YayiLabelSRC})





set(yayiLabelTestsSubdirectory ${YAYI_CORE_TEST_DIR}/yayiLabelTests)
set(yayiLabelTestsSRC
  ${yayiLabelTestsSubdirectory}/main.hpp
  ${yayiLabelTestsSubdirectory}/main.cpp
  ${yayiLabelTestsSubdirectory}/label_image_test.cpp
  ${yayiLabelTestsSubdirectory}/label_extrema_test.cpp
)

add_executable(YayiLabelTests ${yayiLabelTestsSRC})
target_include_directories(YayiLabelTests PRIVATE ${yayiLabelTestsSubdirectory})
target_link_libraries(YayiLabelTests YayiLabel YayiStructuringElement ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY})
add_test(NAME yayiLabelTests-1 
         COMMAND YayiLabelTests)
set_property(TARGET YayiLabelTests PROPERTY FOLDER "UnitTests/")
test_environment_setup(yayiLabelTests-1)


set(YayiLabelPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiLabelPython)
set(YayiLabelPythonSRC
  ${YayiLabelPythonSubdirectory}/label_python.cpp
  ${YayiLabelPythonSubdirectory}/label_python.hpp

  ${YayiLabelPythonSubdirectory}/label_basic.cpp
  ${YayiLabelPythonSubdirectory}/label_extrema.cpp
)

add_python_library(YayiLabelPython "${YayiLabelPythonSRC}" "YayiLabel")
target_include_directories(YayiLabelPython 
                           PRIVATE ${YayiLabelPythonSubdirectory})
add_to_python_packaging(YayiLabelPython)

add_test(NAME yayiLabelTestsPython-1 
         COMMAND ${PYTHON_EXECUTABLE} ${YayiLabelPythonSubdirectory}/label_python.py $<TARGET_FILE_DIR:YayiLabelPython>)
test_environment_setup(yayiLabelTestsPython-1)
