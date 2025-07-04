# Fast Edit Distance Calculator

This project provides a high-performance solution for calculating the edit distance (Levenshtein distance) between strings and finding the *k* closest matches from a vocabulary for a list of target words. The core computation is implemented in C++ for speed, and Python is used for orchestration via Pybind11 bindings.

## Features

*   **Efficient Edit Distance**: Utilizes the Wagner-Fischer algorithm for calculating Levenshtein distance in C++.
*   **K-Closest Words**: Quickly finds the *k* most similar words from a given vocabulary for each target word.
*   **Python Integration**: Seamlessly callable from Python thanks to Pybind11.
*   **Easy to Build**: Uses standard Python `setuptools` for building the C++ extension.

## Project Structure

*   `edit_distance.cpp`: Contains the core C++ logic for edit distance calculation (`calculateEditDistance`) and finding the k-closest words (`findKClosestWords`).
*   `bindings.cpp`: Contains the Pybind11 code to create Python bindings for the C++ functions. The resulting Python module is named `edit_distance_cpp`.
*   `setup.py`: The build script for compiling the C++ extension.
*   `main.py`: An example Python script demonstrating how to use the `edit_distance_cpp` module with sample data.
*   `test_edit_distance.py`: A suite of unit tests (using Python's `unittest` module) to verify the correctness of the implementation.
*   `AGENTS.md`: Contains specific instructions for AI agents working with this codebase, including build and test procedures.

## Prerequisites

*   A C++11 compatible compiler (e.g., GCC, Clang, MSVC).
*   Python (version 3.6 or newer recommended).
*   `pip` (Python package installer).

## Getting Started

### 1. Install Pybind11

Pybind11 is used for creating the Python bindings for the C++ code. It's listed as a setup requirement in `setup.py` but you can also install it manually:
```bash
pip install pybind11
```

### 2. Build the C++ Extension

Navigate to the project's root directory (where `setup.py` is located) and run the following command:

```bash
python setup.py build_ext --inplace
```

This command compiles the C++ code and creates a Python extension module (e.g., `edit_distance_cpp.cpython-XX-architecture.so` or `edit_distance_cpp.cpXX-win_amd64.pyd`) in the current directory. This file allows Python to call the C++ functions.

### 3. Run the Example

Once the module is built, you can run the example script:

```bash
python main.py
```

This script will:
1.  Define a sample vocabulary of words and a list of target words.
2.  Use the `find_k_closest_words_cpp` function from the compiled module to find the 3 closest words for each target.
3.  Print the results.
4.  Demonstrate direct usage of `calculate_edit_distance_cpp`.

### 4. Run Tests

To ensure everything is working correctly, run the unit tests:

```bash
python test_edit_distance.py
```

All tests should pass if the module was built successfully and the code is functioning as expected.

## How It Works

1.  **`calculateEditDistance(string1, string2)`**: This C++ function takes two strings and returns their Levenshtein distance. It uses dynamic programming (Wagner-Fischer algorithm).
2.  **`findKClosestWords(target_word, vocabulary, k)`**: This C++ function iterates through the `vocabulary`, calculates the edit distance from the `target_word` to each vocabulary word, and then returns a list of the `k` words with the smallest distances.
3.  **Pybind11 Bindings (`bindings.cpp`)**: This file makes the C++ functions available to Python. It handles the conversion of data types (e.g., C++ `std::vector<std::string>` to Python lists).
4.  **Python Usage (`main.py`, `test_edit_distance.py`)**: Python scripts can import the compiled `edit_distance_cpp` module and call the exposed functions as if they were native Python functions.

## Customization

*   **Modify Vocabulary/Targets**: Change the `vocabulary` and `target_words` lists in `main.py` to use your own data.
*   **Adjust `k`**: Modify the `k` parameter to find a different number of closest words.
*   **Extend C++ Logic**: If you need different string similarity metrics or further optimizations, you can modify `edit_distance.cpp` and update the bindings in `bindings.cpp`. Remember to rebuild the module after any C++ changes.

This project serves as a template for CPU-intensive text processing tasks where C++ performance is beneficial within a Python-driven workflow.
