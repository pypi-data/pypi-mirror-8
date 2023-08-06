


# this is the place where config files will be copied, if needed
set(config_folder ${CMAKE_BINARY_DIR}/configs)
file(MAKE_DIRECTORY ${config_folder})

set(debian_dependencies)


# Third parties builds
#include(select_library_configurations)
if(MSVC)
  # looking for appropriate paths
  if(CMAKE_CL_64)
    set_property(GLOBAL PROPERTY FIND_LIBRARY_USE_LIB64_PATHS ON)
  else()
    set_property(GLOBAL PROPERTY FIND_LIBRARY_USE_LIB64_PATHS OFF)
  endif()
endif()
set_property(GLOBAL PROPERTY thirdpartiesdependencies)


# --------------------------------------------------------------------------------
# boost


if(NOT BOOST_ROOT)
  message(STATUS "Boost root not configured, taking the system boost version")
  set(YAYI_BOOST_FROM_SYSTEM TRUE)
else()
  message(STATUS "Boost root directory set to ${BOOST_ROOT}")
  set(YAYI_BOOST_FROM_SYSTEM FALSE)
endif()

if(UNIX AND NOT APPLE AND NOT YAYI_BOOST_FROM_SYSTEM)
  message(WARNING "[YAYI Boost] you are setting a different boost than the one provided by the system. This option should be taken with care.")
endif()

set(Boost_ADDITIONAL_VERSIONS   
    "1.54" "1.54.0" "1.55" "1.55.0" "1.56" "1.56.0")
# use of the cmake special package

# disable auto link
add_definitions(-DBOOST_ALL_NO_LIB)
# linking with shared library version
set(Boost_USE_STATIC_LIBS OFF)
#set(Boost_USE_STATIC_LIBS   ON)

if(NOT Boost_USE_STATIC_LIBS)
  # link against dynamic libraries
  add_definitions(-DBOOST_ALL_DYN_LINK)
endif()

# if we are using the system version, we do not want to have the exact version embedded in the rpath/ldd
if(YAYI_BOOST_FROM_SYSTEM)
  set(Boost_REALPATH OFF)
else()
  set(Boost_REALPATH ON)
endif()

set(Boost_USE_MULTITHREADED ON)
set(Boost_DEBUG ON)
set(Boost_DETAILED_FAILURE_MSG ON)
if(DEFINED BOOST_ROOT)
  set(Boost_NO_SYSTEM_PATHS ON)
else()
  set(Boost_NO_SYSTEM_PATHS OFF)
endif()
set(Boost_NO_BOOST_CMAKE ON)

set(yayi_boost_version_minimal 1.54)

find_package(Boost ${yayi_boost_version_minimal}
             REQUIRED 
             COMPONENTS date_time filesystem system thread regex unit_test_framework python graph)
set(Boost_INCLUDE_DIRS ${Boost_INCLUDE_DIRS} PARENT_SCOPE)
set(Boost_LIBRARY_DIRS ${Boost_LIBRARY_DIRS} PARENT_SCOPE)
set(Boost_VERSION      ${Boost_VERSION}      PARENT_SCOPE)
# indicate to the build that we are using the system version (for packaging decisions)
set(YAYI_BOOST_FROM_SYSTEM ${YAYI_BOOST_FROM_SYSTEM} PARENT_SCOPE)

set(debian_dependencies ${debian_dependencies} 
                        "libboost-date-time-dev (>= ${yayi_boost_version_minimal})"
                        "libboost-filesystem-dev (>= ${yayi_boost_version_minimal})"
                        "libboost-system-dev (>= ${yayi_boost_version_minimal})"
                        "libboost-thread-dev (>= ${yayi_boost_version_minimal})"
                        "libboost-regex-dev (>= ${yayi_boost_version_minimal})"
                        "libboost-test-dev (>= ${yayi_boost_version_minimal})"
                        "libboost-python-dev (>= ${yayi_boost_version_minimal})"
                        "libboost-graph-dev (>= ${yayi_boost_version_minimal})")

set(BoostFilesToInstall
  ${Boost_PYTHON_LIBRARY_RELEASE}
  ${Boost_SYSTEM_LIBRARY_RELEASE}
  ${Boost_GRAPH_LIBRARY_RELEASE}
  ${Boost_REGEX_LIBRARY_RELEASE}
  ${Boost_DATE_TIME_LIBRARY_RELEASE}
  ${Boost_THREAD_LIBRARY_RELEASE}
  ${Boost_FILESYSTEM_LIBRARY_RELEASE}
  #${Boost_UNIT_TEST_FRAMEWORK_LIBRARY_RELEASE}
  )
