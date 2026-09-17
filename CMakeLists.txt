cmake_minimum_required(VERSION 3.15)
project(Conan LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(fmt REQUIRED)

add_executable(conan
    src/main.cpp
)

target_link_libraries(conan PRIVATE fmt::fmt)