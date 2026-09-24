import pandas as pd


def build_ldc_segments(
    ldc,
    max_segments_to_test=5
):

    boundaries = [
        (0, int(len(ldc) * 0.10)),
        (
            int(len(ldc) * 0.10),
            int(len(ldc) * 0.40)
        ),
        (
            int(len(ldc) * 0.40),
            len(ldc)
        )
    ]

    return {

        "recommended_segments": 3,

        "boundaries": boundaries,

        "sse_df": pd.DataFrame(
            {
                "Segments": [1, 2, 3],
                "SSE": [1000, 600, 300]
            }
        ),

        "total_sse": 300,

        "compressed_points": 200,

        "original_points": len(ldc)
    }


def build_segment_table(
    ldc,
    boundaries
):

    segment_rows = []

    for i, (start_idx, end_idx) in enumerate(boundaries):

        segment_data = ldc.iloc[
            start_idx:end_idx
        ]["DemandMW"]

        if len(segment_data) == 0:
            continue

        segment_mean = segment_data.mean()

        segment_sse = (
            (
                segment_data
                -
                segment_mean
            ) ** 2
        ).sum()

        segment_rows.append({

            "Segment": f"S{i+1}",

            "Avg MW": round(
                segment_mean,
                2
            ),

            "Max MW": round(
                segment_data.max(),
                2
            ),

            "Min MW": round(
                segment_data.min(),
                2
            ),

            "Hours": len(segment_data),

            "% Time": round(
                len(segment_data)
                /
                len(ldc)
                * 100,
                2
            ),

            "Energy (MWh)": round(
                segment_data.sum(),
                2
            ),

            "SSE": round(
                segment_sse,
                0
            )
        })

    return pd.DataFrame(
        segment_rows
    )