set(BoostFilesToInstall ${BoostFilesToInstall} PARENT_SCOPE)

# to avoid a change in behaviour introduced between cmake 2.8.7 and 2.8.11
set(Boost_DATE_TIME_LIBRARY           ${Boost_DATE_TIME_LIBRARY}            PARENT_SCOPE)
set(Boost_FILESYSTEM_LIBRARY          ${Boost_FILESYSTEM_LIBRARY}           PARENT_SCOPE)
set(Boost_SYSTEM_LIBRARY              ${Boost_SYSTEM_LIBRARY}               PARENT_SCOPE)
set(Boost_THREAD_LIBRARY              ${Boost_THREAD_LIBRARY}               PARENT_SCOPE)
set(Boost_REGEX_LIBRARY               ${Boost_REGEX_LIBRARY}                PARENT_SCOPE)
set(Boost_UNIT_TEST_FRAMEWORK_LIBRARY ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY}  PARENT_SCOPE)
set(Boost_PYTHON_LIBRARY              ${Boost_PYTHON_LIBRARY}               PARENT_SCOPE)
set(Boost_GRAPH_LIBRARY               ${Boost_GRAPH_LIBRARY}                PARENT_SCOPE)

message(STATUS "Boost library found in " ${Boost_LIBRARY_DIRS})
message(STATUS "Boost major.minor.subminor=${Boost_MAJOR_VERSION}.${Boost_MINOR_VERSION}.${Boost_SUBMINOR_VERSION}")


# emit the installation command
if(NOT YAYI_BOOST_FROM_SYSTEM)
  install(FILES
    ${BoostFilesToInstall}
    CONFIGURATIONS Release
    DESTINATION lib
    COMPONENT core)

  #add_files_to_python_packaging(FILES ${BoostFilesToInstall})
endif()





# Python libraries

find_package(PythonLibs REQUIRED)
find_package(PythonInterp REQUIRED)
set(PYTHON_LIBRARIES ${PYTHON_LIBRARIES} PARENT_SCOPE)
set(PYTHON_INCLUDE_PATH  ${PYTHON_INCLUDE_PATH} PARENT_SCOPE)
set(PYTHON_EXECUTABLE    ${PYTHON_EXECUTABLE}  PARENT_SCOPE)

string(REPLACE "." ";" VERSION_LIST ${PYTHONLIBS_VERSION_STRING})
list(GET VERSION_LIST 0 PYTHONLIBS_VERSION_MAJOR)
list(GET VERSION_LIST 1 PYTHONLIBS_VERSION_MINOR)

# notes:
# the way boost.python was compiled should be verified (linking against the found python lib)
# the python interpreter should be verified against the python libs (a distribution mismatch might happen)
set(debian_dependencies ${debian_dependencies} "libpython-dev (>= ${PYTHONLIBS_VERSION_MAJOR}.${PYTHONLIBS_VERSION_MINOR})")
set(debian_dependencies ${debian_dependencies} "python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")



if(ENABLE_NUMPY)
  execute_process(
    COMMAND ${PYTHON_EXECUTABLE} -c "import numpy; print numpy.get_include()"
    OUTPUT_VARIABLE NUMPY_INCLUDE_PATH
    ERROR_VARIABLE  NUMPY_ERROR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    )
  if(NOT (NUMPY_ERROR STREQUAL "") OR (NUMPY_INCLUDE_PATH STREQUAL ""))
    message(FATAL_ERROR "[YAYIIO | NUMPY] the following error occured: ${NUMPY_ERROR} - Consider setting PYTHON_ROOT in the environment")
  endif()
  message(STATUS "[YAYIIO] Getting headers for Numpy from ${NUMPY_INCLUDE_PATH}")
  set(NUMPY_INCLUDE_PATH   ${NUMPY_INCLUDE_PATH}     PARENT_SCOPE)
  
  set(debian_dependencies ${debian_dependencies} "python-numpy (>= 1:1.8)")
  
endif()





# Lib JPEG
if(DO_NOT_USE_YAYI_JPEG)
  find_package(JPEG REQUIRED QUIET)
  message(STATUS "[YAYIIO] Jpeg library found in " ${JPEG_INCLUDE_DIR} ${JPEG_LIBRARIES})
  set(JPEG                ${JPEG_LIBRARIES}       PARENT_SCOPE)
  set(JPEG_LIB_SRC        ${JPEG_INCLUDE_DIR}     PARENT_SCOPE)
  
  set(debian_dependencies ${debian_dependencies} "libjpeg8-dev")
  
