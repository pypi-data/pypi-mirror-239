//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/core_functions/aggregate/algebraic_functions.hpp
//
//
//===----------------------------------------------------------------------===//
// This file is automatically generated by scripts/generate_functions.py
// Do not edit this file manually, your changes will be overwritten
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/function/function_set.hpp"

namespace duckdb {

struct AvgFun {
	static constexpr const char *Name = "avg";
	static constexpr const char *Parameters = "x";
	static constexpr const char *Description = "Calculates the average value for all tuples in x.";
	static constexpr const char *Example = "SUM(x) / COUNT(*)";

	static AggregateFunctionSet GetFunctions();
};

struct MeanFun {
	using ALIAS = AvgFun;

	static constexpr const char *Name = "mean";
};

struct CorrFun {
	static constexpr const char *Name = "corr";
	static constexpr const char *Parameters = "y,x";
	static constexpr const char *Description = "Returns the correlation coefficient for non-null pairs in a group.";
	static constexpr const char *Example = "COVAR_POP(y, x) / (STDDEV_POP(x) * STDDEV_POP(y))";

	static AggregateFunction GetFunction();
};

struct CovarPopFun {
	static constexpr const char *Name = "covar_pop";
	static constexpr const char *Parameters = "y,x";
	static constexpr const char *Description = "Returns the population covariance of input values.";
	static constexpr const char *Example = "(SUM(x*y) - SUM(x) * SUM(y) / COUNT(*)) / COUNT(*)";

	static AggregateFunction GetFunction();
};

struct CovarSampFun {
	static constexpr const char *Name = "covar_samp";
	static constexpr const char *Parameters = "y,x";
	static constexpr const char *Description = "Returns the sample covariance for non-null pairs in a group.";
	static constexpr const char *Example = "(SUM(x*y) - SUM(x) * SUM(y) / COUNT(*)) / (COUNT(*) - 1)";

	static AggregateFunction GetFunction();
};

struct FAvgFun {
	static constexpr const char *Name = "favg";
	static constexpr const char *Parameters = "x";
	static constexpr const char *Description = "Calculates the average using a more accurate floating point summation (Kahan Sum)";
	static constexpr const char *Example = "favg(A)";

	static AggregateFunction GetFunction();
};

struct StandardErrorOfTheMeanFun {
	static constexpr const char *Name = "sem";
	static constexpr const char *Parameters = "x";
	static constexpr const char *Description = "Returns the standard error of the mean";
	static constexpr const char *Example = "";

	static AggregateFunction GetFunction();
};

struct StdDevPopFun {
	static constexpr const char *Name = "stddev_pop";
	static constexpr const char *Parameters = "x";
	static constexpr const char *Description = "Returns the population standard deviation.";
	static constexpr const char *Example = "sqrt(var_pop(x))";

	static AggregateFunction GetFunction();
};

struct StdDevSampFun {
	static constexpr const char *Name = "stddev_samp";
	static constexpr const char *Parameters = "x";
	static constexpr const char *Description = "Returns the sample standard deviation";
	static constexpr const char *Example = "sqrt(var_samp(x))";

	static AggregateFunction GetFunction();
};

struct StddevFun {
	using ALIAS = StdDevSampFun;

	static constexpr const char *Name = "stddev";
};

struct VarPopFun {
	static constexpr const char *Name = "var_pop";
	static constexpr const char *Parameters = "x";
	static constexpr const char *Description = "Returns the population variance.";
	static constexpr const char *Example = "";

	static AggregateFunction GetFunction();
};

struct VarSampFun {
	static constexpr const char *Name = "var_samp";
	static constexpr const char *Parameters = "x";
	static constexpr const char *Description = "Returns the sample variance of all input values.";
	static constexpr const char *Example = "(SUM(x^2) - SUM(x)^2 / COUNT(x)) / (COUNT(x) - 1)";

	static AggregateFunction GetFunction();
};

struct VarianceFun {
	using ALIAS = VarSampFun;

	static constexpr const char *Name = "variance";
};

} // namespace duckdb
