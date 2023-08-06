# @file
# This file contains macro for generating a header file containing the current version
# of the sources the library is compiled against

# @author Raffi Enficiaud



macro(get_git_revisions GIT_REV GIT_DATE)

  find_package(Git)
  if(NOT GIT_FOUND)
    message(FATAL_ERROR "Git not found")
  endif()

  # from http://stackoverflow.com/questions/1435953/how-can-i-pass-git-sha1-to-compiler-as-definition-using-cmake
  execute_process(COMMAND
    "${GIT_EXECUTABLE}" describe --match=NeVeRmAtCh --always --abbrev=40 --dirty
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
    OUTPUT_VARIABLE ${GIT_REV}
    RESULT_VARIABLE GIT_CMD_RESULT
    ERROR_VARIABLE GIT_CMD_ERROR
    #ERROR_QUIET 
    OUTPUT_STRIP_TRAILING_WHITESPACE)

  if(NOT (${GIT_CMD_RESULT} EQUAL 0))
    message(STATUS "[GIT] command error: maybe not a git repository: ${GIT_CMD_RESULT} / ${GIT_CMD_ERROR}")
    set(${GIT_REV} "none")
  else()

    # the date of the commit
    execute_process(COMMAND
      "${GIT_EXECUTABLE}" log -1 --format=%ai --date=local
      WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
      OUTPUT_VARIABLE ${GIT_DATE}
      ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)

  endif()

endmacro(get_git_revisions)



# Old Subversion commands, might be reused.
#if(EXISTS ${YAYI_root_dir}/.svn)
#  find_package(Subversion)
#  if(Subversion_FOUND)
#    Subversion_WC_INFO(${YAYI_CORE_DIR} YayiCoreSVN)
#  else()
#    message(WARNING "Subversion not found")
#    set(YayiCoreSVN_WC_REVISION "XXX" CACHE STRING "Yayi SVN version")
#  endif(Subversion_FOUND)
#else()
#  message(WARNING "no .svn")
#  set(YayiCoreSVN_WC_REVISION "XXX" CACHE STRING "Yayi SVN version")
#endif()




macro(generate_library_version filename_to_generate)
  set(_revision_file_name ${YAYI_root_dir}/cmake/yayi_revision.cpp.config)

  set(_should_generate FALSE)
  set(_is_archive FALSE)
  
  set(_current_rev)
  set(_current_date)
  get_git_revisions(_current_rev _current_date)
  if(${_current_rev} STREQUAL "none")
    message(STATUS "[GIT] looks like a tarball")
    set(_is_archive TRUE)
    if(NOT EXISTS ${filename_to_generate})
      set(_current_rev "archive")
      set(_current_date "archive")
      set(_should_generate TRUE)
      message(FATAL_ERROR "Non existing")
    else()
      message(STATUS "[GIT] file ${filename_to_generate} already contains the version")
    endif()
  endif()
  
  if(NOT ${_is_archive})
    if(DEFINED _yayi_previous_revision)
      if(NOT (${_yayi_previous_revision} STREQUAL ${_current_rev}) OR (NOT EXISTS ${filename_to_generate}))
        set(_should_generate TRUE)
      endif()
    else()
      set(_should_generate TRUE)
    endif()
  endif()
  
  if(_should_generate)
    message(STATUS "Repository at revision ${_current_rev} commited at ${_current_date}")
    set(_yayi_previous_revision ${_current_rev} CACHE INTERNAL "internal revision to avoid repeated rebuild" FORCE)
    set(revision_version  ${_current_rev})
    set(revision_date     ${_current_date})
    configure_file(${_revision_file_name} ${filename_to_generate})
    set_source_files_properties(${filename_to_generate} PROPERTIES GENERATED TRUE)
    unset(revision_version)
    unset(revision_date)
    
  endif()
  
  unset(_should_generate)
  unset(_is_archive)
  unset(_current_rev)
  unset(_current_date)
  unset(_revision_file_name)
  
endmacro(generate_library_version)


