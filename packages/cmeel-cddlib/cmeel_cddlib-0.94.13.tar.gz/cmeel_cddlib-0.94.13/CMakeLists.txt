cmake_minimum_required(VERSION 3.20)

set(NAME cddlib)
set(ORIGINAL_VERSION "0.94m")
set(NUMERIC_VERSION "0.94.13")

project(cmeel-${NAME} VERSION ${CMAKE_VERSION})

if(DEFINED ENV{CMEEL_JOBS})
  set(CMEEL_JOBS
      $ENV{CMEEL_JOBS}
      CACHE STRING "number of build jobs" FORCE)
else()
  set(CMEEL_JOBS
      4
      CACHE STRING "number of build jobs")
endif()

include(ExternalProject)
ExternalProject_Add(
  ${NAME}
  URL "https://github.com/${NAME}/${NAME}/releases/download/${ORIGINAL_VERSION}/${NAME}-${ORIGINAL_VERSION}.tar.gz"
      DOWNLOAD_EXTRACT_TIMESTAMP
      OFF
  BUILD_IN_SOURCE ON
  CONFIGURE_COMMAND "./configure" "--prefix=${CMAKE_INSTALL_PREFIX}"
  BUILD_COMMAND "make" "-j${CMEEL_JOBS}"
  TEST_COMMAND "make" "check"
  INSTALL_COMMAND "make" "install")

# dummy file for install target
install(FILES README.md DESTINATION share/cmeel-${NAME}/)
