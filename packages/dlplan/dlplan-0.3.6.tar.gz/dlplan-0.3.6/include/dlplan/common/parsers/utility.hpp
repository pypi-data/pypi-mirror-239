#ifndef DLPLAN_INCLUDE_DLPLAN_COMMON_PARSERS_UTILITY_HPP_
#define DLPLAN_INCLUDE_DLPLAN_COMMON_PARSERS_UTILITY_HPP_

#include <map>

#include "include/dlplan/common/parsers/config.hpp"


namespace dlplan {

extern bool in_bounds(
    const error_handler_type& error_handler,
    const iterator_type& iter, const iterator_type& end);

}

#endif