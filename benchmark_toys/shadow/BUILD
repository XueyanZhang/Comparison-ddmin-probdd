package(default_visibility = ["//test:__subpackages__"])

load("//benchmark:benchmark.bzl", "sanity_test")
load("//benchmark:shadow.bzl", "shadow_reduction_golden_test")

sanity_test(
    name = "shadow_sanity_test",
    source_files = [
        "source.c",
        "shadow.c",
    ],
    test_script = "r.sh",
)

shadow_reduction_golden_test(
    name = "shadow_reduction_golden_test",
    enable_edit_caching = True,
    enable_query_caching = False,
    golden_progress_file = "golden_reduction_progress.txt",
    golden_reduced_shadow_file = "golden_reduced_shadow.c",
    golden_reduced_source_file = "golden_reduced_source.c",
    log_file = "reduction_golden_test.log",
    progress_dump_file = "reduction_progress.txt",
    reduction_algorithm = "perses_node_priority_with_dfs_delta",
    shadow_file = "shadow.c",
    source_file = "source.c",
    test_script = "r.sh",
)
