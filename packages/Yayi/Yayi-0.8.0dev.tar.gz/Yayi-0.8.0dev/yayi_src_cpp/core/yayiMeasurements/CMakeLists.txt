

set(YayiMeasurementsSubdirectory ${YAYI_CORE_DIR}/yayiMeasurements)

set(YayiMeasurementsSRC
  ${YayiMeasurementsSubdirectory}/yayiMeasurements.hpp
  ${YayiMeasurementsSubdirectory}/include/measurements_t.hpp

  ${YayiMeasurementsSubdirectory}/measurements_min_max.hpp
  ${YayiMeasurementsSubdirectory}/include/measurements_min_max_t.hpp
  ${YayiMeasurementsSubdirectory}/src/measurements_min_max.cpp

  ${YayiMeasurementsSubdirectory}/measurements_histogram.hpp
  ${YayiMeasurementsSubdirectory}/include/measurements_histogram_t.hpp
  ${YayiMeasurementsSubdirectory}/src/measurements_histogram.cpp

  ${YayiMeasurementsSubdirectory}/measurements_mean_variance.hpp
  ${YayiMeasurementsSubdirectory}/include/measurements_mean_variance_t.hpp
  ${YayiMeasurementsSubdirectory}/src/measurements_mean_variance.cpp

  ${YayiMeasurementsSubdirectory}/measurements_quantiles.hpp
  ${YayiMeasurementsSubdirectory}/include/measurements_quantiles_t.hpp
  ${YayiMeasurementsSubdirectory}/src/measurements_quantiles.cpp
)


add_library(YayiMeasurements ${YayiMeasurementsSRC})
target_include_directories(YayiMeasurements 
                           PRIVATE ${YayiMeasurementsSubdirectory}
                           PRIVATE ${YayiMeasurementsSubdirectory}/include
                           PRIVATE ${YayiMeasurementsSubdirectory}/src)
target_link_libraries(YayiMeasurements YayiImageCore YayiCommon)
set_target_properties(YayiMeasurements 
                      PROPERTIES DEFINE_SYMBOL "YAYI_EXPORT_MEASUREMENTS_"
                                 FOLDER "Core/")

install_yayi_targets(
  TARGET YayiMeasurements 
  CONFIGURATION Release 
  HEADER_FILES ${YayiMeasurementsSRC})



set(yayiMeasurementsTestsSubdirectory ${YAYI_CORE_TEST_DIR}/yayiMeasurementsTests)
set(yayiMeasurementsTestsSRC
  ${yayiMeasurementsTestsSubdirectory}/main.hpp
  ${yayiMeasurementsTestsSubdirectory}/main.cpp

  ${yayiMeasurementsTestsSubdirectory}/min_max_test.cpp
)
add_executable(YayiMeasurementsTests ${yayiMeasurementsTestsSRC})
target_link_libraries(YayiMeasurementsTests YayiCommon YayiImageCore ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY})
add_test(NAME yayiMeasurementsTests-1 
         COMMAND YayiMeasurementsTests)
set_property(TARGET YayiMeasurementsTests PROPERTY FOLDER "UnitTests/")
test_environment_setup(yayiMeasurementsTests-1)




set(YayiMeasurementsPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiMeasurementsPython)
set(YayiMeasurementsPythonSRC
  ${YayiMeasurementsPythonSubdirectory}/measurements_python.hpp
  ${YayiMeasurementsPythonSubdirectory}/measurements_python.cpp

  ${YayiMeasurementsPythonSubdirectory}/measurements_min_max.cpp
  ${YayiMeasurementsPythonSubdirectory}/measurements_histograms.cpp
  ${YayiMeasurementsPythonSubdirectory}/measurements_statistics.cpp
)

add_python_library(YayiMeasurementsPython "${YayiMeasurementsPythonSRC}" "YayiMeasurements")
target_include_directories(YayiMeasurementsPython 
                           PRIVATE ${YayiMeasurementsPythonSubdirectory}/include)
add_to_python_packaging(YayiMeasurementsPython)

add_test(NAME yayiMeasurementsTestsPython-1 
         COMMAND ${PYTHON_EXECUTABLE} ${YayiMeasurementsPythonSubdirectory}/measurements_python.py $<TARGET_FILE_DIR:YayiMeasurementsPython>)
test_environment_setup(yayiMeasurementsTestsPython-1)