else(DO_NOT_USE_YAYI_JPEG)

  set(LIBJPEG_ARCHIVE ${THIRD_PARTIES_PATH}/jpegsrc.v8d.tar.gz)
  set(LIBJPEG jpeg-8d)
  set(LIBJPEG_SOURCE_DIR
      ${CMAKE_BINARY_DIR}/untarred/${LIBJPEG}
      CACHE PATH
      "Jpeg sources directory")

  if(NOT EXISTS ${LIBJPEG_SOURCE_DIR})
    message(STATUS "[YAYIIO] Creating Jpeg directory and deflating ${LIBJPEG}")
    file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/untarred)
    
    execute_process(COMMAND ${CMAKE_COMMAND} -E tar zxf ${LIBJPEG_ARCHIVE}
                    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/untarred)    
    
  endif()


  set(LIBJPEG_SRC

    # common
    ${LIBJPEG_SOURCE_DIR}/jcapimin.c  ${LIBJPEG_SOURCE_DIR}/jcapistd.c  ${LIBJPEG_SOURCE_DIR}/jdapimin.c  ${LIBJPEG_SOURCE_DIR}/jdapistd.c
    ${LIBJPEG_SOURCE_DIR}/jcomapi.c   ${LIBJPEG_SOURCE_DIR}/jcparam.c   ${LIBJPEG_SOURCE_DIR}/jctrans.c   ${LIBJPEG_SOURCE_DIR}/jdtrans.c
    ${LIBJPEG_SOURCE_DIR}/jaricom.c   ${LIBJPEG_SOURCE_DIR}/jerror.c    ${LIBJPEG_SOURCE_DIR}/jmemmgr.c   ${LIBJPEG_SOURCE_DIR}/jutils.c
    ${LIBJPEG_SOURCE_DIR}/jmemnobs.c

    # compression
    ${LIBJPEG_SOURCE_DIR}/jcinit.c    ${LIBJPEG_SOURCE_DIR}/jcmaster.c  ${LIBJPEG_SOURCE_DIR}/jcmainct.c  ${LIBJPEG_SOURCE_DIR}/jcprepct.c
    ${LIBJPEG_SOURCE_DIR}/jccoefct.c  ${LIBJPEG_SOURCE_DIR}/jccolor.c   ${LIBJPEG_SOURCE_DIR}/jcsample.c  ${LIBJPEG_SOURCE_DIR}/jcdctmgr.c
    ${LIBJPEG_SOURCE_DIR}/jfdctint.c  ${LIBJPEG_SOURCE_DIR}/jfdctfst.c  ${LIBJPEG_SOURCE_DIR}/jfdctflt.c  ${LIBJPEG_SOURCE_DIR}/jchuff.c
    ${LIBJPEG_SOURCE_DIR}/jcarith.c   ${LIBJPEG_SOURCE_DIR}/jcmarker.c  ${LIBJPEG_SOURCE_DIR}/jdatadst.c

    # decompression
    ${LIBJPEG_SOURCE_DIR}/jdmaster.c  ${LIBJPEG_SOURCE_DIR}/jdinput.c   ${LIBJPEG_SOURCE_DIR}/jdmainct.c  ${LIBJPEG_SOURCE_DIR}/jdcoefct.c
    ${LIBJPEG_SOURCE_DIR}/jdpostct.c  ${LIBJPEG_SOURCE_DIR}/jdmarker.c  ${LIBJPEG_SOURCE_DIR}/jdhuff.c    ${LIBJPEG_SOURCE_DIR}/jdarith.c
    ${LIBJPEG_SOURCE_DIR}/jddctmgr.c  ${LIBJPEG_SOURCE_DIR}/jidctint.c  ${LIBJPEG_SOURCE_DIR}/jidctfst.c  ${LIBJPEG_SOURCE_DIR}/jidctflt.c
    ${LIBJPEG_SOURCE_DIR}/jdsample.c  ${LIBJPEG_SOURCE_DIR}/jdcolor.c   ${LIBJPEG_SOURCE_DIR}/jdmerge.c   ${LIBJPEG_SOURCE_DIR}/jquant1.c
    ${LIBJPEG_SOURCE_DIR}/jquant2.c   ${LIBJPEG_SOURCE_DIR}/jdatasrc.c
  )

  file(MAKE_DIRECTORY ${config_folder}/jpeg)
  configure_file(${THIRD_PARTIES_PATH}/Config/jconfig.h ${config_folder}/jpeg COPYONLY)

  # installation
  set(LIBJPEG_PUBLIC_HEADERS
    ${config_folder}/jpeg/jconfig.h
    ${LIBJPEG_SOURCE_DIR}/jpeglib.h
    ${LIBJPEG_SOURCE_DIR}/jmorecfg.h
    ${LIBJPEG_SOURCE_DIR}/jerror.h
    ${LIBJPEG_SOURCE_DIR}/jinclude.h
    ${LIBJPEG_SOURCE_DIR}/jpegint.h
    #${LIBJPEG_SOURCE_DIR}/jdct.h
    #${LIBJPEG_SOURCE_DIR}/jmemsys.h
    ${LIBJPEG_SOURCE_DIR}/jversion.h
  )

  # we use only static libraries here. All of them will be included in YayiIO
  add_library (${LIBJPEG} STATIC ${LIBJPEG_SRC} ${LIBJPEG_PUBLIC_HEADERS})
  set_property(TARGET ${LIBJPEG} PROPERTY FOLDER "Externals/")
  
  # specific to libjpeg
  set_property(TARGET ${LIBJPEG} APPEND PROPERTY COMPILE_DEFINITIONS NO_GETENV)

  # jpeg configuration file
  target_include_directories(${LIBJPEG} PUBLIC ${config_folder}/jpeg)


  set(JPEG                ${LIBJPEG}              PARENT_SCOPE)
  set(JPEG_LIB_SRC        ${LIBJPEG_SOURCE_DIR}   PARENT_SCOPE)

