## 
##
## Installation 
##
set(CPACK_PACKAGE_NAME                  "Yayi")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY   "Yayi: a generic mathematical morphology research and development framework")
set(CPACK_PACKAGE_VENDOR                "Raffi Enficiaud")

set(CPACK_PACKAGE_DESCRIPTION_FILE      "${YAYI_root_dir}/README.txt")
set(CPACK_RESOURCE_FILE_LICENSE         "${YAYI_root_dir}/LICENSE_1_0.txt")
set(CPACK_PACKAGE_VERSION               ${YAYI_VERSION})
set(CPACK_PACKAGE_VERSION_MAJOR         ${YAYI_MAJOR})
set(CPACK_PACKAGE_VERSION_MINOR         ${YAYI_MINOR})
set(CPACK_PACKAGE_VERSION_PATCH         ${YAYI_SUBMINOR})
set(CPACK_PACKAGE_INSTALL_DIRECTORY     "Yayi ${CPACK_PACKAGE_VERSION}")
set(CPACK_PACKAGE_CONTACT               "Raffi Enficiaud <raffi.enficiaud@free.fr>")

set(CPACK_COMPONENTS_ALL core python api_doc python_doc)
set(CPACK_COMPONENT_CORE_DISPLAY_NAME           "Core C++ libraries and headers")
set(CPACK_COMPONENT_PYTHON_DISPLAY_NAME         "Python extensions")

set(CPACK_COMPONENT_CORE_DESCRIPTION            "DLL and C++ headers for building programs with Yayi")
set(CPACK_COMPONENT_PYTHON_DESCRIPTION          "Python extensions of Yayi")

set(CPACK_COMPONENT_python_DEPENDS              core)

set(CPACK_COMPONENT_PYTHON_DOC_GROUP                "Documentation")
set(CPACK_COMPONENT_API_DOC_GROUP                   "Documentation")
set(CPACK_COMPONENT_GROUP_DOCUMENTATION_DESCRIPTION   "Documentation for Yayi")

set(CPACK_SOURCE_IGNORE_FILES
    ${CPACK_SOURCE_IGNORE_FILES}
    ${CMAKE_BINARY_DIR}
    ${YAYI_root_dir}/.git
    ${YAYI_root_dir}/.gitignore
    ${YAYI_root_dir}/plugins/project_managment
    ${YAYI_root_dir}/plugins/Logos
    ${YAYI_root_dir}/plugins/doxparser
    ${YAYI_root_dir}/plugins/Benches
    ${YAYI_root_dir}/plugins/WebSite)

#set(CPACK_ALL_INSTALL_TYPES Full Developer Python)
#set(CPACK_COMPONENT_LIBRARIES_INSTALL_TYPES         Python Developer Full)
#set(CPACK_COMPONENT_HEADERS_INSTALL_TYPES           Developer Full)
#set(CPACK_COMPONENT_PYTHON_INSTALL_TYPES            Python Full)


if(WIN32 AND NOT UNIX)
  # There is a bug in NSI that does not handle full unix paths properly. Make
  # sure there is at least one set of four (4) backlasshes.
  #set(CPACK_PACKAGE_ICON                "")
  #set(CPACK_NSIS_INSTALLED_ICON_NAME    "")
  set(CPACK_NSIS_DISPLAY_NAME           "${CPACK_PACKAGE_INSTALL_DIRECTORY}")
  set(CPACK_NSIS_HELP_LINK              "http:////raffi.enficiaud.free.fr")
  set(CPACK_NSIS_URL_INFO_ABOUT         "http:////raffi.enficiaud.free.fr")
  set(CPACK_NSIS_CONTACT                "raffi.enficiaud@free.fr")
  set(CPACK_NSIS_MODIFY_PATH            ON)

  set(CPACK_NSIS_ENABLE_UNINSTALL_BEFORE_INSTALL ON)
  set(CPACK_NSIS_URL_INFO_ABOUT ${CPACK_NSIS_HELP_LINK})
  set(CPACK_NSIS_MENU_LINKS
       "documentation/index.html" "C++ library documentation"
       ) 


  if(CMAKE_CL_64)
    set(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES64")
    set(CPACK_NSIS_PACKAGE_NAME "${CPACK_PACKAGE_INSTALL_DIRECTORY} (Win64)")
    set(CPACK_PACKAGE_INSTALL_REGISTRY_KEY "${CPACK_PACKAGE_NAME} ${CPACK_PACKAGE_VERSION} (Win64)")
  else()
    set(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES")
    set(CPACK_NSIS_PACKAGE_NAME "${CPACK_PACKAGE_INSTALL_DIRECTORY}")
    set(CPACK_PACKAGE_INSTALL_REGISTRY_KEY "${CPACK_PACKAGE_NAME} ${CPACK_PACKAGE_VERSION}")
  endif()


else()
  set(CPACK_STRIP_FILES                 TRUE)
  #set(CPACK_SOURCE_STRIP_FILES          TRUE)
endif()




message(STATUS "debian_dependencies are ${debian_dependencies}")

# debian package generation
if(UNIX AND NOT APPLE)
  set(CPACK_GENERATOR DEB)
  SET(CPACK_DEB_COMPONENT_INSTALL 1)
  #set(CPACK_COMPONENTS_GROUPING IGNORE)
  file(READ ${CPACK_PACKAGE_DESCRIPTION_FILE} CPACK_DEBIAN_PACKAGE_DESCRIPTION)
  string(REPLACE "\n" "" CPACK_DEBIAN_PACKAGE_DESCRIPTION "${CPACK_DEBIAN_PACKAGE_DESCRIPTION}")
  string(REPLACE "\r" "" CPACK_DEBIAN_PACKAGE_DESCRIPTION "${CPACK_DEBIAN_PACKAGE_DESCRIPTION}")

  message(${CPACK_DEBIAN_PACKAGE_DESCRIPTION})



  set(CPACK_DEBIAN_PACKAGE_DEPENDS)
  list(LENGTH debian_dependencies debian_dependencies_lenght)
  if(${debian_dependencies_lenght} GREATER 0)
    list(GET debian_dependencies 0 CPACK_DEBIAN_PACKAGE_DEPENDS)
    list(REMOVE_AT debian_dependencies 0)
  endif()
  
  foreach(var IN LISTS debian_dependencies)
    set(CPACK_DEBIAN_PACKAGE_DEPENDS "${CPACK_DEBIAN_PACKAGE_DEPENDS}, ${var}")
  endforeach()

  #message(FATAL_ERROR "CPACK_DEBIAN_PACKAGE_DEPENDS ${CPACK_DEBIAN_PACKAGE_DEPENDS}")
  
  #set(CPACK_DEBIAN_PACKAGE_DEPENDS "libc6 (>= 2.3.1-6), libgcc1 (>= 1:3.4.2-12), python2.6, libboost-program-options1.40.0 (>= 1.40.0)")
    
endif()
include(CPack)

