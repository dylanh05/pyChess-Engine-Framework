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
CMAKE_BINARY_DIR = /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles

# Include any dependencies generated for this target.
include CMakeFiles/cEngine.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/cEngine.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/cEngine.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/cEngine.dir/flags.make

CMakeFiles/cEngine.dir/cminimax_iter.cpp.o: CMakeFiles/cEngine.dir/flags.make
CMakeFiles/cEngine.dir/cminimax_iter.cpp.o: cminimax_iter.cpp
CMakeFiles/cEngine.dir/cminimax_iter.cpp.o: CMakeFiles/cEngine.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/cEngine.dir/cminimax_iter.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/cEngine.dir/cminimax_iter.cpp.o -MF CMakeFiles/cEngine.dir/cminimax_iter.cpp.o.d -o CMakeFiles/cEngine.dir/cminimax_iter.cpp.o -c /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/cminimax_iter.cpp

CMakeFiles/cEngine.dir/cminimax_iter.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/cEngine.dir/cminimax_iter.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/cminimax_iter.cpp > CMakeFiles/cEngine.dir/cminimax_iter.cpp.i

CMakeFiles/cEngine.dir/cminimax_iter.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/cEngine.dir/cminimax_iter.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/cminimax_iter.cpp -o CMakeFiles/cEngine.dir/cminimax_iter.cpp.s

# Object files for target cEngine
cEngine_OBJECTS = \
"CMakeFiles/cEngine.dir/cminimax_iter.cpp.o"

# External object files for target cEngine
cEngine_EXTERNAL_OBJECTS =

cEngine.cpython-38-x86_64-linux-gnu.so: CMakeFiles/cEngine.dir/cminimax_iter.cpp.o
cEngine.cpython-38-x86_64-linux-gnu.so: CMakeFiles/cEngine.dir/build.make
cEngine.cpython-38-x86_64-linux-gnu.so: CMakeFiles/cEngine.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared module cEngine.cpython-38-x86_64-linux-gnu.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/cEngine.dir/link.txt --verbose=$(VERBOSE)
	/usr/bin/strip /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/cEngine.cpython-38-x86_64-linux-gnu.so

# Rule to build all files generated by this target.
CMakeFiles/cEngine.dir/build: cEngine.cpython-38-x86_64-linux-gnu.so
.PHONY : CMakeFiles/cEngine.dir/build

CMakeFiles/cEngine.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/cEngine.dir/cmake_clean.cmake
.PHONY : CMakeFiles/cEngine.dir/clean

CMakeFiles/cEngine.dir/depend:
	cd /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles /mnt/c/Users/daher/Documents/Projects/pyChess-Engine-Framework/cengines/cppfiles/CMakeFiles/cEngine.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/cEngine.dir/depend
