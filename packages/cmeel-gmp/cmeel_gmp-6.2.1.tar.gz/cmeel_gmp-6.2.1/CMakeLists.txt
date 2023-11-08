cmake_minimum_required(VERSION 3.20)

set(NAME gmp)
set(VERSION 6.2.1)

project(cmeel-${NAME} VERSION ${VERSION})

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
  URL "https://homepages.laas.fr/gsaurel/${NAME}-${VERSION}.tar.lz"
      DOWNLOAD_EXTRACT_TIMESTAMP OFF
  BUILD_IN_SOURCE ON
  CONFIGURE_COMMAND "./configure" "--prefix=${CMAKE_INSTALL_PREFIX}"
  COMMAND sed -i.bak "/SUBDIRS/s/ doc//" Makefile
  BUILD_COMMAND "make" "-j${CMEEL_JOBS}"
  TEST_COMMAND "make" "check"
  INSTALL_COMMAND "make" "install"
  COMMAND "${CMAKE_COMMAND}" "-E" "rm"
          "${CMAKE_INSTALL_PREFIX}/lib/lib${NAME}.la")

# dummy file for install target
install(FILES README.md DESTINATION share/cmeel-${NAME}/)
