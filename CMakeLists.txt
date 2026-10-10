cmake_minimum_required(VERSION 3.20)

project(ExampleProject C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(example STATIC src/math_utils.c)
target_include_directories(example PUBLIC src)

include(FetchContent)
FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz
)

set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_executable(target_unit_tests tests/test_math.cpp)
target_link_libraries(target_unit_tests PRIVATE example GTest::gtest_main)
