#pragma once

#include "atlas/core/types.hpp"

#include <string>
#include <string_view>
#include <vector>

namespace atlas {

struct Concept {
    ConceptId id{};
    std::string title;
    std::string summary;
    std::vector<std::string> tags;
    std::vector<SourceReference> sources;

    [[nodiscard]] bool valid() const noexcept;
    [[nodiscard]] bool has_tag(std::string_view tag) const;
};

struct Relation {
    ConceptId from{};
    ConceptId to{};
    std::string type;
    double weight{1.0};
    std::string note;

    [[nodiscard]] bool valid() const noexcept;
};

} // namespace atlas
