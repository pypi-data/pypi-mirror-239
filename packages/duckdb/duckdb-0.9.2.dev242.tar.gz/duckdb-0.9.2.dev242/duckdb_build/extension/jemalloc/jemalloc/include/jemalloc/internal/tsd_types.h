#ifndef JEMALLOC_INTERNAL_TSD_TYPES_H
#define JEMALLOC_INTERNAL_TSD_TYPES_H

namespace duckdb_jemalloc {

#define MALLOC_TSD_CLEANUPS_MAX	4

typedef struct tsd_s tsd_t;
typedef struct tsdn_s tsdn_t;
typedef bool (*malloc_tsd_cleanup_t)(void);

} // namespace duckdb_jemalloc

#endif /* JEMALLOC_INTERNAL_TSD_TYPES_H */
