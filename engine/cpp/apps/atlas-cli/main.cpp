#include "atlas/io/atlas_store.hpp"
#include "atlas/query/query_engine.hpp"

#include <cstdlib>
#include <filesystem>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <string_view>
#include <vector>

namespace {

using atlas::Concept;
using atlas::ConceptId;
using atlas::KnowledgeGraph;
using atlas::Relation;

void print_help() {
    std::cout << R"(Atlas Knowledge Engine

Usage:
  atlas demo
  atlas validate <file>
  atlas stats <file>
  atlas stats-json <file>
  atlas list <file>
  atlas list-json <file>
  atlas show <file> <concept-id>
  atlas search <file> <query...>
  atlas tag <file> <tag>
  atlas neighbors <file> <concept-id>
  atlas neighbors-json <file> <concept-id>
  atlas path <file> <start-id> <goal-id>
  atlas path-json <file> <start-id> <goal-id>
  atlas add-concept <file> <title> <summary> [tag1,tag2]
  atlas add-relation <file> <from-id> <to-id> <type> [note]

Text commands are intended for people. Commands ending in -json are stable
process boundaries for the TypeScript API and other tools.
)";
}

std::string join_args(int argc, char** argv, int start) {
    std::ostringstream result;
    for (int index = start; index < argc; ++index) {
        if (index != start) {
            result << ' ';
        }
        result << argv[index];
    }
    return result.str();
}

std::vector<std::string> split_tags(const std::string& text) {
    std::vector<std::string> tags;
    std::istringstream input(text);
    for (std::string tag; std::getline(input, tag, ',');) {
        if (!tag.empty()) {
            tags.push_back(std::move(tag));
        }
    }
    return tags;
}

bool parse_id(std::string_view text, ConceptId& id) {
    try {
        std::size_t consumed = 0;
        id = std::stoull(std::string(text), &consumed);
        return consumed == text.size() && id != 0;
    } catch (...) {
        return false;
    }
}

bool load_graph(const std::filesystem::path& file, KnowledgeGraph& graph) {
    const auto result = atlas::AtlasStore::load(graph, file);
    if (!result.ok) {
        std::cerr << "error: " << result.message << '\n';
    }
    return result.ok;
}

std::string json_escape(std::string_view value) {
    std::ostringstream output;
    for (const unsigned char ch : value) {
        switch (ch) {
        case '"': output << "\\\""; break;
        case '\\': output << "\\\\"; break;
        case '\b': output << "\\b"; break;
        case '\f': output << "\\f"; break;
        case '\n': output << "\\n"; break;
        case '\r': output << "\\r"; break;
        case '\t': output << "\\t"; break;
        default:
            if (ch < 0x20U) {
                output << "\\u" << std::hex << std::setw(4) << std::setfill('0')
                       << static_cast<unsigned int>(ch) << std::dec;
            } else {
                output << static_cast<char>(ch);
            }
        }
    }
    return output.str();
}

void print_string_array(const std::vector<std::string>& values) {
    std::cout << '[';
    for (std::size_t index = 0; index < values.size(); ++index) {
        if (index != 0) {
            std::cout << ',';
        }
        std::cout << '"' << json_escape(values[index]) << '"';
    }
    std::cout << ']';
}

void print_concept_json(const Concept& node) {
    std::cout << "{\"id\":" << node.id
              << ",\"title\":\"" << json_escape(node.title)
              << "\",\"summary\":\"" << json_escape(node.summary)
              << "\",\"tags\":";
    print_string_array(node.tags);
    std::cout << ",\"sources\":[";
    for (std::size_t index = 0; index < node.sources.size(); ++index) {
        if (index != 0) {
            std::cout << ',';
        }
        const auto& source = node.sources[index];
        std::cout << "{\"title\":\"" << json_escape(source.title)
                  << "\",\"locator\":\"" << json_escape(source.locator) << "\"}";
    }
    std::cout << "]}";
}

void print_relation_json(const Relation& relation) {
    std::cout << "{\"from\":" << relation.from
              << ",\"to\":" << relation.to
              << ",\"type\":\"" << json_escape(relation.type)
              << "\",\"weight\":" << relation.weight
              << ",\"note\":\"" << json_escape(relation.note) << "\"}";
}

void print_concept(const Concept& node) {
    std::cout << '[' << node.id << "] " << node.title << '\n';
    std::cout << "  " << node.summary << '\n';
    if (!node.tags.empty()) {
        std::cout << "  tags:";
        for (const auto& tag : node.tags) {
            std::cout << ' ' << tag;
        }
        std::cout << '\n';
    }
}

