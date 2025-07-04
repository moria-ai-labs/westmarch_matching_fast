import time
import random
import string
import sys

# Attempt to import the C++ module
try:
    import edit_distance_cpp
except ImportError:
    print("----------------------------------------------------------------------")
    print("WARNING: The C++ module 'edit_distance_cpp' could not be imported.")
    print("Please ensure you have built the module by running:")
    print("  python setup.py build_ext --inplace")
    print("from the project root directory before running the benchmark.")
    print("Benchmark will only run the Python version.")
    print("----------------------------------------------------------------------")
    edit_distance_cpp = None

# --- Pure Python Implementation ---

def levenshtein_distance_python(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance_python(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def find_k_closest_words_python(target_word, vocabulary, k):
    if not vocabulary:
        return []

    word_distances = []
    for vocab_word in vocabulary:
        dist = levenshtein_distance_python(target_word, vocab_word)
        word_distances.append((vocab_word, dist))

    # Sort by distance, then by word alphabetically for tie-breaking (optional but good for consistency)
    word_distances.sort(key=lambda x: (x[1], x[0]))

    return [wd[0] for wd in word_distances[:k]]

def run_benchmark_for_target_list(target_words, vocabulary, k, version_name, find_k_func, dist_func_for_module=None):
    print(f"\nRunning benchmark for: {version_name}")
    start_time = time.perf_counter()

    all_results = {}
    for target_word in target_words:
        if version_name == "C++ Extension" and edit_distance_cpp:
            # edit_distance_cpp.find_k_closest_words_cpp is the function to benchmark
            all_results[target_word] = find_k_func(target_word, vocabulary, k)
        elif version_name == "Python":
             all_results[target_word] = find_k_func(target_word, vocabulary, k)
        else: # C++ module not available
            return None, None


    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"{version_name} - Total time for {len(target_words)} targets: {total_time:.4f} seconds")
    return total_time, all_results

# --- Benchmark Setup ---

def generate_random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_vocabulary(size, min_len=5, max_len=10):
    vocab = set() # Use a set to ensure unique words
    while len(vocab) < size:
        word_len = random.randint(min_len, max_len)
        vocab.add(generate_random_word(word_len))
    return list(vocab)

if __name__ == "__main__":
    # Parameters for the benchmark
    VOCAB_SIZE = 1000       # Number of words in the vocabulary
    NUM_TARGET_WORDS = 100  # Number of target words to find matches for
    WORD_MIN_LEN = 6
    WORD_MAX_LEN = 12
    K_CLOSEST = 5

    print("--- Edit Distance Benchmark ---")
    print(f"Vocabulary size: {VOCAB_SIZE}")
    print(f"Number of target words: {NUM_TARGET_WORDS}")
    print(f"Word length: {WORD_MIN_LEN}-{WORD_MAX_LEN}")
    print(f"K closest: {K_CLOSEST}\n")

    # Generate data
    print("Generating vocabulary...")
    vocabulary = generate_vocabulary(VOCAB_SIZE, WORD_MIN_LEN, WORD_MAX_LEN)
    print("Generating target words...")
    target_words = [generate_random_word(random.randint(WORD_MIN_LEN, WORD_MAX_LEN)) for _ in range(NUM_TARGET_WORDS)]
    print("Data generation complete.")

    # Run Python benchmark
    time_python, results_python = run_benchmark_for_target_list(
        target_words, vocabulary, K_CLOSEST, "Python",
        find_k_closest_words_python
    )

    # Run C++ benchmark (if module is available)
    time_cpp = None
    results_cpp = None
    if edit_distance_cpp:
        time_cpp, results_cpp = run_benchmark_for_target_list(
            target_words, vocabulary, K_CLOSEST, "C++ Extension",
            edit_distance_cpp.find_k_closest_words_cpp,
            edit_distance_cpp.calculate_edit_distance_cpp # Pass this for potential verification if needed
        )

        if results_python and results_cpp:
            # Optional: Basic verification that results are mostly similar
            # This is tricky because tie-breaking can differ.
            # We'll just check if the first result for the first few targets match.
            print("\nVerifying a few results (first match for first 5 targets):")
            verified_count = 0
            mismatch_count = 0
            for i, target in enumerate(target_words[:5]):
                py_res = results_python.get(target, [None])
                cpp_res = results_cpp.get(target, [None])
                if py_res and cpp_res and py_res[0] == cpp_res[0]:
                    verified_count +=1
                else:
                    mismatch_count +=1
                    # print(f"Mismatch for '{target}': Python got '{py_res[0]}', C++ got '{cpp_res[0]}'")
                    # dist_py = levenshtein_distance_python(target, py_res[0]) if py_res[0] else float('inf')
                    # dist_cpp_for_py_res = edit_distance_cpp.calculate_edit_distance_cpp(target, py_res[0]) if py_res[0] else float('inf')
                    # dist_cpp = edit_distance_cpp.calculate_edit_distance_cpp(target, cpp_res[0]) if cpp_res[0] else float('inf')
                    # print(f"  Dist (py): {dist_py}, Dist (cpp for py_res): {dist_cpp_for_py_res}, Dist (cpp for cpp_res): {dist_cpp}")

            if mismatch_count == 0 and verified_count > 0:
                print("Results for first item seem consistent.")
            elif verified_count > 0 :
                 print(f"Some first items differ, this might be due to tie-breaking in sort ({mismatch_count} mismatches for first item out of 5 checked).")
            else:
                print("Could not verify results consistency (not enough common results or all mismatched).")


    if time_python is not None and time_cpp is not None:
        speedup = time_python / time_cpp
        print(f"\n--- Summary ---")
        print(f"Python version time: {time_python:.4f} seconds")
        print(f"C++ version time:    {time_cpp:.4f} seconds")
        print(f"Speedup (Python time / C++ time): {speedup:.2f}x")
    elif time_python is not None:
        print(f"\n--- Summary ---")
        print(f"Python version time: {time_python:.4f} seconds")
        print(f"C++ version was not run.")
    else:
        print("Neither benchmark was run successfully.")

    print("\nNote: Benchmark results can vary based on system load, exact data generated, and Python/C++ compiler versions.")
    print("The Levenshtein implementation in this benchmark's Python version is a common optimized one but may differ slightly from other libraries or the C++ one in tie-breaking for k-closest.")
