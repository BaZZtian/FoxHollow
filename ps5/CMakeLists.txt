# SPDX-License-Identifier: MIT
cmake_minimum_required(VERSION 3.25)
project(sfa_ps5_objects LANGUAGES C)

if(NOT PROSPERO OR NOT CMAKE_CROSSCOMPILING)
    message(FATAL_ERROR "Use the open PS5 payload SDK toolchain")
endif()
if(NOT SFA_SOURCE_DIR OR NOT EXISTS "${SFA_SOURCE_DIR}/port/compiling.txt")
    message(FATAL_ERROR "SFA_SOURCE_DIR must name the privately exported Foxhollow source")
endif()
if(NOT SFA_ZLIB_INCLUDE_DIR OR NOT EXISTS "${SFA_ZLIB_INCLUDE_DIR}/zlib.h"
    OR NOT EXISTS "${SFA_ZLIB_INCLUDE_DIR}/zconf.h")
    message(FATAL_ERROR "Provide the actual target-generated zlib compatibility headers")
endif()

set(CMAKE_C_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
file(STRINGS "${SFA_SOURCE_DIR}/port/compiling.txt" sfa_sources)
list(FILTER sfa_sources EXCLUDE REGEX "^ *(#|$)")
list(TRANSFORM sfa_sources PREPEND "${SFA_SOURCE_DIR}/game/src/")

# This target checks the actual game translation units against the PS5 ABI.
# It deliberately has no executable, platform stubs, packaging or deployment.
add_library(sfa_game STATIC ${sfa_sources})
target_include_directories(sfa_game PRIVATE
    "${SFA_ZLIB_INCLUDE_DIR}"
    "${SFA_SOURCE_DIR}/port/include"
    "${SFA_SOURCE_DIR}/extern/aurora/include"
    "${SFA_SOURCE_DIR}/extern/musyx/include"
    "${SFA_SOURCE_DIR}/game/include"
    "${SFA_SOURCE_DIR}/game")
target_compile_definitions(sfa_game PRIVATE
    TARGET_PC=1 BUILD_VERSION=0 VERSION_GSAE01 NDEBUG=1
    MUSY_TARGET=MUSY_TARGET_PC MUSY_VERSION_MAJOR=2 MUSY_VERSION_MINOR=0
    MUSY_VERSION_PATCH=0 MUSYX_ENABLE_DEBUGGER=1)
target_compile_options(sfa_game PRIVATE
    -std=gnu11 -fsigned-char -fcommon -Wno-error=incompatible-pointer-types
    -include "${SFA_SOURCE_DIR}/port/include/foxhollow_compat.h"
    -fpatchable-function-entry=16)
