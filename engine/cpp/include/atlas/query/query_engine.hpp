#pragma once

#include "atlas/graph/knowledge_graph.hpp"

#include <cstddef>
#include <string>
#include <string_view>
#include <vector>

namespace atlas {

struct SearchResult {
    Concept node;
    double score{};
    std::vector<std::string> matched_fields;
};

class QueryEngine {
public:
    explicit QueryEngine(const KnowledgeGraph& graph) noexcept;

    [[nodiscard]] std::vector<SearchResult> search(std::string_view query, std::size_t limit = 10) const;
    [[nodiscard]] std::vector<Concept> by_tag(std::string_view tag) const;

private:
    const KnowledgeGraph& graph_;
};

} // namespace atlas
