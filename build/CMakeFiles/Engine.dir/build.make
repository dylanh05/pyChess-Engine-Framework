# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.26

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/dylanah/.local/lib/python3.8/site-packages/cmake/data/bin/cmake

# The command to remove a file.
RM = /home/dylanah/.local/lib/python3.8/site-packages/cmake/data/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/build

# Include any dependencies generated for this target.
include CMakeFiles/Engine.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/Engine.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/Engine.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/Engine.dir/flags.make

CMakeFiles/Engine.dir/cppengine.cpp.o: CMakeFiles/Engine.dir/flags.make
CMakeFiles/Engine.dir/cppengine.cpp.o: /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/cppengine.cpp
CMakeFiles/Engine.dir/cppengine.cpp.o: CMakeFiles/Engine.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/Engine.dir/cppengine.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/Engine.dir/cppengine.cpp.o -MF CMakeFiles/Engine.dir/cppengine.cpp.o.d -o CMakeFiles/Engine.dir/cppengine.cpp.o -c /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/cppengine.cpp

CMakeFiles/Engine.dir/cppengine.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Engine.dir/cppengine.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/cppengine.cpp > CMakeFiles/Engine.dir/cppengine.cpp.i

CMakeFiles/Engine.dir/cppengine.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Engine.dir/cppengine.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/cppengine.cpp -o CMakeFiles/Engine.dir/cppengine.cpp.s

# Object files for target Engine
Engine_OBJECTS = \
"CMakeFiles/Engine.dir/cppengine.cpp.o"

# External object files for target Engine
Engine_EXTERNAL_OBJECTS =

Engine.cpython-38-x86_64-linux-gnu.so: CMakeFiles/Engine.dir/cppengine.cpp.o
Engine.cpython-38-x86_64-linux-gnu.so: CMakeFiles/Engine.dir/build.make
Engine.cpython-38-x86_64-linux-gnu.so: CMakeFiles/Engine.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared module Engine.cpython-38-x86_64-linux-gnu.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/Engine.dir/link.txt --verbose=$(VERBOSE)
	/usr/bin/strip /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/build/Engine.cpython-38-x86_64-linux-gnu.so

# Rule to build all files generated by this target.
CMakeFiles/Engine.dir/build: Engine.cpython-38-x86_64-linux-gnu.so
.PHONY : CMakeFiles/Engine.dir/build

CMakeFiles/Engine.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/Engine.dir/cmake_clean.cmake
.PHONY : CMakeFiles/Engine.dir/clean

CMakeFiles/Engine.dir/depend:
	cd /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/build /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/build /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/build/CMakeFiles/Engine.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/Engine.dir/depend