endif(DO_NOT_USE_YAYI_JPEG)







# ZLib
if(DO_NOT_USE_YAYI_ZLIB)
  find_package(ZLIB REQUIRED QUIET)
  message(STATUS "[YAYIIO] Zlib location is ${ZLIB_INCLUDE_DIR}")
  set(ZLIB_SRC_DIR ${ZLIB_INCLUDE_DIR}  PARENT_SCOPE)
  set(ZLIB         ${ZLIB_LIBRARIES}    PARENT_SCOPE)

  set(debian_dependencies ${debian_dependencies} "zlib1g-dev")
  
else(DO_NOT_USE_YAYI_ZLIB)

  set(LIBZLIB_ARCHIVE ${THIRD_PARTIES_PATH}/zlib-1.2.5.tar.gz)
  set(LIBZLIB zlib-1.2.5)
  set(ZLIB_SOURCE_DIR
      ${CMAKE_BINARY_DIR}/untarred/${LIBZLIB})

  if(NOT EXISTS ${ZLIB_SOURCE_DIR})
    message(STATUS "[YAYIIO] Creating ZLib directory and deflating ${LIBZLIB} into ${ZLIB_SOURCE_DIR}")
    
    if(NOT EXISTS ${CMAKE_BINARY_DIR}/untarred)
      file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/untarred)
    endif()
    
    execute_process(COMMAND ${CMAKE_COMMAND} -E tar zxf ${LIBZLIB_ARCHIVE}
                    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/untarred)    
    
  endif()
  
  set(ZLIB_SRC

    ${ZLIB_SOURCE_DIR}/adler32.c
    ${ZLIB_SOURCE_DIR}/compress.c
    ${ZLIB_SOURCE_DIR}/crc32.c
    ${ZLIB_SOURCE_DIR}/deflate.c
    ${ZLIB_SOURCE_DIR}/gzclose.c
    ${ZLIB_SOURCE_DIR}/gzlib.c
    ${ZLIB_SOURCE_DIR}/gzread.c
    ${ZLIB_SOURCE_DIR}/gzwrite.c
    ${ZLIB_SOURCE_DIR}/infback.c
    ${ZLIB_SOURCE_DIR}/inffast.c
    ${ZLIB_SOURCE_DIR}/inflate.c
    ${ZLIB_SOURCE_DIR}/inftrees.c
    ${ZLIB_SOURCE_DIR}/trees.c
    ${ZLIB_SOURCE_DIR}/uncompr.c
    ${ZLIB_SOURCE_DIR}/zutil.c

    ${ZLIB_SOURCE_DIR}/crc32.h
    ${ZLIB_SOURCE_DIR}/deflate.h
    ${ZLIB_SOURCE_DIR}/gzguts.h
    ${ZLIB_SOURCE_DIR}/inffast.h
    ${ZLIB_SOURCE_DIR}/inffixed.h
    ${ZLIB_SOURCE_DIR}/inflate.h
    ${ZLIB_SOURCE_DIR}/inftrees.h
    ${ZLIB_SOURCE_DIR}/trees.h
    ${ZLIB_SOURCE_DIR}/zutil.h

    #${ZLIB_SOURCE_DIR}/contrib/masmx86/gvmat32.asm
    #${ZLIB_SOURCE_DIR}/contrib/masmx86/gvmat32c.c
    #${ZLIB_SOURCE_DIR}/contrib/masmx86/inffas32.asm

  )

  set(ZLIB_PUBLIC_HEADERS
    ${ZLIB_SOURCE_DIR}/zlib.h
    ${ZLIB_SOURCE_DIR}/zconf.h
  )

  # we may worry about sharing zlib among HDF5, libTIFF, libPNG. Everything should be fine if we are
  # using the static libraries, since they get all linked in yayiIO
  add_library(${LIBZLIB} STATIC ${ZLIB_SRC} ${ZLIB_PUBLIC_HEADERS})
  set_property(TARGET ${LIBZLIB} PROPERTY FOLDER "Externals/")


  set(ZLIB                ${LIBZLIB} PARENT_SCOPE)
  set(ZLIB_SRC_DIR        ${ZLIB_SOURCE_DIR} PARENT_SCOPE)
  
