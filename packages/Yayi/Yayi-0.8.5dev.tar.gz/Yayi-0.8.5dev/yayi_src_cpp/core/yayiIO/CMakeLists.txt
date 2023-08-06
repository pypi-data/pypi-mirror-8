



set(YayiIOSubdirectory ${YAYI_CORE_DIR}/yayiIO)

set(YayiIOSRC
  ${YayiIOSubdirectory}/include/yayi_IO.hpp

  ${YayiIOSubdirectory}/src/IO_raw.cpp
  ${YayiIOSubdirectory}/src/IO_jpg.cpp
  ${YayiIOSubdirectory}/src/IO_png.cpp
  ${YayiIOSubdirectory}/src/IO_tiff.cpp
  ${YayiIOSubdirectory}/src/O_eps.cpp
  ${YayiIOSubdirectory}/src/IO_HDF5.cpp
)


add_library(YayiIO ${YayiIOSRC})
target_include_directories(YayiIO 
                           PRIVATE ${YayiIOSubdirectory}
                           PRIVATE ${YayiIOSubdirectory}/include
                           PRIVATE ${YayiIOSubdirectory}/src
                           PRIVATE ${PNG_LIB_SRC}
                           PRIVATE ${ZLIB_SRC_DIR}
                           PRIVATE ${JPEG_LIB_SRC}
                           PRIVATE ${TIFF_LIB_SRC})

target_link_libraries(YayiIO 
                      LINK_PUBLIC YayiImageCore YayiCommon 
                      LINK_PRIVATE ${JPEG} ${PNG} ${TIFF})

set_target_properties(YayiIO 
                      PROPERTIES  DEFINE_SYMBOL "YAYI_EXPORT_IO_"
                                  COMPILE_FLAGS "${PNG_DEFS}"
                                  FOLDER "Core/")


if(ENABLE_HDF5)
  message(STATUS "Linking YayiIO to HDF5 ---- " ${HDF5LIBL} ${HDF5LIBB})
  target_compile_definitions(YayiIO PRIVATE -DYAYI_IO_HDF5_ENABLED__)
  target_include_directories(YayiIO PRIVATE ${HDF5_INCLUDE_DIRS})
  target_link_libraries(YayiIO ${HDF5LIBL} ${HDF5LIBB})
endif()


install_yayi_targets(
  TARGET YayiIO 
  CONFIGURATION Release 
  HEADER_FILES ${YayiIOSRC})



set(yayiIOTestsSubdirectory ${YAYI_CORE_TEST_DIR}/yayiIOTests)
set(yayiIOTestsSRC
  ${yayiIOTestsSubdirectory}/io_raw_tests.cpp
  ${yayiIOTestsSubdirectory}/io_jpeg_tests.cpp
  ${yayiIOTestsSubdirectory}/io_png_tests.cpp
  ${yayiIOTestsSubdirectory}/io_tiff_tests.cpp
  ${yayiIOTestsSubdirectory}/io_hdf5_tests.cpp

  ${yayiIOTestsSubdirectory}/main.cpp
  ${yayiIOTestsSubdirectory}/main.hpp
)

add_executable(YayiIOTests ${yayiIOTestsSRC})
target_link_libraries(YayiIOTests YayiIO YayiImageCore YayiCommon 
                      ${Boost_SYSTEM_LIBRARY} 
                      ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY} 
                      ${Boost_FILESYSTEM_LIBRARY})
set_property(TARGET YayiIOTests PROPERTY FOLDER "UnitTests/")

add_test(NAME yayiIOTests-1 
         COMMAND YayiIOTests)
test_environment_setup(yayiIOTests-1)






set(YayiIOPythonSubdirectory ${YAYI_PYTHONEXT_DIR}/yayiIOPython)
set(YayiIOPythonSRC
 ${YayiIOPythonSubdirectory}/io_python.hpp
 ${YayiIOPythonSubdirectory}/io_python.cpp

 ${YayiIOPythonSubdirectory}/io_python_jpg.cpp
 ${YayiIOPythonSubdirectory}/io_python_png.cpp
 ${YayiIOPythonSubdirectory}/io_python_raw.cpp
 ${YayiIOPythonSubdirectory}/io_python_tiff.cpp
 ${YayiIOPythonSubdirectory}/io_python_hdf5.cpp
 ${YayiIOPythonSubdirectory}/io_python_numpy.cpp
)

add_python_library(YayiIOPython "${YayiIOPythonSRC}" "YayiIO")
target_include_directories(YayiIOPython 
                           PRIVATE ${YayiIOPythonSubdirectory}/include)

if(ENABLE_NUMPY)
  target_compile_definitions(YayiIOPython PRIVATE -DYAYI_IO_NUMPY_ENABLED__)
  target_include_directories(YayiIOPython PRIVATE ${NUMPY_INCLUDE_PATH})
endif()

add_to_python_packaging(YayiIOPython)

set(ADD_HDF5 "")
if(ENABLE_HDF5)
  set(ADD_HDF5 "HDF5")
endif()

set(ADD_NUMPY "")
if(ENABLE_NUMPY)
  set(ADD_NUMPY "NUMPY")
endif()

add_test(NAME yayiIOTestsPython-1 
         COMMAND ${PYTHON_EXECUTABLE} ${YayiIOPythonSubdirectory}/io_python.py $<TARGET_FILE_DIR:YayiIOPython> ${ADD_HDF5} ${ADD_NUMPY})
test_environment_setup(yayiIOTestsPython-1)
