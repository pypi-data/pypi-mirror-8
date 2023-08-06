

# to avoid having some ../.. in the paths
get_filename_component(YAYI_root_dir_absolute ${YAYI_root_dir} ABSOLUTE)
set(YAYI_DOCUMENTATION_ROOT ${YAYI_root_dir_absolute}/doc)


# SPHINX
# Getting sphinx availability
execute_process(
  COMMAND ${PYTHON_EXECUTABLE} -c "try:\n\timport sphinx\n\tprint \"TRUE\"\nexcept Exception, e:\n\tprint \"FALSE\""
  OUTPUT_VARIABLE SPHINX_AVAILABLE
  ERROR_VARIABLE  SPHINX_ERROR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

# error in checking ? should not occur
if(NOT (SPHINX_ERROR STREQUAL ""))
  message(FATAL_ERROR "Error: something wrong with the sphinx detection script: ${SPHINX_ERROR}")
endif()

if(SPHINX_AVAILABLE STREQUAL "FALSE")
  message(STATUS "[YAYIDoc] Sphinx not available")
else()
  message(STATUS "[YAYIDoc] Sphinx available from python: adding sphinx target")

  if(UNIX)
    # adds YAYIPATH to make environment
    if(APPLE)
      set(VARRPATH "DYLD_LIBRARY_PATH")
    else()
      set(VARRPATH "LD_LIBRARY_PATH")
    endif()
    set(SPHINX_COMMAND make YAYIPATH=$<TARGET_FILE_DIR:YayiCommonPython> ${VARRPATH}=$ENV{${VARRPATH}}:${Boost_LIBRARY_DIRS})
  elseif(WIN32)

    # test how to do it under windows...
    set(SPHINX_COMMAND "set YAYIPATH=$<TARGET_FILE_DIR:YayiCommonPython>\nset PATH=%PATH%\;${Boost_LIBRARY_DIRS}\nmake.bat")
  endif()




  add_custom_target(Sphinx
    #${SPHINX_COMMAND} html
    sphinx-build -b html ${YAYI_DOCUMENTATION_ROOT}/sphinx ${YAYI_PYTHON_PACKAGE_LOCATION}/doc
    WORKING_DIRECTORY ${YAYI_DOCUMENTATION_ROOT}/sphinx
    COMMENT "Generating sphinx documentation"
    VERBATIM
    # we want the binaries to be there also
    DEPENDS PythonPackageSetup
    SOURCES
      ${YAYI_DOCUMENTATION_ROOT}/sphinx/conf.py
      ${YAYI_DOCUMENTATION_ROOT}/sphinx/index.rst )
  set_property(TARGET Sphinx PROPERTY FOLDER "Documentation/")

endif()




# Doxygen
set(YAYI_DOXYGEN_PATH ${YAYI_DOCUMENTATION_ROOT}/Doxygen)
find_file(DOXYGEN_CONFIG_FILE Doxyfile ${YAYI_DOXYGEN_PATH})
mark_as_advanced(DOXYGEN_CONFIG_FILE)


find_package(Doxygen)
if(NOT DOXYGEN_FOUND)
  message("Doxygen not found")
elseif(DOXYGEN_CONFIG_FILE)
  message(STATUS "[YAYIDoc] Doxygen: configuring documentation with file ${DOXYGEN_CONFIG_FILE}")
  set(YAYI_HTML_FILES_DIR "${YAYI_root_dir}/plugins/Website" CACHE FILEPATH "YAYI_HTML_FILES_DIR")
  set(DOXY_LAYOUT_FILE ${YAYI_DOXYGEN_PATH}/DoxygenLayout_new.xml)
  
  if(DOXYGEN_DOT_FOUND)
    message("[YAYIDoc] Doxygen dot found at ${DOXYGEN_DOT_PATH}")
  else(DOXYGEN_DOT_FOUND)
    message("[YAYIDoc] Doxygen dot not found")
  endif(DOXYGEN_DOT_FOUND)

  #message("YAYI_HTML_FILES_DIR ${YAYI_HTML_FILES_DIR}")

  ###### GENERAL ######
  set(DOXY_OUTPUT_DIR           ${CMAKE_BINARY_DIR}/documentation/doxygen)
  set(DOXY_CONFIG_FILE          ${DOXY_OUTPUT_DIR}/Doxyfile.generated)

  set(DOXY_STRIP_FROM_PATH      ${YAYI_root_dir_absolute})
  set(DOXY_STRIP_FROM_INC_PATH  ${YAYI_root_dir_absolute})
    
  option(DOXYGEN_GENERATE_XML   "Generates xml documentation"   TRUE)
  option(DOXYGEN_GENERATE_LATEX "Generates LateX documentation" FALSE)
  option(DOXYGEN_GENERATE_HTML  "Generates HTML documentation"  TRUE)
  

  mark_as_advanced(DOXYGEN_GENERATE_HTML)
  mark_as_advanced(DOXYGEN_GENERATE_XML)
  mark_as_advanced(DOXYGEN_GENERATE_HTML)

  mark_as_advanced(DOXYGEN_HTML_HEADER)
  mark_as_advanced(DOXYGEN_HTML_FOOTER)
  mark_as_advanced(DOXYGEN_HTML_STYLESHEET)


  ###### INPUT FILES ######
  get_property(YAYI_CORE_DIR GLOBAL PROPERTY YAYI_CORE_DIR)
  set(DOXY_INPUT_DIRS \"${YAYI_DOCUMENTATION_ROOT}/Doxygen\")
  foreach(_DIR ${YAYI_CORE_DIR})
    list(APPEND DOXY_INPUT_DIRS \"${_DIR}/\")
  endforeach(_DIR ${YAYI_CORE_DIR})


  set(DOXY_FILES_PATTERN *.h *.hpp *.dox) #add dox for mainpage and others see http://entrenchant.blogspot.com/2009/09/doxygen-gotchas.html
  set(DOXY_IMAGE_PATH   \"${YAYI_HTML_FILES_DIR}\" CACHE FILEPATH  "Doxygen image path")
  set(DOXY_EXAMPLE_PATH \"${YAYI_HTML_FILES_DIR}\" \"${YAYI_root_dir}/coreTests\" CACHE FILEPATH  "Doxygen example path")
  #set(DOXY_LOGO_PATH    "${YAYI_root_dir}/plugins/Logos/yayi_logo_seul.png" CACHE FILEPATH  "Doxygen logo")
  set(DOXY_INCLUDE_PATH \"${JPEG_LIB_SRC}\" \"${PNG_LIB_SRC}\" \"${ZLIB_SRC_DIR}\" \"${Boost_INCLUDE_DIRS}\" CACHE FILEPATH "Doxygen preprocessor paths")
  set(DOXY_CITE_BIB_FILE "${YAYI_DOCUMENTATION_ROOT}/Latex/bib_all_utf8.bib")

  file(GLOB doxygen_extra_files ${YAYI_DOXYGEN_PATH}/icons/*.*)
  set(doxygen_extra_files2)
  foreach(f ${doxygen_extra_files})
    list(APPEND doxygen_extra_files2 \"${f}\")
  endforeach(f ${doxygen_extra_files})

  set(DOXY_EXTRA_FILES   "${doxygen_extra_files2}")

  # translating the cmake lists into dox
  string(REGEX REPLACE ";" " \\\\ \n" DOXY_FILES_PATTERN    "${DOXY_FILES_PATTERN}")
  string(REGEX REPLACE ";" " \\\\ \n" DOXY_INPUT_DIRS       "${DOXY_INPUT_DIRS}")
  string(REGEX REPLACE ";" " \\\\ \n" DOXY_IMAGE_PATH       "${DOXY_IMAGE_PATH}")
  string(REGEX REPLACE ";" " \\\\ \n" DOXY_EXAMPLE_PATH     "${DOXY_EXAMPLE_PATH}")
  #string(REGEX REPLACE ";" " \\\\ \n" DOXY_LOGO_PATH        "${DOXY_LOGO_PATH}")
  string(REGEX REPLACE ";" " \\\\ \n" DOXY_INCLUDE_PATH     "${DOXY_INCLUDE_PATH}")
  string(REGEX REPLACE ";" " \\\\ \n" DOXY_EXTRA_FILES      "${DOXY_EXTRA_FILES}")

  
  #### XML ####

  ###DOCBOOK ?
  #http://www.sagehill.net/docbookxsl/
  #check XML is ON
  #check docbook xsl
  #check xslt proc somewhere
  #and or add py to launch

  ###### HTML HELP ######

  if (FALSE)
    # we do not generate this shit
    find_package(HTMLHelp)
    if(HTML_HELP_COMPILER)
      option(DOXYGEN_GENERATE_HTML_HELP "Generate html-help documentation" ON)
      if(DOXYGEN_GENERATE_HTML_HELP)
        set(DOXY_GENERATE_HTMLHELP YES)
        set(DOXY_CHM_FILE ${DOXY_OUTPUT_DIR}/${PROJECT_NAME}.chm)
        string(REGEX REPLACE "[/]" "\\\\" DOXY_CHM_FILE ${DOXY_CHM_FILE})
      endif()
    endif()
  endif()



  #### DOT ####
  if(DOXYGEN_DOT_FOUND)
    set(DOXY_HAVE_DOT YES)
    set(DOT_BINARY_PATH ${DOXYGEN_DOT_PATH})
  else()
    set(DOXY_HAVE_DOT NO)
    set(DOT_BINARY_PATH "")
  endif()

   ###### WARNINGS ######
  if(CMAKE_BUILD_TOOL MATCHES "(msdev|devenv)")
    set(DOXY_WARN_FORMAT "\"$file($line) : $text \"")
  else()
    set(DOXY_WARN_FORMAT "\"$file:$line: $text \"")
  endif()

  message(STATUS "[YAYIDoc] Configuring file ${DOXYGEN_CONFIG_FILE} to ${DOXY_CONFIG_FILE}")
  configure_file(${DOXYGEN_CONFIG_FILE} ${DOXY_CONFIG_FILE} @ONLY)

  file(GLOB doxygen_pages ${YAYI_DOXYGEN_PATH}/*.dox)
  set(doxygen_layout_files 
      ${YAYI_DOXYGEN_PATH}/DoxygenLayout_new.xml
      ${DOXY_HTML_STYLESHEET}
      ${DOXY_HTML_STYLESHEET_EXT}
      ${YAYI_DOXYGEN_PATH}/footer.html
      ${YAYI_DOXYGEN_PATH}/header.html)

  add_custom_target(Doxygen
    ${DOXYGEN_EXECUTABLE} ${DOXY_CONFIG_FILE}
    COMMENT "Generating doxygen documentation"
    DEPENDS ${DOXYGEN_CONFIG_FILE}
    SOURCES 
      ${YAYI_root_dir}/cmake/CMakeDoc.cmake
      ${YAYI_DOXYGEN_PATH}/Doxyfile
      ${DOXY_CONFIG_FILE}
      ${doxygen_pages}
      ${doxygen_layout_files}
      )
  set_property(TARGET Doxygen PROPERTY FOLDER "Documentation/")
  source_group(Pages FILES ${doxygen_pages})  
  source_group(Layout FILES ${doxygen_layout_files})  


  #install(
  #  DIRECTORY ${DOXY_OUTPUT_DIR}/html/
  #  DESTINATION ${YAYI_DOCUMENTATION_INSTALLATION_RELATIVE_PATH}
  #  COMPONENT api_doc
  #  PATTERN "html/*")


endif()
