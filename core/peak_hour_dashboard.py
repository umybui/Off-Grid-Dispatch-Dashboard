import streamlit as st


def build_peak_hour_dashboard(
    peak_hour,
    peak_hour_share_fig
):

    st.subheader(
        "Peak Hour Performance Analysis"
    )

    st.caption(
        f"""
        Peak-demand hours are defined as all hours where system
        demand reached at least 90% of the system peak demand.
    
        For the selected study period, the peak-demand threshold
        is {peak_hour['peak_threshold']:.2f} MW, resulting in
        {len(peak_hour['peak_hours'])} peak-demand hours.
    
        The analysis below evaluates how generating plants
        contributed during these critical periods and identifies
        the assets most important for supporting system peak demand.
        """
    )
    
    snapshot = (
        peak_hour["peak_snapshot"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Peak Threshold",
            f"{peak_hour['peak_threshold']:,.2f}"
        )

    with col2:
        st.metric(
            "Peak Hours",
            len(
                peak_hour["peak_hours"]
            )
        )

    with col3:
        st.metric(
            "Plants Supporting Peak",
            len(snapshot)
        )

    with st.expander(
        "Peak Hour Snapshot",
        expanded=False
    ):

        st.dataframe(
            snapshot.round(2),
            use_container_width=True,
            hide_index=True
        )

    st.markdown(
        "##### Generation Mix at Peak Demand"
    )

    st.caption(
        """
        The chart shows each plant's share of total energy
        generated during peak-demand hours only.
    
        Larger percentages indicate plants that were most
        relied upon when system demand was near its maximum.
        """
    )
    
    st.plotly_chart(
        peak_hour_share_fig,
        use_container_width=True
    )

    with st.expander(
        "View Generation Mix at Peak Demand Data",
        expanded=False
    ):

        display_df = (
            peak_hour["peak_snapshot"]
            [
                [
                    "Plant",
                    "AvgPeakMW",
                    "PeakEnergySharePct"
                ]
            ]
            .rename(
                columns={
                    "AvgPeakMW": "Value",
                    "PeakEnergySharePct": "Percent"
                }
            )
            .sort_values(
                "Value",
                ascending=False
            )
            .round(2)
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
