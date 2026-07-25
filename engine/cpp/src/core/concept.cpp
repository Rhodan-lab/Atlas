#include "atlas/core/concept.hpp"

#include <algorithm>
#include <cctype>

namespace atlas {
namespace {

std::string lowercase(std::string_view value) {
    std::string result(value);
    std::transform(result.begin(), result.end(), result.begin(), [](unsigned char ch) {
        return static_cast<char>(std::tolower(ch));
    });
    return result;
}

} // namespace

bool Concept::valid() const noexcept {
    return id != 0 && !title.empty();
}

bool Concept::has_tag(std::string_view tag) const {
    const auto expected = lowercase(tag);
    return std::any_of(tags.begin(), tags.end(), [&](const std::string& candidate) {
        return lowercase(candidate) == expected;
    });
}

bool Relation::valid() const noexcept {
    return from != 0 && to != 0 && from != to && !type.empty() && weight > 0.0;
}

} // namespace atlas
