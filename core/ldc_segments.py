import pandas as pd
import numpy as np


def optimal_ldc_segments(
    ldc_values,
    k
):

    y = np.array(ldc_values)

    n = len(y)

    prefix_sum = np.zeros(n + 1)
    prefix_sq = np.zeros(n + 1)

    prefix_sum[1:] = np.cumsum(y)
    prefix_sq[1:] = np.cumsum(y ** 2)

    def segment_sse(i, j):

        count = j - i

        if count <= 0:
            return 0

        seg_sum = (
            prefix_sum[j]
            - prefix_sum[i]
        )

        seg_sq = (
            prefix_sq[j]
            - prefix_sq[i]
        )

        mean = seg_sum / count

        return (
            seg_sq
            - count * mean * mean
        )

    dp = np.full(
        (k + 1, n + 1),
        np.inf
    )

    split = np.zeros(
        (k + 1, n + 1),
        dtype=int
    )

    dp[0, 0] = 0

    for seg in range(1, k + 1):

        for end in range(1, n + 1):

            for start in range(
                seg - 1,
                end
            ):

                cost = (
                    dp[seg - 1, start]
                    + segment_sse(
                        start,
                        end
                    )
                )

                if cost < dp[seg, end]:

                    dp[seg, end] = cost

                    split[seg, end] = start

    boundaries = []

    end = n

    for seg in range(
        k,
        0,
        -1
    ):

        start = split[
            seg,
            end
        ]

        boundaries.append(
            (start, end)
        )

        end = start

    boundaries.reverse()

    return (
        boundaries,
        dp[k, n]
    )


def build_ldc_segments(
    ldc,
    max_segments_to_test=20
):

    max_points = 200

    if len(ldc) > max_points:

        step = max(
            1,
            len(ldc) // max_points
        )

        ldc_seg = (
            ldc["DemandMW"]
            .groupby(
                ldc.index // step
            )
            .mean()
            .reset_index(
                drop=True
            )
        )

    else:

        ldc_seg = (
            ldc["DemandMW"]
            .copy()
        )

    sse_results = []

    for k in range(
        1,
        max_segments_to_test + 1
    ):

        _, sse = optimal_ldc_segments(
            ldc_seg.values,
            k
        )

        sse_results.append(
            {
                "Segments": k,
                "SSE": sse
            }
        )

    sse_df = pd.DataFrame(
        sse_results
    )

    sse_df["Improvement"] = (
        sse_df["SSE"].shift(1)
        - sse_df["SSE"]
    )

    sse_df["PctImprovement"] = (
        sse_df["Improvement"]
        /
        sse_df["SSE"].shift(1)
        * 100
    )

    recommended_segments = 4

    for i in range(
        2,
        len(sse_df)
    ):

        if (
            sse_df.loc[
                i,
                "PctImprovement"
            ]
            < 10
        ):

            recommended_segments = int(
                sse_df.loc[
                    i - 1,
                    "Segments"
                ]
            )

            break

    boundaries, total_sse = (
        optimal_ldc_segments(
            ldc_seg.values,
            recommended_segments
        )
    )

    return {

        "recommended_segments":
            recommended_segments,

        "boundaries":
            boundaries,

        "sse_df":
            sse_df,

        "total_sse":
            total_sse,

        "compressed_points":
            len(ldc_seg),

        "original_points":
            len(ldc)
    }

def build_segment_table(
    ldc,
    boundaries,
    compressed_points=None
):

    segment_rows = []

    if compressed_points is None:
        compressed_points = len(ldc)

    scale_factor = (
        len(ldc)
        / compressed_points
    )

    for i, (
        start_idx,
        end_idx
    ) in enumerate(boundaries):

        actual_start = int(
            start_idx * scale_factor
        )

        actual_end = int(
            end_idx * scale_factor
        )

        segment_data = ldc.iloc[
            actual_start:actual_end
        ]["DemandMW"]

        if len(segment_data) == 0:
            continue

        segment_mean = (
            segment_data.mean()
        )

        segment_sse = (
            (
                segment_data
                - segment_mean
            ) ** 2
        ).sum()

        segment_rows.append({

            "Segment":
                f"S{i+1}",

            "Start %":
                round(
                    actual_start
                    / len(ldc)
                    * 100,
                    2
                ),

            "End %":
                round(
                    actual_end
                    / len(ldc)
                    * 100,
                    2
                ),

            "Avg MW":
                round(
                    segment_mean,
                    2
                ),

            "Max MW":
                round(
                    segment_data.max(),
                    2
                ),

            "Min MW":
                round(
                    segment_data.min(),
                    2
                ),

            "Hours":
                len(segment_data),

            "% Time":
                round(
                    len(segment_data)
                    / len(ldc)
                    * 100,
                    2
                ),

            "Energy (MWh)":
                round(
                    segment_data.sum(),
                    2
                ),

            "SSE":
                round(
                    segment_sse,
                    0
                )
        })

    return pd.DataFrame(
        segment_rows
    )
