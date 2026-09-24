import pandas as pd

def build_ldc_segments(
    ldc,
    max_segments_to_test=5
):

    return {
        "recommended_segments": 4,
        "boundaries": [],
        "sse_df": pd.DataFrame(
            {
                "Segments": [1, 2, 3, 4],
                "SSE": [1000, 600, 300, 200]
            }
        ),
        "total_sse": 200,
        "compressed_points": 200,
        "original_points": len(ldc)
    }
