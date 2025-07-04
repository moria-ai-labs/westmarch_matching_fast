#include <string>
#include <vector>
#include <algorithm>

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

// Structure to store word and its distance
struct WordDistance {
    std::string word;
    int distance;

    // Comparator for sorting
    bool operator<(const WordDistance& other) const {
        return distance < other.distance;
    }
};

// Function to find k closest words from vocabulary for a target word
std::vector<std::string> findKClosestWords(
    const std::string& target_word,
    const std::vector<std::string>& vocabulary,
    int k
) {
    std::vector<WordDistance> word_distances;

    for (const auto& vocab_word : vocabulary) {
        int dist = calculateEditDistance(target_word, vocab_word);
        word_distances.push_back({vocab_word, dist});
    }

    // Sort by distance
    std::sort(word_distances.begin(), word_distances.end());

    std::vector<std::string> closest_words;
    for (int i = 0; i < std::min((int)word_distances.size(), k); ++i) {
        closest_words.push_back(word_distances[i].word);
    }

    return closest_words;
}
