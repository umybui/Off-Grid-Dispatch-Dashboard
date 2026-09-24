import numpy as np
import pandas as pd

def optimal_ldc_segments(ldc_values, k):

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

        return seg_sq - count * mean * mean

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

            for start in range(seg - 1, end):

                cost = (
                    dp[seg - 1, start]
                    + segment_sse(start, end)
                )

                if cost < dp[seg, end]:

                    dp[seg, end] = cost

                    split[seg, end] = start

    boundaries = []

    end = n

    for seg in range(k, 0, -1):

        start = split[seg, end]

        boundaries.append(
            (start, end)
        )

        end = start

    boundaries.reverse()

    return boundaries, dp[k, n]

def build_ldc_segments(
    ldc,
    max_segments_to_test=5
):

    max_points = 200

    if len(ldc) > max_points:

        step = max(
            len(ldc) // max_points,
            1
        )

        ldc_seg = (
            ldc.groupby(
                ldc.index // step
            )["DemandMW"]
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

        sse_results.append({
            "Segments": k,
            "SSE": sse
        })

    sse_df = pd.DataFrame(
        sse_results
    )

    sse_df["Improvement"] = (
        sse_df["SSE"].shift(1)
        -
        sse_df["SSE"]
    )

    sse_df["PctImprovement"] = (
        sse_df["Improvement"]
        /
        sse_df["SSE"].shift(1)
        * 100
    )

    recommended_segments = min(
        4,
        max_segments_to_test
    )

    for i in range(
        2,
        len(sse_df)
    ):

        if (
            sse_df.loc[
                i,
                "PctImprovement"
            ] < 10
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