endif(DO_NOT_USE_YAYI_ZLIB)






# lib PNG
if(DO_NOT_USE_YAYI_LIBPNG)
  find_package(PNG REQUIRED QUIET)
  message(STATUS "[YAYIIO] LibPNG location is ${PNG_INCLUDE_DIR}")
  set(PNG_LIB_SRC       ${PNG_INCLUDE_DIR}    PARENT_SCOPE)
  set(PNG               ${PNG_LIBRARIES}      PARENT_SCOPE)
  set(PNG_DEFS          ${PNG_DEFINITIONS}    PARENT_SCOPE)
  
  set(debian_dependencies ${debian_dependencies} "libpng12-dev")

else(DO_NOT_USE_YAYI_LIBPNG)

  set(LIBPNG png-1.5.14)
  set(LIBPNG_ARCHIVE ${THIRD_PARTIES_PATH}/lib${LIBPNG}.tar.gz)
  set(LIBPNG_SOURCE_DIR
      ${CMAKE_BINARY_DIR}/untarred/lib${LIBPNG})

  if(NOT EXISTS ${LIBPNG_SOURCE_DIR})
    message(STATUS "[YAYIIO] Creating libPNG directory and deflating ${LIBPNG} into ${LIBPNG_SOURCE_DIR}")
    
    if(NOT EXISTS ${CMAKE_BINARY_DIR}/untarred)
      file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/untarred)
    endif()
    
    execute_process(COMMAND ${CMAKE_COMMAND} -E tar zxf ${LIBPNG_ARCHIVE}
                    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/untarred)    
    
  endif()

  message(STATUS "Configuring PNG headers")
  get_filename_component(png_absolute ${LIBPNG_SOURCE_DIR} REALPATH )
  if(MSVC)
     configure_file(${LIBPNG_SOURCE_DIR}/scripts/pnglibconf.h.prebuilt ${png_absolute}/pnglibconf.h COPYONLY)
  else()
    # thomas, as-t-on besoin de faire la distinction win/linux ??
    # @raf pas sur mais visual oui a cause de pnglibconf.h.prebuilt
    configure_file(${LIBPNG_SOURCE_DIR}/scripts/pnglibconf.h.prebuilt ${png_absolute}/pnglibconf.h)
  endif()

  set(LIBPNG_PUBLIC_HEADERS
    ${LIBPNG_SOURCE_DIR}/png.h
    ${LIBPNG_SOURCE_DIR}/pngconf.h
    ${LIBPNG_SOURCE_DIR}/pnglibconf.h)

  set(LIBPNG_SRC
    ${LIBPNG_PUBLIC_HEADERS}
    ${LIBPNG_SOURCE_DIR}/pngget.c
    ${LIBPNG_SOURCE_DIR}/pngmem.c
    ${LIBPNG_SOURCE_DIR}/pngpread.c
    ${LIBPNG_SOURCE_DIR}/pngread.c
    ${LIBPNG_SOURCE_DIR}/pngrio.c
    ${LIBPNG_SOURCE_DIR}/pngrtran.c
    ${LIBPNG_SOURCE_DIR}/pngrutil.c
    ${LIBPNG_SOURCE_DIR}/pngset.c
    ${LIBPNG_SOURCE_DIR}/pngtrans.c

    ${LIBPNG_SOURCE_DIR}/pngerror.c
    ${LIBPNG_SOURCE_DIR}/png.c

    ${LIBPNG_SOURCE_DIR}/pngwio.c
    ${LIBPNG_SOURCE_DIR}/pngwrite.c
    ${LIBPNG_SOURCE_DIR}/pngwtran.c
    ${LIBPNG_SOURCE_DIR}/pngwutil.c
  )

  add_library(${LIBPNG} STATIC ${LIBPNG_SRC} ${LIBPNG_PUBLIC_HEADERS})
  target_link_libraries(${LIBPNG} LINK_PRIVATE ${LIBZLIB})
  set_property(TARGET ${LIBPNG} PROPERTY FOLDER "Externals/")
  target_include_directories(${LIBPNG} PRIVATE ${ZLIB_SOURCE_DIR})
  target_compile_definitions(${LIBPNG} PRIVATE -DPNG_CONFIGURE_LIBPNG)


  if(CMAKE_HOST_WIN32)
    # on windows only / warning: get back the Release/Debug definitions
    get_target_property(current_def ${LIBPNG} COMPILE_DEFINITIONS)
    if(NOT current_def)
      set(current_def "")
    endif()
    if(ZLIB_BUILD_SHARED AND LIBPNG_BUILD_SHARED)
      set(current_def ${current_def} PNG_USE_PNGVCRD ZLIB_DLL PNG_LIBPNG_SPECIALBUILD)
    endif()
    set(current_def_debug   ${current_def} DEBUG PNG_DEBUG=1)
    set(current_def_release ${current_def} NDEBUG)
    set_target_properties(${LIBPNG} PROPERTIES COMPILE_DEFINITIONS_DEBUG "PNG_DEBUG=1")
    set_target_properties(${LIBPNG} PROPERTIES COMPILE_DEFINITIONS_RELEASE "${current_def_release}")
    set_target_properties(${LIBPNG} PROPERTIES DEFINE_SYMBOL "PNG_BUILD_DLL")
  endif()

  set(PNG                 ${LIBPNG}              PARENT_SCOPE)
  set(PNG_LIB_SRC         ${LIBPNG_SOURCE_DIR}   PARENT_SCOPE)
  set(PNG_DEFS            ""   PARENT_SCOPE)
