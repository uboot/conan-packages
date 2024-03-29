from conans import ConanFile, CMake, tools


class AppConan(ConanFile):
    name = "app"
    version = "1.2.3"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    revision_mode = "scm"

    def requirements(self):
        self.requires("tree/1.2.3@mycompany/stable")
        self.requires("core/1.2.3@mycompany/stable")
        if self.settings.os != "Windows":
            self.requires("hello/1.2.3@mycompany/stable")
            self.options['hello'].shared = True

    def source(self):
        self.run("git clone https://github.com/conan-io/hello.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(HelloWorld)",
                              '''PROJECT(HelloWorld)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="hello")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

