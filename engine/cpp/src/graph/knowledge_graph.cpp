#include "atlas/graph/knowledge_graph.hpp"

#include <algorithm>
#include <queue>
#include <unordered_map>
#include <unordered_set>

namespace atlas {

bool KnowledgeGraph::add_concept(Concept node) {
    if (!node.valid() || concepts_.contains(node.id)) {
        return false;
    }
    concepts_.emplace(node.id, std::move(node));
    return true;
}

bool KnowledgeGraph::upsert_concept(Concept node) {
    if (!node.valid()) {
        return false;
    }
    concepts_.insert_or_assign(node.id, std::move(node));
    return true;
}

bool KnowledgeGraph::remove_concept(ConceptId id) {
    if (concepts_.erase(id) == 0) {
        return false;
    }
    std::erase_if(relations_, [id](const Relation& relation) {
        return relation.from == id || relation.to == id;
    });
    return true;
}

bool KnowledgeGraph::add_relation(Relation relation) {
    if (!relation.valid() || !concepts_.contains(relation.from) || !concepts_.contains(relation.to)) {
        return false;
    }

    const bool duplicate = std::any_of(relations_.begin(), relations_.end(), [&](const Relation& existing) {
        return existing.from == relation.from && existing.to == relation.to && existing.type == relation.type;
    });
    if (duplicate) {
        return false;
    }

    relations_.push_back(std::move(relation));
    return true;
}

bool KnowledgeGraph::remove_relation(ConceptId from, ConceptId to, const std::string& type) {
    const auto old_size = relations_.size();
    std::erase_if(relations_, [&](const Relation& relation) {
        return relation.from == from && relation.to == to && relation.type == type;
    });
    return relations_.size() != old_size;
}

const Concept* KnowledgeGraph::find_concept(ConceptId id) const noexcept {
    const auto it = concepts_.find(id);
    return it == concepts_.end() ? nullptr : &it->second;
}

Concept* KnowledgeGraph::find_concept(ConceptId id) noexcept {
    const auto it = concepts_.find(id);
    return it == concepts_.end() ? nullptr : &it->second;
}

std::vector<Concept> KnowledgeGraph::concepts() const {
    std::vector<Concept> result;
    result.reserve(concepts_.size());
    for (const auto& [id, node] : concepts_) {
        static_cast<void>(id);
        result.push_back(node);
    }
    std::sort(result.begin(), result.end(), [](const Concept& lhs, const Concept& rhs) {
        return lhs.id < rhs.id;
    });
    return result;
}

const std::vector<Relation>& KnowledgeGraph::relations() const noexcept {
    return relations_;
}

std::vector<Relation> KnowledgeGraph::outgoing(ConceptId id) const {
    std::vector<Relation> result;
    for (const auto& relation : relations_) {
        if (relation.from == id) {
            result.push_back(relation);
        }
    }
    return result;
}

std::vector<Relation> KnowledgeGraph::incoming(ConceptId id) const {
    std::vector<Relation> result;
    for (const auto& relation : relations_) {
        if (relation.to == id) {
            result.push_back(relation);
        }
    }
    return result;
}

std::vector<ConceptId> KnowledgeGraph::shortest_path(ConceptId start, ConceptId goal) const {
    if (!concepts_.contains(start) || !concepts_.contains(goal)) {
        return {};
    }
    if (start == goal) {
        return {start};
    }

    std::queue<ConceptId> frontier;
    std::unordered_set<ConceptId> visited;
    std::unordered_map<ConceptId, ConceptId> parent;

    frontier.push(start);
    visited.insert(start);

    while (!frontier.empty()) {
        const ConceptId current = frontier.front();
        frontier.pop();

        for (const auto& relation : relations_) {
            ConceptId next = 0;
            if (relation.from == current) {
                next = relation.to;
            } else if (relation.to == current) {
                next = relation.from;
            } else {
                continue;
            }

            if (visited.contains(next)) {
                continue;
            }

            visited.insert(next);
            parent[next] = current;
            if (next == goal) {
                std::vector<ConceptId> path{goal};
                while (path.back() != start) {
                    path.push_back(parent.at(path.back()));
                }
                std::reverse(path.begin(), path.end());
                return path;
            }
            frontier.push(next);
        }
    }

    return {};
}

std::size_t KnowledgeGraph::concept_count() const noexcept {
    return concepts_.size();
}

std::size_t KnowledgeGraph::relation_count() const noexcept {
    return relations_.size();
}

ConceptId KnowledgeGraph::next_id() const noexcept {
    ConceptId maximum = 0;
    for (const auto& [id, node] : concepts_) {
        static_cast<void>(node);
        maximum = std::max(maximum, id);
    }
    return maximum + 1;
}

void KnowledgeGraph::clear() noexcept {
    concepts_.clear();
    relations_.clear();
}

} // namespace atlas
