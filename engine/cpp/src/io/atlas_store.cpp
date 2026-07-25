#include "atlas/io/atlas_store.hpp"

#include <fstream>
#include <iomanip>
#include <sstream>

namespace atlas {
namespace {

std::string join(const std::vector<std::string>& values, char separator) {
    std::ostringstream output;
    for (std::size_t index = 0; index < values.size(); ++index) {
        if (index != 0) {
            output << separator;
        }
        output << values[index];
    }
    return output.str();
}

std::vector<std::string> split(const std::string& value, char separator) {
    std::vector<std::string> result;
    std::istringstream input(value);
    for (std::string item; std::getline(input, item, separator);) {
        if (!item.empty()) {
            result.push_back(std::move(item));
        }
    }
    return result;
}

} // namespace

StoreResult AtlasStore::save(const KnowledgeGraph& graph, const std::filesystem::path& path) {
    std::ofstream output(path, std::ios::trunc);
    if (!output) {
        return {false, "Unable to open file for writing: " + path.string()};
    }

    output << "ATLAS\t1\n";
    for (const auto& node : graph.concepts()) {
        output << "C\t" << node.id << '\t'
               << std::quoted(node.title) << '\t'
               << std::quoted(node.summary) << '\t'
               << std::quoted(join(node.tags, '|')) << '\n';
        for (const auto& source : node.sources) {
            output << "S\t" << node.id << '\t'
                   << std::quoted(source.title) << '\t'
                   << std::quoted(source.locator) << '\n';
        }
    }

    for (const auto& relation : graph.relations()) {
        output << "R\t" << relation.from << '\t' << relation.to << '\t'
               << std::quoted(relation.type) << '\t' << relation.weight << '\t'
               << std::quoted(relation.note) << '\n';
    }

    if (!output.good()) {
        return {false, "Write failed: " + path.string()};
    }
    return {true, "Saved " + std::to_string(graph.concept_count()) + " concepts."};
}

StoreResult AtlasStore::load(KnowledgeGraph& graph, const std::filesystem::path& path) {
    std::ifstream input(path);
    if (!input) {
        return {false, "Unable to open file: " + path.string()};
    }

    std::string header;
    if (!std::getline(input, header) || header != "ATLAS\t1") {
        return {false, "Unsupported or invalid Atlas file."};
    }

    KnowledgeGraph candidate;
    std::vector<std::pair<ConceptId, SourceReference>> pending_sources;
    std::vector<Relation> pending_relations;

    std::string line;
    std::size_t line_number = 1;
    while (std::getline(input, line)) {
        ++line_number;
        if (line.empty()) {
            continue;
        }

        std::istringstream row(line);
        char record_type = '\0';
        char tab = '\0';
        if (!row.get(record_type) || !row.get(tab) || tab != '\t') {
            return {false, "Malformed record prefix at line " + std::to_string(line_number)};
        }

        const auto consume_tab = [&row]() {
            char separator = '\0';
            return static_cast<bool>(row.get(separator)) && separator == '\t';
        };

        if (record_type == 'C') {
            Concept node;
            std::string tags;
            if (!(row >> node.id) || !consume_tab() ||
                !(row >> std::quoted(node.title)) || !consume_tab() ||
                !(row >> std::quoted(node.summary)) || !consume_tab() ||
                !(row >> std::quoted(tags))) {
                return {false, "Malformed concept at line " + std::to_string(line_number)};
            }
            node.tags = split(tags, '|');
            if (!candidate.add_concept(std::move(node))) {
                return {false, "Invalid or duplicate concept at line " + std::to_string(line_number)};
            }
        } else if (record_type == 'S') {
            ConceptId concept_id{};
            SourceReference source;
            if (!(row >> concept_id) || !consume_tab() ||
                !(row >> std::quoted(source.title)) || !consume_tab() ||
                !(row >> std::quoted(source.locator))) {
                return {false, "Malformed source at line " + std::to_string(line_number)};
            }
            pending_sources.emplace_back(concept_id, std::move(source));
        } else if (record_type == 'R') {
            Relation relation;
            if (!(row >> relation.from) || !consume_tab() ||
                !(row >> relation.to) || !consume_tab() ||
                !(row >> std::quoted(relation.type)) || !consume_tab() ||
                !(row >> relation.weight) || !consume_tab() ||
                !(row >> std::quoted(relation.note))) {
                return {false, "Malformed relation at line " + std::to_string(line_number)};
            }
            pending_relations.push_back(std::move(relation));
        } else {
            return {false, "Unknown record type at line " + std::to_string(line_number)};
        }
    }

    for (auto& [concept_id, source] : pending_sources) {
        Concept* node = candidate.find_concept(concept_id);
        if (node == nullptr) {
            return {false, "Source references a missing concept."};
        }
        node->sources.push_back(std::move(source));
    }

    for (auto& relation : pending_relations) {
        if (!candidate.add_relation(std::move(relation))) {
            return {false, "A relation is invalid, duplicated, or references a missing concept."};
        }
    }

    graph = std::move(candidate);
    return {true, "Loaded " + std::to_string(graph.concept_count()) + " concepts."};
}

} // namespace atlas
