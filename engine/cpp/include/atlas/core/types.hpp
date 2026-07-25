#pragma once

#include <cstdint>
#include <string>

namespace atlas {

using ConceptId = std::uint64_t;

struct SourceReference {
    std::string title;
    std::string locator;
};

} // namespace atlas
