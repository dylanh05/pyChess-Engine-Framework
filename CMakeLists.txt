cmake_minimum_required(VERSION 3.4)
project(pylib)
add_subdirectory(pybind11)
pybind11_add_module(cEngine cminimax_iter.cpp)