#include <string>
#include <vector>
#include <algorithm>
#include <iostream>

// Function to calculate Levenshtein distance between two strings
int calculateEditDistance(const std::string& s1, const std::string& s2) {
    const size_t len1 = s1.length(), len2 = s2.length();
    std::vector<std::vector<int>> d(len1 + 1, std::vector<int>(len2 + 1));

    for (size_t i = 0; i <= len1; ++i) {
        d[i][0] = i;
    }
    for (size_t j = 0; j <= len2; ++j) {
        d[0][j] = j;
    }

    for (size_t i = 1; i <= len1; ++i) {
        for (size_t j = 1; j <= len2; ++j) {
            int cost = (s1[i - 1] == s2[j - 1]) ? 0 : 1;
            d[i][j] = std::min({ d[i - 1][j] + 1,         // Deletion
                                 d[i][j - 1] + 1,         // Insertion
                                 d[i - 1][j - 1] + cost }); // Substitution
        }
    }
    return d[len1][len2];
}

int main() {
    std::string target = "appel";
    std::vector<std::string> vocabulary = {
        "apple", "apply", "apricot", "banana", "bandana", "orange",
        "orangutan", "grape", "grappa", "kiwi", "lime", "lemon"
    };

    std::cout << "Distances from '" << target << "':" << std::endl;
    for (const auto& vocab_word : vocabulary) {
        std::cout << "  '" << vocab_word << "': " << calculateEditDistance(target, vocab_word) << std::endl;
    }
    std::cout << "\nKitten/Sitting check: " << calculateEditDistance("kitten", "sitting") << std::endl;
    return 0;
}
