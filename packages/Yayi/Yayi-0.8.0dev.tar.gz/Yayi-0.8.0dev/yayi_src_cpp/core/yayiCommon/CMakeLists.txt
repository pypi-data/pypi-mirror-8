

set(YayiCommonSubdirectory ${YAYI_CORE_DIR}/yayiCommon)

generate_library_version(${YayiCommonSubdirectory}/src/current_configuration_generated.cpp)

set(YayiCommonSRC
  ${YayiCommonSubdirectory}/yayiCommon.hpp

  ${YayiCommonSubdirectory}/common_config.hpp
  ${YayiCommonSubdirectory}/common_coordinates.hpp
  ${YayiCommonSubdirectory}/common_coordinates_operations_t.hpp
  ${YayiCommonSubdirectory}/include/common_coordinates_mpl_utils_t.hpp
  ${YayiCommonSubdirectory}/common_hyperrectangle.hpp
  ${YayiCommonSubdirectory}/common_errors.hpp
  ${YayiCommonSubdirectory}/common_histogram.hpp
  ${YayiCommonSubdirectory}/common_pixels.hpp
  ${YayiCommonSubdirectory}/common_pixels_T.hpp
  ${YayiCommonSubdirectory}/common_types.hpp
  ${YayiCommonSubdirectory}/common_priority_queues.hpp
  ${YayiCommonSubdirectory}/common_variant.hpp
  ${YayiCommonSubdirectory}/common_constants.hpp
  ${YayiCommonSubdirectory}/common_labels.hpp
  ${YayiCommonSubdirectory}/common_colorspace.hpp
  ${YayiCommonSubdirectory}/common_orders.hpp

  # matrices (to be moved into ${YayiCommonSubdirectory})
  ${YayiCommonSubdirectory}/include/common_matrix_t.hpp
  ${YayiCommonSubdirectory}/include/common_matrix_inversion_t.hpp

  ${YayiCommonSubdirectory}/include/common_dispatch.hpp
  ${YayiCommonSubdirectory}/include/common_graph.hpp
  ${YayiCommonSubdirectory}/include/common_graphDispatch.hpp
  ${YayiCommonSubdirectory}/include/common_object.hpp
  ${YayiCommonSubdirectory}/include/common_string_utilities.hpp
  ${YayiCommonSubdirectory}/include/common_types_T.hpp
  ${YayiCommonSubdirectory}/include/current_configuration.hpp
  ${YayiCommonSubdirectory}/include/common_variantDispatch.hpp
  ${YayiCommonSubdirectory}/include/common_time.hpp
  ${YayiCommonSubdirectory}/include/common_tree.hpp
  ${YayiCommonSubdirectory}/include/common_tree_Impl.hpp
  ${YayiCommonSubdirectory}/include/thread_pool.hpp

  ${YayiCommonSubdirectory}/src/common_error.cpp
  ${YayiCommonSubdirectory}/src/common_types.cpp
  ${YayiCommonSubdirectory}/src/common_colorspace.cpp
  ${YayiCommonSubdirectory}/src/current_configuration.cpp
  ${YayiCommonSubdirectory}/src/thread_pool.cpp

  # auto generated file
  ${YayiCommonSubdirectory}/src/current_configuration_generated.cpp
)



add_library(YayiCommon ${YayiCommonSRC})
target_include_directories(YayiCommon 
                           PRIVATE ${YayiCommonSubdirectory}
                           PRIVATE ${YayiCommonSubdirectory}/include
                           PRIVATE ${YayiCommonSubdirectory}/src)
#target_compile_options(YayiCommon PRIVATE "-fvisibility=hidden")
#target_compile_options(YayiCommon PRIVATE "-fvisibility-inlines-hidden")
#        set_target_properties(YayiCommon
#          PROPERTIES 
#            LINK_FLAGS "${_previous_link_flags} -Wl,--exclude-libs,ALL"
#        )
        

