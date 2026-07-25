option(ATLAS_BUILD_TESTS "Build Atlas C++ tests" ON)
option(ATLAS_ENABLE_WARNINGS "Enable strict compiler warnings" ON)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(atlas_core
    src/core/concept.cpp
    src/graph/knowledge_graph.cpp
    src/io/atlas_store.cpp
    src/query/query_engine.cpp
)

target_include_directories(atlas_core PUBLIC include)
target_compile_features(atlas_core PUBLIC cxx_std_20)

if(ATLAS_ENABLE_WARNINGS)
    if(MSVC)
        target_compile_options(atlas_core PRIVATE /W4 /permissive-)
    else()
        target_compile_options(atlas_core PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wshadow)
    endif()
endif()

add_executable(atlas apps/atlas-cli/main.cpp)
target_link_libraries(atlas PRIVATE atlas_core)

if(ATLAS_ENABLE_WARNINGS)
    if(MSVC)
        target_compile_options(atlas PRIVATE /W4 /permissive-)
    else()
        target_compile_options(atlas PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wshadow)
    endif()
endif()

include(CTest)
if(BUILD_TESTING AND ATLAS_BUILD_TESTS)
    add_executable(atlas_cpp_tests tests/atlas_tests.cpp)
    target_link_libraries(atlas_cpp_tests PRIVATE atlas_core)
    add_test(NAME atlas_cpp_tests COMMAND atlas_cpp_tests)
endif()

install(TARGETS atlas RUNTIME DESTINATION bin)
