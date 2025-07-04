# This is a placeholder for where the compiled C++ module will be imported.
# We expect a file named something like `edit_distance_cpp.cpython-38-x86_64-linux-gnu.so`
# (the exact name depends on the Python version and OS) to be in the same directory
# or in the Python path after compilation.

# Import the C++ module (name defined in PYBIND11_MODULE)
try:
    import edit_distance_cpp
except ImportError as e:
    print(f"Error importing C++ module: {e}")
    print("Please make sure you have compiled the C++ extension (e.g., using setup.py).")
    print("The compiled file (e.g., edit_distance_cpp.so or edit_distance_cpp.pyd) should be in the current directory or Python path.")
    edit_distance_cpp = None

def find_closest_matches_python(vocabulary, target_words, k):
    """
    Finds the k closest words from the vocabulary for each target word using the C++ extension.
    """
    if not edit_distance_cpp:
        print("C++ module not loaded. Cannot proceed.")
        return {}

    results = {}
    for target in target_words:
        closest_words = edit_distance_cpp.find_k_closest_words_cpp(target, vocabulary, k)
        results[target] = closest_words
    return results

if __name__ == "__main__":
    # Sample data
    vocabulary = [
        "apple", "apply", "apricot", "banana", "bandana", "orange",
        "orangutan", "grape", "grappa", "kiwi", "lime", "lemon"
    ]
    target_words = ["appel", "oranje", "grp", "lim"]
    k = 3

    print(f"Vocabulary: {vocabulary}")
    print(f"Target Words: {target_words}")
    print(f"Finding {k} closest words for each target...\n")

    closest_matches = find_closest_matches_python(vocabulary, target_words, k)

    if closest_matches:
        for target, matches in closest_matches.items():
            print(f"Target: '{target}'")
            if matches:
                print(f"  Closest {k}: {', '.join(matches)}")
            else:
                print(f"  No matches found in vocabulary.")
            # For verification, let's also print distances using the C++ direct function
            if edit_distance_cpp:
                print("  Distances to matches:")
                for match in matches:
                    dist = edit_distance_cpp.calculate_edit_distance_cpp(target, match)
                    print(f"    - '{match}': {dist}")
            print("-" * 20)

    # Example of direct distance calculation
    if edit_distance_cpp:
        word1 = "kitten"
        word2 = "sitting"
        distance = edit_distance_cpp.calculate_edit_distance_cpp(word1, word2)
        print(f"\nDirect distance calculation example:")
        print(f"Distance between '{word1}' and '{word2}' is: {distance}")

        word1 = "flaw"
        word2 = "lawn"
        distance = edit_distance_cpp.calculate_edit_distance_cpp(word1, word2)
        print(f"Distance between '{word1}' and '{word2}' is: {distance}")
    else:
        print("\nDirect distance calculation example skipped as C++ module is not loaded.")
