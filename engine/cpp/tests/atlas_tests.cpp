#include "atlas/io/atlas_store.hpp"
#include "atlas/query/query_engine.hpp"

#include <cstdlib>
#include <filesystem>
#include <iostream>
#include <string>

namespace {

int failures = 0;

void expect(bool condition, const std::string& label) {
    if (!condition) {
        ++failures;
        std::cerr << "FAIL: " << label << '\n';
    }
}

atlas::KnowledgeGraph sample_graph() {
    atlas::KnowledgeGraph graph;
    expect(graph.add_concept({1, "Cell", "Basic unit of life", {"biology"}, {}}), "add first node");
    expect(graph.add_concept({2, "ATP", "Energy-carrying molecule", {"biology", "chemistry"}, {}}), "add second node");
    expect(graph.add_concept({3, "Respiration", "Process that produces ATP", {"biology"}, {}}), "add third node");
    expect(graph.add_relation({3, 2, "produces", 1.0, ""}), "add relation");
    expect(graph.add_relation({1, 3, "performs", 1.0, ""}), "add second relation");
    return graph;
}

} // namespace

int main() {
    auto graph = sample_graph();
    expect(graph.concept_count() == 3, "node count");
    expect(graph.relation_count() == 2, "relation count");
    expect(!graph.add_concept({1, "Duplicate", "", {}, {}}), "reject duplicate node");
    expect(!graph.add_relation({1, 99, "invalid", 1.0, ""}), "reject missing target");

    atlas::QueryEngine query(graph);
    const auto results = query.search("energy biology");
    expect(!results.empty(), "search returns results");
    expect(results.front().node.id == 2, "search ranking");
    expect(query.by_tag("BIOLOGY").size() == 3, "case-insensitive tag search");

    const auto path = graph.shortest_path(1, 2);
    expect(path.size() == 3, "shortest path through respiration");

    const auto file = std::filesystem::temp_directory_path() / "atlas-test.atlas";
    const auto save_result = atlas::AtlasStore::save(graph, file);
    expect(save_result.ok, "save graph");

    atlas::KnowledgeGraph loaded;
    const auto load_result = atlas::AtlasStore::load(loaded, file);
    expect(load_result.ok, "load graph");
    expect(loaded.concept_count() == graph.concept_count(), "round-trip node count");
    expect(loaded.relation_count() == graph.relation_count(), "round-trip relation count");
    std::filesystem::remove(file);

    if (failures != 0) {
        std::cerr << failures << " test(s) failed.\n";
        return EXIT_FAILURE;
    }
    std::cout << "All Atlas tests passed.\n";
    return EXIT_SUCCESS;
}
