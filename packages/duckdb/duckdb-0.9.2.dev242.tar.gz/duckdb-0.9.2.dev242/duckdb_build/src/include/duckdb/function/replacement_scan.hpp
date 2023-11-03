//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/function/replacement_scan.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/common.hpp"
#include "duckdb/common/string_util.hpp"

namespace duckdb {

class ClientContext;
class TableRef;

struct ReplacementScanData {
	virtual ~ReplacementScanData() {
	}
};

typedef unique_ptr<TableRef> (*replacement_scan_t)(ClientContext &context, const string &table_name,
                                                   ReplacementScanData *data);

//! Replacement table scans are automatically attempted when a table name cannot be found in the schema
//! This allows you to do e.g. SELECT * FROM 'filename.csv', and automatically convert this into a CSV scan
struct ReplacementScan {
	explicit ReplacementScan(replacement_scan_t function, unique_ptr<ReplacementScanData> data_p = nullptr)
	    : function(function), data(std::move(data_p)) {
	}

	static bool CanReplace(const string &table_name, const vector<string> &extensions) {
		auto lower_name = StringUtil::Lower(table_name);

		if (StringUtil::EndsWith(lower_name, ".gz")) {
			lower_name = lower_name.substr(0, lower_name.size() - 3);
		} else if (StringUtil::EndsWith(lower_name, ".zst")) {
			lower_name = lower_name.substr(0, lower_name.size() - 4);
		}

		for (auto &extension : extensions) {
			if (StringUtil::EndsWith(lower_name, "." + extension) ||
			    StringUtil::Contains(lower_name, "." + extension + "?")) {
				return true;
			}
		}

		return false;
	}

	replacement_scan_t function;
	unique_ptr<ReplacementScanData> data;
};

} // namespace duckdb
