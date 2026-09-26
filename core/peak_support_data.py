from core.peak_support import (
    build_peak_support_table
)


def build_peak_support_analysis(
    peak_hour,
    capacity_reference
):

    peak_snapshot = (
        peak_hour["peak_snapshot"]
    )

    performance = (
        build_peak_support_table(
            peak_snapshot,
            capacity_reference
        )
    )

    return performance
