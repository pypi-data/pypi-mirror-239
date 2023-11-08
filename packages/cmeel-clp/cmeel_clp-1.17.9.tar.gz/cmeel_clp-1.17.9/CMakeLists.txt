cmake_minimum_required(VERSION 3.20)

set(NAME Clp)
set(VERSION "1.17.9")

project(cmeel-${NAME} VERSION ${CMAKE_VERSION})

include(FindPkgConfig)
pkg_check_modules(CoinUtils REQUIRED coinutils)

if(DEFINED ENV{CMEEL_JOBS})
  set(CMEEL_JOBS
      $ENV{CMEEL_JOBS}
      CACHE STRING "number of build jobs" FORCE)
else()
  set(CMEEL_JOBS
      4
      CACHE STRING "number of build jobs")
endif()

string(REPLACE ";" " " CoinUtils_LDFLAGS_STR "${CoinUtils_LDFLAGS}")

include(ExternalProject)
ExternalProject_Add(
  ${NAME}
  URL "https://github.com/coin-or/${NAME}/archive/refs/tags/releases/${VERSION}.tar.gz"
      DOWNLOAD_EXTRACT_TIMESTAMP
      OFF
  BUILD_IN_SOURCE ON
  CONFIGURE_COMMAND
    "./configure" "--prefix=${CMAKE_INSTALL_PREFIX}"
    "--with-coinutils-lib=${CoinUtils_LDFLAGS_STR}"
    "--with-coinutils-incdir=${CoinUtils_INCLUDE_DIRS}"
  BUILD_COMMAND "make" "-j${CMEEL_JOBS}"
  TEST_COMMAND "make" "check"
  INSTALL_COMMAND "make" "install" "-j1"
  COMMAND
    "${CMAKE_COMMAND}" "-E" "rm" "${CMAKE_INSTALL_PREFIX}/lib/lib${NAME}.la"
    "${CMAKE_INSTALL_PREFIX}/lib/lib${NAME}Solver.la")

# dummy file for install target
install(FILES README.md DESTINATION share/cmeel-${NAME}/)