endif(DO_NOT_USE_YAYI_LIBPNG)



# lib TIFF
if(DO_NOT_USE_YAYI_LIBTIFF)
  find_package(TIFF REQUIRED QUIET)
  message(STATUS "[YAYIIO] LibTIFF location is ${TIFF_INCLUDE_DIR}")
  set(TIFF_LIB_SRC      ${TIFF_INCLUDE_DIR}    PARENT_SCOPE)
  set(TIFF              ${TIFF_LIBRARIES}      PARENT_SCOPE)
  set(debian_dependencies ${debian_dependencies} "libtiff4-dev")
else(DO_NOT_USE_YAYI_LIBTIFF)
  
  set(LIBTIFF tiff-4.0.3)
  set(LIBTIFF_ARCHIVE ${THIRD_PARTIES_PATH}/${LIBTIFF}.tar.gz)
  set(LIBTIFF_SOURCE_DIR
      ${CMAKE_BINARY_DIR}/untarred/${LIBTIFF}/libtiff)

  if(NOT EXISTS ${LIBTIFF_SOURCE_DIR})
    message(STATUS "[YAYIIO] Creating libTIFF directory and deflating ${LIBTIFF} into ${LIBTIFF_SOURCE_DIR}")
    
    if(NOT EXISTS ${CMAKE_BINARY_DIR}/untarred)
      file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/untarred)
    endif()
    
    execute_process(COMMAND ${CMAKE_COMMAND} -E tar zxf ${LIBTIFF_ARCHIVE}
                    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/untarred)    
    
  endif()


  set(LIBTIFF_PUBLIC_HEADERS
    ${LIBTIFF_SOURCE_DIR}/tiff.h
    ${LIBTIFF_SOURCE_DIR}/tiffio.h
    ${LIBTIFF_SOURCE_DIR}/tiffio.hxx
    #${LIBTIFF_SOURCE_DIR}/tiffconf.h
    ${THIRD_PARTIES_PATH}/Config/tif_config.h)


  set(LIBTIFF_SRC
    ${LIBTIFF_SOURCE_DIR}/tiffvers.h
    ${LIBTIFF_SOURCE_DIR}/tif_extension.c
    ${LIBTIFF_SOURCE_DIR}/tif_color.c
    #${LIBTIFF_SOURCE_DIR}/tiffcomp.h
    ${LIBTIFF_SOURCE_DIR}/tiffiop.h
    ${LIBTIFF_SOURCE_DIR}/t4.h
    ${LIBTIFF_SOURCE_DIR}/tif_dir.h
    ${LIBTIFF_SOURCE_DIR}/tif_fax3.h
    ${LIBTIFF_SOURCE_DIR}/tif_predict.h
    ${LIBTIFF_SOURCE_DIR}/uvcode.h
    ${LIBTIFF_SOURCE_DIR}/tif_aux.c
    ${LIBTIFF_SOURCE_DIR}/tif_close.c
    ${LIBTIFF_SOURCE_DIR}/tif_codec.c
    ${LIBTIFF_SOURCE_DIR}/tif_compress.c
    ${LIBTIFF_SOURCE_DIR}/tif_dir.c
    ${LIBTIFF_SOURCE_DIR}/tif_dirinfo.c
    ${LIBTIFF_SOURCE_DIR}/tif_dirread.c
    ${LIBTIFF_SOURCE_DIR}/tif_dirwrite.c
    ${LIBTIFF_SOURCE_DIR}/tif_dumpmode.c   # dunno what this is...
    ${LIBTIFF_SOURCE_DIR}/tif_error.c
    ${LIBTIFF_SOURCE_DIR}/tif_fax3.c
    ${LIBTIFF_SOURCE_DIR}/tif_fax3sm.c
    #${LIBTIFF_SOURCE_DIR}/mkg3states.c

    ${LIBTIFF_SOURCE_DIR}/tif_flush.c
    ${LIBTIFF_SOURCE_DIR}/tif_getimage.c
    ${LIBTIFF_SOURCE_DIR}/tif_jpeg.c
    #tiff-4.0.3/libtiff/tif_jpeg_12.c   # dunno
    #tiff-4.0.3/libtiff/tif_ojpeg.c    # I guess there is no need for this
    #${LIBTIFF_SOURCE_DIR}/tif_jbig.c  # external lib

    ${LIBTIFF_SOURCE_DIR}/tif_luv.c
    ${LIBTIFF_SOURCE_DIR}/tif_lzw.c
    #${LIBTIFF_SOURCE_DIR}//tif_lzma.c # lzma support unactivated as it requires an additional dependency
    ${LIBTIFF_SOURCE_DIR}/tif_next.c
    ${LIBTIFF_SOURCE_DIR}/tif_open.c
    ${LIBTIFF_SOURCE_DIR}/tif_packbits.c
    ${LIBTIFF_SOURCE_DIR}/tif_pixarlog.c
    ${LIBTIFF_SOURCE_DIR}/tif_predict.c
    ${LIBTIFF_SOURCE_DIR}/tif_print.c
    ${LIBTIFF_SOURCE_DIR}/tif_read.c
    ${LIBTIFF_SOURCE_DIR}/tif_strip.c
    ${LIBTIFF_SOURCE_DIR}/tif_swab.c
    ${LIBTIFF_SOURCE_DIR}/tif_thunder.c
    ${LIBTIFF_SOURCE_DIR}/tif_tile.c

    ${LIBTIFF_SOURCE_DIR}/tif_version.c
    ${LIBTIFF_SOURCE_DIR}/tif_warning.c

    ${LIBTIFF_SOURCE_DIR}/tif_write.c
    ${LIBTIFF_SOURCE_DIR}/tif_zip.c
  )

  file(MAKE_DIRECTORY ${config_folder}/libtiff)
  configure_file(${THIRD_PARTIES_PATH}/Config/tif_config.h ${config_folder}/libtiff/ COPYONLY)
  configure_file(${THIRD_PARTIES_PATH}/Config/tiffconf.h   ${config_folder}/libtiff/ COPYONLY)

  if(UNIX)
    set(LIBTIFF_SRC ${LIBTIFF_SRC} ${LIBTIFF_SOURCE_DIR}/tif_unix.c)
  else()
    set(LIBTIFF_SRC ${LIBTIFF_SRC} ${LIBTIFF_SOURCE_DIR}/tif_win32.c)
  endif()

  add_library(${LIBTIFF} STATIC ${LIBTIFF_SRC} ${LIBTIFF_PUBLIC_HEADERS})
  target_include_directories(${LIBTIFF} 
    PRIVATE ${ZLIB_SOURCE_DIR}
    PRIVATE ${LIBJPEG_SOURCE_DIR}
    PUBLIC  ${config_folder}/libtiff/)

  target_link_libraries(${LIBTIFF} LINK_PRIVATE ${LIBZLIB} ${LIBJPEG})
  set_property(TARGET ${LIBTIFF} PROPERTY FOLDER "Externals/")

  set(TIFF                ${LIBTIFF}              PARENT_SCOPE)
  set(TIFF_LIB_SRC        ${LIBTIFF_SOURCE_DIR}   PARENT_SCOPE)

