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

*   Git (for cloning the repository).
*   A C++11 compatible compiler (e.g., GCC, Clang, MSVC).
*   Python (version 3.6 or newer recommended).
*   `pip` (Python package installer).

## Installation from Source (via Git)

1.  **Clone the Repository**:
    Replace `your-username/your-repository-name` with the actual URL of the Git repository.
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Install Pybind11 (if not building through setup_requires)**:
    Pybind11 is used for creating the Python bindings for the C++ code. It's listed as a setup requirement in `setup.py` but you can also install it manually if preferred or if `setup_requires` causes issues in your environment:
    ```bash
    pip install pybind11
    ```

3.  **Build and Install the Package**:
    Navigate to the project's root directory (where `setup.py` is located after cloning) and run:
    ```bash
    pip install .
    ```
    This command invokes `setup.py` to build the C++ extension and install the package into your Python environment.
    Alternatively, for development, you can build in-place:
    ```bash
    python setup.py build_ext --inplace
    ```
    This creates the shared object file (e.g., `edit_distance_cpp.cpython-XX-architecture.so` or `.pyd`) directly in the current directory, allowing you to run `main.py` and `test_edit_distance.py` without installing the package globally.

## Usage after Installation

If you have installed the package using `pip install .` or built it in-place using `python setup.py build_ext --inplace`, you can then use the module.

### Run the Example

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

## Performance

The C++ implementation of edit distance and k-closest word searching offers a significant performance improvement over a pure Python equivalent. The exact speedup depends on factors such as vocabulary size, the number of target words, average string lengths, and the specific hardware.

The Wagner-Fischer algorithm for Levenshtein distance has a time complexity of O(m*n), where *m* and *n* are the lengths of the two strings being compared. Finding the *k* closest words involves performing this calculation for each of the *V* words in the vocabulary against a target word, followed by a sort (approximately *V* log *V*). This process is repeated for each of the *T* target words.

Due to compiled code execution, more efficient string handling, and tighter loops, the C++ version typically outperforms Python by a considerable margin, often by one to two orders of magnitude (e.g., 10x to 100x faster) for reasonably large datasets.

You can run a comparative benchmark using the provided `benchmark.py` script:
```bash
python benchmark.py
```
This script will generate sample data, run both the C++ extension and a pure Python implementation, and report the time taken and the calculated speedup. Ensure the C++ module is built (`python setup.py build_ext --inplace` or `pip install .`) before running the benchmark for the C++ version to be included.
