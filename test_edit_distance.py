import unittest
import sys
import os

# Attempt to import the C++ module
# This assumes the module has been built and is in the current directory or Python path
try:
    import edit_distance_cpp
except ImportError:
    print("----------------------------------------------------------------------")
    print("ERROR: The C++ module 'edit_distance_cpp' could not be imported.")
    print("Please ensure you have built the module by running:")
    print("  python setup.py build_ext --inplace")
    print("from the project root directory before running tests.")
    print("----------------------------------------------------------------------")
    # To allow tests to be discovered but fail gracefully if module not built
    edit_distance_cpp = None

@unittest.skipIf(edit_distance_cpp is None, "C++ module not compiled or not found")
class TestEditDistance(unittest.TestCase):

    def test_calculate_edit_distance_cpp(self):
        self.assertEqual(edit_distance_cpp.calculate_edit_distance_cpp("kitten", "sitting"), 3)
        self.assertEqual(edit_distance_cpp.calculate_edit_distance_cpp("flaw", "lawn"), 2)
        self.assertEqual(edit_distance_cpp.calculate_edit_distance_cpp("apple", "apply"), 1)
        self.assertEqual(edit_distance_cpp.calculate_edit_distance_cpp("apple", "apple"), 0)
        self.assertEqual(edit_distance_cpp.calculate_edit_distance_cpp("", "apple"), 5)
        self.assertEqual(edit_distance_cpp.calculate_edit_distance_cpp("apple", ""), 5)
        self.assertEqual(edit_distance_cpp.calculate_edit_distance_cpp("", ""), 0)
        self.assertEqual(edit_distance_cpp.calculate_edit_distance_cpp("sunday", "saturday"), 3)

    def test_find_k_closest_words_cpp(self):
        vocabulary = [
            "apple", "apply", "apricot", "banana", "bandana", "orange",
            "orangutan", "grape", "grappa", "kiwi", "lime", "lemon"
        ]

        # Test case 1
        target1 = "appel"
        k1 = 3
        expected1 = ["apple", "apply", "grape"] # apple (1), apply (2), grape (2), apricot (3)
        # Note: order among same-distance words might vary if not stable sort, but C++ std::sort is stable.
        # Let's check for content, order matters for top-k if distances are distinct.
        # If distances are same, original order from vocab (after sorting by distance) matters.
        # Our C++ sort is on WordDistance objects, then we pick top k.
        # `apple` (dist 1), `apply` (dist 2 from appel), `grape` (dist 2 from appel)
        # `apricot` (dist 3 from appel)
        # `lemon` (dist 3 from appel)
        # `orange` (dist 3 from appel)
        # So, ["apple", "apply", "grape"] or ["apple", "grape", "apply"] are both valid if sort is not stable for equivalent comparison.
        # std::sort is not guaranteed to be stable, but std::stable_sort is.
        # However, we sort WordDistance structs, and if distances are equal, original order is preserved if WordDistance comparison is strict.
        # Let's verify the specific output based on our implementation.
        # calculateEditDistance("appel", "apple") = 1
        # calculateEditDistance("appel", "apply") = 2
        # calculateEditDistance("appel", "apricot") = 3
        # calculateEditDistance("appel", "banana") = 4
        # calculateEditDistance("appel", "bandana") = 5
        # calculateEditDistance("appel", "orange") = 3
        # calculateEditDistance("appel", "orangutan") = 6
        # calculateEditDistance("appel", "grape") = 2
        # calculateEditDistance("appel", "grappa") = 3
        # calculateEditDistance("appel", "kiwi") = 5
        # calculateEditDistance("appel", "lime") = 4
        # calculateEditDistance("appel", "lemon") = 3

        # Distances:
        # apple: 1
        # apply: 2
        # grape: 2
        # apricot: 3
        # orange: 3
        # grappa: 3
        # lemon: 3
        # banana: 4
        # lime: 4
        # bandana: 5
        # kiwi: 5
        # orangutan: 6

        # Sorted by distance (then original vocab order for ties):
        # {apple, 1}, {apply, 2}, {grape, 2}, {apricot, 3}, {orange, 3}, {grappa, 3}, {lemon, 3}, ...
        # So top 3 should be apple, apply, grape (order of apply/grape depends on their original relative order if sort not stable for objects)
        # Our std::sort on vector of WordDistance: if distances are equal, the relative order of elements with equal distances is not guaranteed.
        # To be safe, we should check for set equality for words with same distance.
        # For k=3, words are: apple (1), apply (2), grape (2). Result: ["apple", "apply", "grape"] or ["apple", "grape", "apply"]

        result1 = edit_distance_cpp.find_k_closest_words_cpp(target1, vocabulary, k1)
        self.assertEqual(result1[0], "apple") # Must be apple
        self.assertIn("apply", result1[1:])
        self.assertIn("grape", result1[1:])
        self.assertEqual(len(result1), 3)


        # Test case 2
        target2 = "oranje"
        k2 = 2
        # calculateEditDistance("oranje", "orange") = 1
        # calculateEditDistance("oranje", "orangutan") = 3
        # calculateEditDistance("oranje", "apply") = 4
        # calculateEditDistance("oranje", "apricot") = 3
        # calculateEditDistance("oranje", "grape") = 3
        # calculateEditDistance("oranje", "grappa") = 4
        # ...
        # Distances:
        # orange: 1
        # orangutan: 3
        # apricot: 3
        # grape: 3
        # apply: 4
        # grappa: 4
        # lemon: 4
        # apple: 5
        # banana: 5
        # bandana: 6
        # lime: 5
        # kiwi: 6
        # Sorted: {orange, 1}, {apricot, 3}, {orangutan, 3}, {grape, 3}, ...
        # Top 2: orange, and one of (apricot, orangutan, grape)
        expected_first2 = "orange"
        expected_second_options2 = ["apricot", "orangutan", "grape"] # order within these might vary
        result2 = edit_distance_cpp.find_k_closest_words_cpp(target2, vocabulary, k2)
        self.assertEqual(result2[0], expected_first2)
        self.assertIn(result2[1], expected_second_options2)
        self.assertEqual(len(result2), 2)

        # Test case 3: k is larger than vocabulary size
        target3 = "kiwi"
        k3 = 20
        # Expected: all vocabulary words, sorted by distance to "kiwi"
        result3 = edit_distance_cpp.find_k_closest_words_cpp(target3, vocabulary, k3)
        self.assertEqual(len(result3), len(vocabulary))
        self.assertEqual(result3[0], "kiwi") # distance 0

        # Test case 4: Empty vocabulary
        target4 = "apple"
        k4 = 3
        expected4 = []
        result4 = edit_distance_cpp.find_k_closest_words_cpp(target4, [], k4)
        self.assertEqual(result4, expected4)

        # Test case 5: k=0
        target5 = "apple"
        k5 = 0
        expected5 = []
        result5 = edit_distance_cpp.find_k_closest_words_cpp(target5, vocabulary, k5)
        self.assertEqual(result5, expected5)

        # Test case 6: Exact match is present
        target6 = "banana"
        k6 = 3
        result6 = edit_distance_cpp.find_k_closest_words_cpp(target6, vocabulary, k6)
        self.assertEqual(result6[0], "banana") # dist 0
        # Next closest to "banana":
        # bandana: dist 1
        # apple: dist 3
        # apply: dist 4
        # apricot: dist 3
        # orange: dist 3
        # orangutan: dist 5
        # grape: dist 3
        # grappa: dist 4
        # kiwi: dist 4
        # lime: dist 4
        # lemon: dist 3
        # Distances:
        # banana: 0
        # bandana: 1
        # apple: 3
        # apricot: 3
        # orange: 3
        # grape: 3
        # lemon: 3
        # apply: 4
        # grappa: 4
        # kiwi: 4
        # lime: 4
        # orangutan: 5
        # Expected for k=3: "banana", "bandana", and one of ("apple", "apricot", "orange", "grape", "lemon")
        self.assertEqual(result6[1], "bandana")
        self.assertIn(result6[2], ["apple", "apricot", "orange", "grape", "lemon"])
        self.assertEqual(len(result6), 3)


if __name__ == '__main__':
    # This allows running the tests from the command line:
    # python test_edit_distance.py
    #
    # It's important to run `python setup.py build_ext --inplace` first.
    if edit_distance_cpp is None:
        sys.exit(1) # Exit with error if module couldn't be loaded.
    unittest.main()
