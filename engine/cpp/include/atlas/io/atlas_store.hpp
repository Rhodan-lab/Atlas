#pragma once

#include "atlas/graph/knowledge_graph.hpp"

#include <filesystem>
#include <string>

namespace atlas {

struct StoreResult {
    bool ok{false};
    std::string message;
};

class AtlasStore {
public:
    [[nodiscard]] static StoreResult save(const KnowledgeGraph& graph, const std::filesystem::path& path);
    [[nodiscard]] static StoreResult load(KnowledgeGraph& graph, const std::filesystem::path& path);
};

} // namespace atlas
