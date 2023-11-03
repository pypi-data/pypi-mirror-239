//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/core_functions/scalar/bit_functions.hpp
//
//
//===----------------------------------------------------------------------===//
// This file is automatically generated by scripts/generate_functions.py
// Do not edit this file manually, your changes will be overwritten
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/function/function_set.hpp"

namespace duckdb {

struct GetBitFun {
	static constexpr const char *Name = "get_bit";
	static constexpr const char *Parameters = "bitstring,index";
	static constexpr const char *Description = "Extracts the nth bit from bitstring; the first (leftmost) bit is indexed 0";
	static constexpr const char *Example = "get_bit('0110010'::BIT, 2)";

	static ScalarFunction GetFunction();
};

struct SetBitFun {
	static constexpr const char *Name = "set_bit";
	static constexpr const char *Parameters = "bitstring,index,new_value";
	static constexpr const char *Description = "Sets the nth bit in bitstring to newvalue; the first (leftmost) bit is indexed 0. Returns a new bitstring";
	static constexpr const char *Example = "set_bit('0110010'::BIT, 2, 0)";

	static ScalarFunction GetFunction();
};

struct BitPositionFun {
	static constexpr const char *Name = "bit_position";
	static constexpr const char *Parameters = "substring,bitstring";
	static constexpr const char *Description = "Returns first starting index of the specified substring within bits, or zero if it is not present. The first (leftmost) bit is indexed 1";
	static constexpr const char *Example = "bit_position('010'::BIT, '1110101'::BIT)";

	static ScalarFunction GetFunction();
};

struct BitStringFun {
	static constexpr const char *Name = "bitstring";
	static constexpr const char *Parameters = "bitstring,length";
	static constexpr const char *Description = "Pads the bitstring until the specified length";
	static constexpr const char *Example = "bitstring('1010'::BIT, 7)";

	static ScalarFunction GetFunction();
};

} // namespace duckdb