#create_pch_headers("YayiCommon" "${YayiCommonSRC}" "")
target_link_libraries(YayiCommon 
                      PRIVATE ${Boost_GRAPH_LIBRARY} 
                      PRIVATE ${Boost_DATE_TIME_LIBRARY} 
                      PRIVATE ${Boost_REGEX_LIBRARY} 
                      PRIVATE ${Boost_THREAD_LIBRARY} 
                      PRIVATE ${Boost_SYSTEM_LIBRARY})
set_target_properties(YayiCommon PROPERTIES 
                      DEFINE_SYMBOL "YAYI_EXPORT_COMMON_"
                      FOLDER "Core/")
install_yayi_targets(
  TARGET YayiCommon 
  CONFIGURATION Release 
  HEADER_FILES ${YayiCommonSRC})




# Test project
set(YayiCommonTestSubdirectory ${YAYI_CORE_TEST_DIR}/yayiCommonCoreTests)
set(YayiCommonTestSRC
  ${YayiCommonTestSubdirectory}/build_date.cpp
  ${YayiCommonTestSubdirectory}/coordinates.cpp
  ${YayiCommonTestSubdirectory}/dispatch_tests.cpp
  ${YayiCommonTestSubdirectory}/main.cpp
  ${YayiCommonTestSubdirectory}/main.hpp
  ${YayiCommonTestSubdirectory}/types_and_variant_tests.cpp
  ${YayiCommonTestSubdirectory}/priority_queues.cpp
  ${YayiCommonTestSubdirectory}/graphs.cpp
  ${YayiCommonTestSubdirectory}/histograms.cpp
  ${YayiCommonTestSubdirectory}/trees.cpp
  ${YayiCommonTestSubdirectory}/matrices_tests.cpp
  ${YayiCommonTestSubdirectory}/color_space.cpp
  ${YayiCommonTestSubdirectory}/thread_pool_test.cpp
)
add_executable(YayiCommonTests ${YayiCommonTestSRC})
target_link_libraries(YayiCommonTests YayiCommon ${Boost_GRAPH_LIBRARY} ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY})
add_test(NAME yayiCommonTests-1 
         COMMAND YayiCommonTests)
set_property(TARGET YayiCommonTests PROPERTY FOLDER "UnitTests/")
test_environment_setup(yayiCommonTests-1)

# Python project
set(YayiCommonPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiCommonPython)
set(YayiCommonPythonSRC
  ${YayiCommonPythonSubdirectory}/common_python.hpp
  ${YayiCommonPythonSubdirectory}/common_python.cpp

  ${YayiCommonPythonSubdirectory}/common_utils.cpp
  ${YayiCommonPythonSubdirectory}/common_enums.cpp
  ${YayiCommonPythonSubdirectory}/common_variant.cpp
  ${YayiCommonPythonSubdirectory}/common_error.cpp
  ${YayiCommonPythonSubdirectory}/common_object.cpp
  ${YayiCommonPythonSubdirectory}/common_coordinate.cpp
  ${YayiCommonPythonSubdirectory}/common_returncode.cpp
  ${YayiCommonPythonSubdirectory}/common_graph.cpp
  ${YayiCommonPythonSubdirectory}/common_colorspace.cpp
)


add_python_library(YayiCommonPython "${YayiCommonPythonSRC}" "YayiCommon")
target_include_directories(YayiCommonPython 
                           PRIVATE ${YayiCommonPythonSubdirectory}/include)
add_to_python_packaging(YayiCommonPython)

#target_compile_options(YayiCommonPython PRIVATE "-fvisibility=hidden")
#target_compile_options(YayiCommonPython PRIVATE "-s")
#target_compile_options(YayiCommonPython PRIVATE "-fvisibility-inlines-hidden")

#      #get_target_property(
#      #  _previous_link_flags 
#      #  YayiCommonPython
#      #  LINK_FLAGS)
#set_target_properties(YayiCommonPython
#          PROPERTIES 
#            LINK_FLAGS "-Wl,-exported_symbol,_initYayiCommonPython"
#        )

add_test(NAME yayiCommonTestsPython-1 
         COMMAND ${PYTHON_EXECUTABLE} ${YayiCommonPythonSubdirectory}/common_test.py $<TARGET_FILE_DIR:YayiCommonPython>)
test_environment_setup(yayiCommonTestsPython-1)

