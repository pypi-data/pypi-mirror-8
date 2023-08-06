

set(YayiImageCoreSubdirectory ${YAYI_CORE_DIR}/yayiImageCore)

set(YayiImageCoreSRC
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_T.hpp
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_zeroary_t.hpp
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_unary_t.hpp
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_binary_t.hpp
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_ternary_t.hpp
  ${YayiImageCoreSubdirectory}/include/ApplyToImage_fourary_t.hpp
  ${YayiImageCoreSubdirectory}/include/yayiImageOperatorClassification_t.hpp

  ${YayiImageCoreSubdirectory}/include/yayiImageAllocators_T.hpp
  ${YayiImageCoreSubdirectory}/include/yayiImageIterator.hpp
  ${YayiImageCoreSubdirectory}/include/yayiImageUtilities_T.hpp

  ${YayiImageCoreSubdirectory}/include/yayiImageCore.hpp
  ${YayiImageCoreSubdirectory}/include/yayiImageCore_Impl.hpp
  ${YayiImageCoreSubdirectory}/include/yayiImageCore_ImplDispatch.hpp
  ${YayiImageCoreSubdirectory}/src/yayiImageCore.cpp

  ${YayiImageCoreSubdirectory}/yayiImageCoreFunctions.hpp
  ${YayiImageCoreSubdirectory}/src/yayiGetSame.cpp
)


add_library(YayiImageCore ${YayiImageCoreSRC})
target_include_directories(YayiImageCore 
                           PRIVATE ${YayiImageCoreSubdirectory}
                           PRIVATE ${YayiImageCoreSubdirectory}/include
                           PRIVATE ${YayiImageCoreSubdirectory}/src)

target_link_libraries(YayiImageCore YayiCommon)
set_target_properties(YayiImageCore 
      PROPERTIES 
        DEFINE_SYMBOL "YAYI_EXPORT_CORE_"
        FOLDER "Core/")

install_yayi_targets(
  TARGET YayiImageCore 
  CONFIGURATION Release 
  HEADER_FILES ${YayiImageCoreSRC})





# unit tests
set(yayiImageCoreTestsSubdirectory ${YAYI_CORE_TEST_DIR}/yayiImageCoreTests)
set(yayiImageCoreTestsSRC
  ${yayiImageCoreTestsSubdirectory}/image_access.cpp
  ${yayiImageCoreTestsSubdirectory}/image_creation.cpp
  ${yayiImageCoreTestsSubdirectory}/image_utilities.cpp
  ${yayiImageCoreTestsSubdirectory}/image_apply_tests.cpp
  ${yayiImageCoreTestsSubdirectory}/image_iterators.cpp
  ${yayiImageCoreTestsSubdirectory}/image_threaded_apply_tests.cpp
  ${yayiImageCoreTestsSubdirectory}/image_operator_classification_tests.cpp
  ${yayiImageCoreTestsSubdirectory}/main.cpp
  ${yayiImageCoreTestsSubdirectory}/main.hpp
)
add_executable(YayiImageCoreTests ${yayiImageCoreTestsSRC})
target_link_libraries(YayiImageCoreTests YayiImageCore ${Boost_THREAD_LIBRARY} ${Boost_SYSTEM_LIBRARY} ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY})
add_test(NAME yayiImageCoreTests-1 
          COMMAND YayiImageCoreTests)
set_property(TARGET YayiImageCoreTests PROPERTY FOLDER "UnitTests/")
test_environment_setup(yayiImageCoreTests-1)

# benches
set(yayiImageCoreBenchesDirectory ${YAYI_CORE_TEST_DIR}/yayiImageCoreBenches)
set(yayiImageCoreBenchesSRC
  ${yayiImageCoreBenchesDirectory}/main.cpp
)
add_executable(YayiImageCoreBenches ${yayiImageCoreBenchesSRC})
target_link_libraries(YayiImageCoreBenches YayiImageCore 
                      ${Boost_DATE_TIME_LIBRARY} 
                      ${Boost_THREAD_LIBRARY} 
                      ${Boost_SYSTEM_LIBRARY} 
                      ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY})
add_test(NAME yayiImageCoreBenches-1 
          CONFIGURATIONS Release
          COMMAND YayiImageCoreBenches)
set_tests_properties(yayiImageCoreBenches-1 PROPERTIES RUN_SERIAL TRUE)
set_property(TARGET YayiImageCoreBenches PROPERTY FOLDER "Benches/")
test_environment_setup(yayiImageCoreBenches-1)


set(YayiImageCorePythonSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiImageCorePython)
set(YayiImageCorePythonSRC
 ${YayiImageCorePythonSubdirectory}/imagecore_python.hpp
 ${YayiImageCorePythonSubdirectory}/imagecore_python.cpp

 ${YayiImageCorePythonSubdirectory}/imagecore_image.cpp
 ${YayiImageCorePythonSubdirectory}/imagecore_iterator.cpp
 ${YayiImageCorePythonSubdirectory}/imagecore_interfacepixel.cpp
 ${YayiImageCorePythonSubdirectory}/imagecore_utilities.cpp
)


add_python_library(YayiImageCorePython "${YayiImageCorePythonSRC}" "YayiImageCore")
target_include_directories(YayiImageCorePython
                           PRIVATE ${YayiImageCorePythonSubdirectory}/include)

add_dependencies(YayiImageCorePython YayiCommonPython)
add_to_python_packaging(YayiImageCorePython)

add_test(NAME yayiImageCoreTestsPython-1
         COMMAND ${PYTHON_EXECUTABLE} ${YayiImageCorePythonSubdirectory}/imagecore_python.py $<TARGET_FILE_DIR:YayiImageCorePython>)
test_environment_setup(yayiImageCoreTestsPython-1)