KnowledgeGraph make_demo_graph() {
    KnowledgeGraph graph;
    static_cast<void>(graph.add_concept({1, "Knowledge Graph", "A network representation of entities and meaningful relations.", {"knowledge", "graph", "foundation"}, {{"Atlas Architecture", "docs/architecture.md"}}}));
    static_cast<void>(graph.add_concept({2, "Concept", "The smallest addressable unit of knowledge in Atlas.", {"knowledge", "model"}, {}}));
    static_cast<void>(graph.add_concept({3, "Relation", "A typed and weighted connection between two concepts.", {"graph", "model"}, {}}));
    static_cast<void>(graph.add_concept({4, "Query Engine", "Ranks concepts by title, summary, tags, and sources.", {"search", "software"}, {}}));
    static_cast<void>(graph.add_concept({5, "Evidence", "A source reference supporting a concept or claim.", {"research", "trust"}, {}}));
    static_cast<void>(graph.add_relation({1, 2, "contains", 1.0, "Graphs are composed of concepts."}));
    static_cast<void>(graph.add_relation({1, 3, "contains", 1.0, "Graphs are connected by relations."}));
    static_cast<void>(graph.add_relation({4, 1, "searches", 1.0, "Queries operate over the graph."}));
    static_cast<void>(graph.add_relation({5, 2, "supports", 1.0, "Evidence can support a concept."}));
    return graph;
}

int command_demo() {
    auto graph = make_demo_graph();
    const std::filesystem::path path = "atlas-demo.atlas";
    const auto save_result = atlas::AtlasStore::save(graph, path);
    if (!save_result.ok) {
        std::cerr << "error: " << save_result.message << '\n';
        return EXIT_FAILURE;
    }
    std::cout << save_result.message << " File: " << path << '\n';

    atlas::QueryEngine query(graph);
    std::cout << "Search demo for 'graph knowledge':\n";
    for (const auto& result : query.search("graph knowledge")) {
        std::cout << "  " << result.score << "  " << result.node.title << '\n';
    }
    return EXIT_SUCCESS;
}

int print_neighbors_json(const KnowledgeGraph& graph, ConceptId id) {
    const Concept* center = graph.find_concept(id);
    if (center == nullptr) {
        std::cerr << "error: concept not found\n";
        return EXIT_FAILURE;
    }

    std::cout << "{\"concept\":";
    print_concept_json(*center);
    std::cout << ",\"outgoing\":[";
    const auto outgoing = graph.outgoing(id);
    for (std::size_t index = 0; index < outgoing.size(); ++index) {
        if (index != 0) {
            std::cout << ',';
        }
        std::cout << "{\"relation\":";
        print_relation_json(outgoing[index]);
        const Concept* target = graph.find_concept(outgoing[index].to);
        std::cout << ",\"concept\":";
        if (target == nullptr) {
            std::cout << "null";
        } else {
            print_concept_json(*target);
        }
        std::cout << '}';
    }
    std::cout << "],\"incoming\":[";
    const auto incoming = graph.incoming(id);
    for (std::size_t index = 0; index < incoming.size(); ++index) {
        if (index != 0) {
            std::cout << ',';
        }
        std::cout << "{\"relation\":";
        print_relation_json(incoming[index]);
        const Concept* source = graph.find_concept(incoming[index].from);
        std::cout << ",\"concept\":";
        if (source == nullptr) {
            std::cout << "null";
        } else {
            print_concept_json(*source);
        }
        std::cout << '}';
    }
    std::cout << "]}\n";
    return EXIT_SUCCESS;
}

