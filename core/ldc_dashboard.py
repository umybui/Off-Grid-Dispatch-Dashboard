import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from core.ldc import build_ldc
from core.ldc_segments import (
    build_ldc_segments,
    build_segment_table
)
from core.ldc_chart import (
    build_ldc_chart
)

def build_ldc_dashboard(
    total_demand
):

    # =====================================================
    # LOAD DURATION CURVE
    # =====================================================
    
    ldc = build_ldc(
        total_demand
    )

    ldc_segments = build_ldc_segments(
        ldc
    )
  
    # =====================================================
    # LDC SEGMENTATION CONTROLS
    # =====================================================
    
    max_segments = 20
    
    recommended_temp = (
        build_ldc_segments(
            ldc,
            max_segments_to_test=max_segments
        )
    )
    
    recommended_segments = (
        recommended_temp[
            "recommended_segments"
        ]
    )
    
    use_recommended = True

    
    segment_table = build_segment_table(
        ldc,
        ldc_segments["boundaries"],
        ldc_segments["compressed_points"]
    )
    
    ldc_fig, segment_summary = (
        build_ldc_chart(
            ldc,
            ldc_segments["boundaries"],
            ldc_segments["compressed_points"]
        )
    )

    # =====================================================
    # LOAD DURATION CURVE
    # =====================================================
    
    st.subheader(
        "Load Duration Curve"
    )
    
    st.caption(
        "Load Segment Summary"
    )
    
    with st.expander(
        "Segmentation Controls",
        expanded=True
    ):
    
        max_segments = st.number_input(
            "Maximum Segments Evaluated",
            min_value=3,
            max_value=20,
            value=20,
            step=1
        )
    
        st.caption(
            """
            The dashboard automatically evaluates
            multiple segmentation levels and identifies
            the elbow point.
    
            Higher values increase analysis detail but
            may slightly increase processing time.
            """
        )
    
    use_recommended = st.toggle(
        "Use Recommended",
        value=True
    )

    # Determine recommendation
    recommended_segments = (
        ldc_segments["recommended_segments"]
    )
    
    # User selection
    selected_segments = (
        recommended_segments
        if use_recommended
        else max_segments
    )
    
    # Rebuild segmentation using selected value
    ldc_segments = build_ldc_segments(
        ldc,
        max_segments_to_test=max_segments,
        selected_segments=selected_segments
    )
    
    segment_table = build_segment_table(
        ldc,
        ldc_segments["boundaries"],
        ldc_segments["compressed_points"]
    )
    
    ldc_fig, segment_summary = (
        build_ldc_chart(
            ldc,
            ldc_segments["boundaries"],
            ldc_segments["compressed_points"]
        )
    )
    
    # =====================================================
    # RECOMMENDED SEGMENTS
    # =====================================================
    
    recommended_segments = (
        ldc_segments["recommended_segments"]
    )
    
    st.success(
        f"Recommended Segments: "
        f"{recommended_segments}"
    )
    
    if not use_recommended:
    
        st.info(
            f"Manual Selection: "
            f"{selected_segments} Segments"
        )
    
    # =====================================================
    # ADVANCED LDC SEGMENTATION ANALYSIS
    # =====================================================
    
    with st.expander(
        "Advanced LDC Segmentation Analysis",
        expanded=True
    ):
    
        st.metric(
            "Current Segmentation SSE",
            f"{ldc_segments['total_sse']:,.0f}"
        )
    
        st.markdown(
            f"""
    ### Recommended Segmentation: {recommended_segments} Segments
    
    The elbow analysis indicates that most of the
    reduction in segmentation error is achieved by
    approximately {recommended_segments} segments.
    
    Beyond this point, additional segments improve
    accuracy more slowly while increasing model
    complexity.
    
    Current Selection:
    **{selected_segments} Segments**
    """
        )
    
        if selected_segments == recommended_segments:
        
            st.success(
                f"Current Selection: {selected_segments} segments "
                f"(recommended value)"
            )
        
        else:
        
            st.info(
                f"Current Selection: {selected_segments} segments "
                f"(recommended: {recommended_segments})"
            )
    
        # =====================================================
        # ELBOW METHOD CHART
        # =====================================================
    
        sse_df = ldc_segments["sse_df"]
    
        fig_elbow = go.Figure()
    
        fig_elbow.add_trace(
            go.Scatter(
                x=sse_df.iloc[:, 0],
                y=sse_df.iloc[:, 1],
                mode="lines+markers",
                name="Total SSE"
            )
        )
    
        highlight_row = (
            sse_df.iloc[
                recommended_segments - 1
            ]
        )
    
        fig_elbow.add_trace(
            go.Scatter(
                x=[highlight_row.iloc[0]],
                y=[highlight_row.iloc[1]],
                mode="markers",
                marker=dict(
                    color="red",
                    size=12,
                    symbol="star"
                ),
                name="Recommended"
            )
        )
    
        fig_elbow.update_layout(
            title="Elbow Method for Load Segmentation",
            xaxis_title="Number of Segments",
            yaxis_title="Segmentation SSE",
            height=400
        )
    
        st.plotly_chart(
            fig_elbow,
            use_container_width=True,
            key="ldc_elbow"
        )
    
        # =====================================================
        # OPERATIONAL INTERPRETATION
        # =====================================================
        
        highest_segment = segment_table.iloc[0]
        lowest_segment = segment_table.iloc[-1]
        
        st.markdown(
            "### Operational Interpretation"
        )
        
        st.markdown(
            f"""
        The selected **{selected_segments}-segment**
        model divides the Load Duration Curve into
        **{selected_segments} natural demand regimes**.
        
        • Highest demand segment (S1) occurs during approximately
        **{highest_segment['% Time']:.1f}%**
        of the study period.
        
        • Lowest demand segment (S{selected_segments})
        occurs during approximately
        **{lowest_segment['% Time']:.1f}%**
        of the study period.
        
        • Total segmentation error is
        **{ldc_segments['total_sse']:,.0f} SSE**.
        
        • These segments can be used for dispatch planning,
        capacity adequacy assessments, reserve studies,
        and generation portfolio analysis.
        """
        )
        
        st.dataframe(
            segment_table.round(2),
            use_container_width=True,
            hide_index=True
        )
    
    # =====================================================
    # LOAD DURATION CURVE CHART
    # =====================================================
    
    st.caption(
        """
        The Load Duration Curve ranks all demand observations
        from highest to lowest, illustrating how often
        different demand levels occur throughout the study period.
    
        Segment boundaries identify natural operating regimes
        such as peaking, upper mid-merit, lower mid-merit,
        and baseload demand conditions.
    
        The segmentation model provides a simplified
        representation of system demand suitable for
        capacity planning, reserve adequacy assessment,
        dispatch optimization, and generation portfolio studies.
        """
    )
    
    st.plotly_chart(
        ldc_fig,
        use_container_width=True,
        key="ldc_curve"
    )

    st.markdown(
        "##### Segment Summary"
    )
    
    st.dataframe(
        pd.DataFrame(
            segment_summary
        ),
        use_container_width=True,
        hide_index=True
    )
   