endif(DO_NOT_USE_YAYI_LIBTIFF)




# HDF5 IO capabilities
if(ENABLE_HDF5)

  set(debian_dependencies ${debian_dependencies} "libhdf5-dev")

  if(WIN32)
    #TODO use /install__Windows_x86 default path
    set(HDF5 hdf5)
    set(HDF5_SOURCE_DIR
        hdf5
        CACHE PATH
        "hdf5 sources directory")
    message("hdf5 directory is ${HDF5_SOURCE_DIR}")

    # use http://www.hdfgroup.org/HDF5/release/obtain5.html
    #put it in external_libraries\hdf5
    set(HDF5_INSTALL_DIR ${HDF5_SOURCE_DIR} CACHE PATH "HDF5 installation root path")
    set(HDF5_INCLUDE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/${HDF5_INSTALL_DIR}/include PARENT_SCOPE)
  else(WIN32)
    # to compile with ./configure --prefix=$HOME/usr/local/ --with-zlib=$HOME/usr/local/
    set(HDF5_INSTALL_DIR  ${THIRD_PARTIES_PATH} CACHE PATH "HDF5 installation root path")
    set(HDF5_INCLUDE_DIRS ${HDF5_INSTALL_DIR}/include PARENT_SCOPE)
  endif(WIN32)

  find_library(HDF5LIBB hdf5 PATHS ${HDF5_INSTALL_DIR}/lib/
      DOC "HDF5 library found on the system"
      NO_DEFAULT_PATH
      NO_CMAKE_ENVIRONMENT_PATH
      NO_CMAKE_PATH
      NO_SYSTEM_ENVIRONMENT_PATH
      NO_CMAKE_SYSTEM_PATH
  )
  find_library(HDF5LIBL hdf5_hl PATHS ${HDF5_INSTALL_DIR}/lib/
      DOC "HDF5 Lite library found on the system"
      NO_DEFAULT_PATH
      NO_CMAKE_ENVIRONMENT_PATH
      NO_CMAKE_PATH
      NO_SYSTEM_ENVIRONMENT_PATH
      NO_CMAKE_SYSTEM_PATH
  )

  if(NOT(HDF5LIBB) OR NOT(HDF5LIBL))
    message("Not found HDF5 from the specified path")
    unset(HDF5LIBB CACHE)
    unset(HDF5LIBL CACHE)
    find_package(HDF5)
    message("HDF5 include :" ${HDF5_INCLUDE_DIRS})
    set(HDF5LIBB ${HDF5_hdf5_LIBRARIES})
    set(HDF5LIBL ${HDF5_hdf5_hl_LIBRARIES})
    set(HDF5LIBB ${HDF5_hdf5_LIBRARIES} PARENT_SCOPE)
    set(HDF5LIBL ${HDF5_hdf5_hl_LIBRARIES} PARENT_SCOPE)
  else()
    get_filename_component(HDF5LIBB2 ${HDF5LIBB} REALPATH)
    get_filename_component(HDF5LIBL2 ${HDF5LIBL} REALPATH)
    unset(HDF5LIBB CACHE)
    unset(HDF5LIBL CACHE)
    set(HDF5LIBB ${HDF5LIBB2} CACHE INTERNAL "HDF5 real path" FORCE)
    set(HDF5LIBL ${HDF5LIBL2} CACHE INTERNAL "HDF5HL real path" FORCE)
    set(HDF5LIBB ${HDF5LIBB2} PARENT_SCOPE)
    set(HDF5LIBL ${HDF5LIBL2} PARENT_SCOPE)

    set(HDF5FilesToInstall ${HDF5LIBB} ${HDF5LIBL})
    if(WIN32)
      install_lib_and_dll("${HDF5FilesToInstall}" lib libraries)
    else()
      install_realpath_with_rename("${HDF5FilesToInstall}" lib libraries Release)
    endif()
  endif()



endif()



# declaring the dependencies to the parent scope
set(debian_dependencies ${debian_dependencies} PARENT_SCOPE)

