

set(YayiDistancesSubdirectory ${YAYI_CORE_DIR}/yayiDistances)

set(YayiDistancesSRC
  ${YayiDistancesSubdirectory}/yayiDistances.hpp
  ${YayiDistancesSubdirectory}/quasi_distance.hpp

  ${YayiDistancesSubdirectory}/include/quasi_distance_T.hpp
  ${YayiDistancesSubdirectory}/src/quasi_distance.cpp

  #${YayiDistancesSubdirectory}/include/exact_distances_t.hpp
  #${YayiDistancesSubdirectory}/include/distance_operations_t.hpp

  ${YayiDistancesSubdirectory}/include/color_distances_t.hpp

  ${YayiDistancesSubdirectory}/include/morphological_distance_t.hpp
  ${YayiDistancesSubdirectory}/morphological_distance.hpp
  ${YayiDistancesSubdirectory}/src/morphological_distance.cpp

)

add_library(YayiDistances ${YayiDistancesSRC})
target_include_directories(YayiDistances 
                           PRIVATE ${YayiDistancesSubdirectory}
                           PRIVATE ${YayiDistancesSubdirectory}/include
                           PRIVATE ${YayiDistancesSubdirectory}/src)
target_link_libraries(YayiDistances YayiCommon YayiIO)
set_target_properties(YayiDistances 
                      PROPERTIES 
                        DEFINE_SYMBOL "YAYI_EXPORT_DISTANCES_"
                        FOLDER "Core/")
install_yayi_targets(
  TARGET YayiDistances 
  CONFIGURATION Release 
  HEADER_FILES ${YayiDistancesSRC})


set(yayiDistancesTestsSubdirectory ${YAYI_CORE_TEST_DIR}/yayiDistancesTests)
set(yayiDistancesTestsSRC
  ${yayiDistancesTestsSubdirectory}/main.hpp
  ${yayiDistancesTestsSubdirectory}/main.cpp

  ${yayiDistancesTestsSubdirectory}/quasi_distance_test.cpp
  ${yayiDistancesTestsSubdirectory}/morpho_distance_tests.cpp
  ${yayiDistancesTestsSubdirectory}/exact_distance_tests.cpp
)

if(${CMAKE_HOST_UNIX})
  # to copy from boost directory at "libs/random/random_device.cpp"
  if(EXISTS ${yayiDistancesTestsSubdirectory}/random_device.cpp)
    add_definitions(-DYAYI_REAL_RANDOM_EXISTS__)
    set(yayiDistancesTestsSRC ${yayiDistancesTestsSRC} ${yayiDistancesTestsSubdirectory}/random_device.cpp)
  endif()
endif(${CMAKE_HOST_UNIX})


add_executable(YayiDistancesTests ${yayiDistancesTestsSRC})
target_link_libraries(YayiDistancesTests YayiDistances YayiStructuringElement YayiIO 
                      ${Boost_DATE_TIME_LIBRARY}
                      ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY})
add_test(NAME yayiDistancesTests-1 
         COMMAND YayiDistancesTests)
set_property(TARGET YayiDistancesTests PROPERTY FOLDER "UnitTests/")
test_environment_setup(yayiDistancesTests-1)


set(YayiDistancesPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiDistancesPython)
set(YayiDistancesPythonSRC
  ${YayiDistancesPythonSubdirectory}/distances_python.hpp
  ${YayiDistancesPythonSubdirectory}/distances_python.cpp

  ${YayiDistancesPythonSubdirectory}/quasi_distance.cpp
  ${YayiDistancesPythonSubdirectory}/binary_distance.cpp
)


add_python_library(YayiDistancesPython "${YayiDistancesPythonSRC}" "YayiDistances")
target_include_directories(YayiDistancesPython 
                           PRIVATE ${YayiDistancesPythonSubdirectory}/include)
add_to_python_packaging(YayiDistancesPython)

add_test(NAME yayiDistancesTestsPython-1 
         COMMAND ${PYTHON_EXECUTABLE} ${YayiDistancesPythonSubdirectory}/distances_python.py $<TARGET_FILE_DIR:YayiDistancesPython>)
test_environment_setup(yayiDistancesTestsPython-1)
