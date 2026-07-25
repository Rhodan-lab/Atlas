#include "atlas/query/query_engine.hpp"

#include <algorithm>
#include <cctype>
#include <sstream>
#include <unordered_set>

namespace atlas {
namespace {

std::string lowercase(std::string_view value) {
    std::string result(value);
    std::transform(result.begin(), result.end(), result.begin(), [](unsigned char ch) {
        return static_cast<char>(std::tolower(ch));
    });
    return result;
}

std::vector<std::string> tokenize(std::string_view value) {
    std::string normalized;
    normalized.reserve(value.size());
    for (const unsigned char ch : value) {
        normalized.push_back(std::isalnum(ch) != 0 ? static_cast<char>(std::tolower(ch)) : ' ');
    }

    std::istringstream input(normalized);
    std::vector<std::string> tokens;
    for (std::string token; input >> token;) {
        tokens.push_back(std::move(token));
    }
    return tokens;
}

bool contains_token(std::string_view field, std::string_view token) {
    return lowercase(field).find(lowercase(token)) != std::string::npos;
}

} // namespace

QueryEngine::QueryEngine(const KnowledgeGraph& graph) noexcept : graph_(graph) {}

std::vector<SearchResult> QueryEngine::search(std::string_view query, std::size_t limit) const {
    const auto tokens = tokenize(query);
    if (tokens.empty() || limit == 0) {
        return {};
    }

    std::vector<SearchResult> results;
    for (const auto& node : graph_.concepts()) {
        double score = 0.0;
        std::unordered_set<std::string> fields;

        for (const auto& token : tokens) {
            if (contains_token(node.title, token)) {
                score += 5.0;
                fields.insert("title");
            }
            if (contains_token(node.summary, token)) {
                score += 2.0;
                fields.insert("summary");
            }
            for (const auto& tag : node.tags) {
                if (contains_token(tag, token)) {
                    score += 3.0;
                    fields.insert("tags");
                }
            }
            for (const auto& source : node.sources) {
                if (contains_token(source.title, token) || contains_token(source.locator, token)) {
                    score += 1.0;
                    fields.insert("sources");
                }
            }
        }

        if (score > 0.0) {
            SearchResult result;
            result.node = node;
            result.score = score;
            result.matched_fields.assign(fields.begin(), fields.end());
            std::sort(result.matched_fields.begin(), result.matched_fields.end());
            results.push_back(std::move(result));
        }
    }

    std::sort(results.begin(), results.end(), [](const SearchResult& lhs, const SearchResult& rhs) {
        if (lhs.score != rhs.score) {
            return lhs.score > rhs.score;
        }
        return lhs.node.title < rhs.node.title;
    });

    if (results.size() > limit) {
        results.resize(limit);
    }
    return results;
}

std::vector<Concept> QueryEngine::by_tag(std::string_view tag) const {
    std::vector<Concept> result;
    for (const auto& node : graph_.concepts()) {
        if (node.has_tag(tag)) {
            result.push_back(node);
        }
    }
    return result;
}

} // namespace atlas
