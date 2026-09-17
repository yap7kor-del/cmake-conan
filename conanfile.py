from conan import ConanFile
from conan.tools.cmake import CMakeToolchain,CMakeDeps
class ConanDemo(ConanFile):
    name="conan_demo"
    version="1.0"
    settings=(
        "os",
        "arch",
        "compiler",
        "build_type"
    )
    requires=[
        "fmt/11.0.2",
    ]
    generators=[
        CMakeToolchain,
        CMakeDeps
    ]