int print_path_json(const KnowledgeGraph& graph, ConceptId start, ConceptId goal) {
    const auto path = graph.shortest_path(start, goal);
    std::cout << "{\"found\":" << (path.empty() ? "false" : "true") << ",\"path\":[";
    for (std::size_t index = 0; index < path.size(); ++index) {
        if (index != 0) {
            std::cout << ',';
        }
        const Concept* node = graph.find_concept(path[index]);
        if (node == nullptr) {
            std::cout << "null";
        } else {
            print_concept_json(*node);
        }
    }
    std::cout << "]}\n";
    return EXIT_SUCCESS;
}

} // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        print_help();
        return EXIT_SUCCESS;
    }

    const std::string command = argv[1];
    if (command == "help" || command == "--help" || command == "-h") {
        print_help();
        return EXIT_SUCCESS;
    }
    if (command == "demo") {
        return command_demo();
    }
    if (argc < 3) {
        std::cerr << "error: missing Atlas file\n";
        return EXIT_FAILURE;
    }

    const std::filesystem::path file = argv[2];
    KnowledgeGraph graph;

    if (command == "add-concept") {
        if (std::filesystem::exists(file) && !load_graph(file, graph)) {
            return EXIT_FAILURE;
        }
        if (argc < 5) {
            std::cerr << "usage: atlas add-concept <file> <title> <summary> [tag1,tag2]\n";
            return EXIT_FAILURE;
        }
        Concept node;
        node.id = graph.next_id();
        node.title = argv[3];
        node.summary = argv[4];
        if (argc >= 6) {
            node.tags = split_tags(argv[5]);
        }
        if (!graph.add_concept(node)) {
            std::cerr << "error: invalid concept\n";
            return EXIT_FAILURE;
        }
        const auto result = atlas::AtlasStore::save(graph, file);
        std::cout << (result.ok ? "Added concept " : "error: ") << node.id << " - " << result.message << '\n';
        return result.ok ? EXIT_SUCCESS : EXIT_FAILURE;
    }

    if (!load_graph(file, graph)) {
        return EXIT_FAILURE;
    }

    if (command == "validate") {
        std::cout << "valid: " << graph.concept_count() << " concepts, "
                  << graph.relation_count() << " relations\n";
        return EXIT_SUCCESS;
    }

    if (command == "stats") {
        std::cout << "concepts: " << graph.concept_count() << '\n';
        std::cout << "relations: " << graph.relation_count() << '\n';
        return EXIT_SUCCESS;
    }

    if (command == "stats-json") {
        std::cout << "{\"concepts\":" << graph.concept_count()
                  << ",\"relations\":" << graph.relation_count()
                  << ",\"formatVersion\":1}\n";
        return EXIT_SUCCESS;
    }

    if (command == "list" || command == "list-json") {
        const auto nodes = graph.concepts();
        if (command == "list") {
            for (const auto& node : nodes) {
                print_concept(node);
            }
        } else {
            std::cout << "{\"concepts\":[";
            for (std::size_t index = 0; index < nodes.size(); ++index) {
                if (index != 0) {
                    std::cout << ',';
                }
                print_concept_json(nodes[index]);
            }
            std::cout << "]}\n";
        }
        return EXIT_SUCCESS;
    }

    if (command == "show") {
        ConceptId id{};
        if (argc < 4 || !parse_id(argv[3], id)) {
            std::cerr << "error: valid concept ID required\n";
            return EXIT_FAILURE;
        }
        const Concept* node = graph.find_concept(id);
        if (node == nullptr) {
            std::cerr << "error: concept not found\n";
            return EXIT_FAILURE;
        }
        print_concept(*node);
        for (const auto& source : node->sources) {
            std::cout << "  source: " << source.title << " <" << source.locator << ">\n";
        }
        return EXIT_SUCCESS;
    }

    if (command == "search") {
        if (argc < 4) {
            std::cerr << "error: search query required\n";
            return EXIT_FAILURE;
        }
        atlas::QueryEngine query(graph);
        for (const auto& result : query.search(join_args(argc, argv, 3))) {
            std::cout << result.score << "\t" << result.node.id << "\t" << result.node.title << '\n';
        }
        return EXIT_SUCCESS;
    }

    if (command == "tag") {
        if (argc < 4) {
            std::cerr << "error: tag required\n";
            return EXIT_FAILURE;
        }
        atlas::QueryEngine query(graph);
        for (const auto& node : query.by_tag(argv[3])) {
            print_concept(node);
        }
        return EXIT_SUCCESS;
    }

    if (command == "neighbors" || command == "neighbors-json") {
        ConceptId id{};
        if (argc < 4 || !parse_id(argv[3], id)) {
            std::cerr << "error: valid concept ID required\n";
            return EXIT_FAILURE;
        }
        if (command == "neighbors-json") {
            return print_neighbors_json(graph, id);
        }
        for (const auto& relation : graph.outgoing(id)) {
            const auto* target = graph.find_concept(relation.to);
            std::cout << "-> " << relation.type << " -> " << (target ? target->title : "<missing>") << '\n';
        }
        for (const auto& relation : graph.incoming(id)) {
            const auto* source = graph.find_concept(relation.from);
            std::cout << "<- " << relation.type << " <- " << (source ? source->title : "<missing>") << '\n';
        }
        return EXIT_SUCCESS;
    }

    if (command == "path" || command == "path-json") {
        ConceptId start{};
        ConceptId goal{};
        if (argc < 5 || !parse_id(argv[3], start) || !parse_id(argv[4], goal)) {
            std::cerr << "error: valid start and goal IDs required\n";
            return EXIT_FAILURE;
        }
        if (command == "path-json") {
            return print_path_json(graph, start, goal);
        }
        const auto path = graph.shortest_path(start, goal);
        if (path.empty()) {
            std::cout << "No path found.\n";
            return EXIT_SUCCESS;
        }
        for (std::size_t index = 0; index < path.size(); ++index) {
            if (index != 0) {
                std::cout << " -> ";
            }
            const auto* node = graph.find_concept(path[index]);
            std::cout << (node ? node->title : "<missing>");
        }
        std::cout << '\n';
        return EXIT_SUCCESS;
    }

    if (command == "add-relation") {
        if (argc < 6) {
            std::cerr << "usage: atlas add-relation <file> <from-id> <to-id> <type> [note]\n";
            return EXIT_FAILURE;
        }
        Relation relation;
        if (!parse_id(argv[3], relation.from) || !parse_id(argv[4], relation.to)) {
            std::cerr << "error: valid relation endpoint IDs required\n";
            return EXIT_FAILURE;
        }
        relation.type = argv[5];
        if (argc >= 7) {
            relation.note = join_args(argc, argv, 6);
        }
        if (!graph.add_relation(relation)) {
            std::cerr << "error: invalid, duplicate, or unresolved relation\n";
            return EXIT_FAILURE;
        }
        const auto result = atlas::AtlasStore::save(graph, file);
        std::cout << (result.ok ? "Added relation - " : "error: ") << result.message << '\n';
        return result.ok ? EXIT_SUCCESS : EXIT_FAILURE;
    }

    std::cerr << "error: unknown command '" << command << "'\n";
    print_help();
    return EXIT_FAILURE;
}
