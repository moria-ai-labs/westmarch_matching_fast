#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // For automatic conversion of STL containers
#include "edit_distance.cpp" // Include the C++ functions

namespace py = pybind11;

PYBIND11_MODULE(edit_distance_cpp, m) {
    m.doc() = "Python module for fast edit distance calculation using C++"; // Optional module docstring

    m.def("find_k_closest_words_cpp", &findKClosestWords, "A function that finds the k closest words from a vocabulary to a target word",
          py::arg("target_word"), py::arg("vocabulary"), py::arg("k"));

    // Expose calculateEditDistance if needed directly in Python, though findKClosestWords is the main interface
    m.def("calculate_edit_distance_cpp", &calculateEditDistance, "Calculates Levenshtein distance between two strings",
          py::arg("s1"), py::arg("s2"));
}
