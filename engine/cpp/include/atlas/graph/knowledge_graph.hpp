#pragma once

#include "atlas/core/concept.hpp"

#include <cstddef>
#include <optional>
#include <unordered_map>
#include <vector>

namespace atlas {

class KnowledgeGraph {
public:
    [[nodiscard]] bool add_concept(Concept node);
    [[nodiscard]] bool upsert_concept(Concept node);
    [[nodiscard]] bool remove_concept(ConceptId id);

    [[nodiscard]] bool add_relation(Relation relation);
    [[nodiscard]] bool remove_relation(ConceptId from, ConceptId to, const std::string& type);

    [[nodiscard]] const Concept* find_concept(ConceptId id) const noexcept;
    [[nodiscard]] Concept* find_concept(ConceptId id) noexcept;

    [[nodiscard]] std::vector<Concept> concepts() const;
    [[nodiscard]] const std::vector<Relation>& relations() const noexcept;
    [[nodiscard]] std::vector<Relation> outgoing(ConceptId id) const;
    [[nodiscard]] std::vector<Relation> incoming(ConceptId id) const;
    [[nodiscard]] std::vector<ConceptId> shortest_path(ConceptId start, ConceptId goal) const;

    [[nodiscard]] std::size_t concept_count() const noexcept;
    [[nodiscard]] std::size_t relation_count() const noexcept;
    [[nodiscard]] ConceptId next_id() const noexcept;
    void clear() noexcept;

private:
    std::unordered_map<ConceptId, Concept> concepts_;
    std::vector<Relation> relations_;
};

} // namespace atlas
