
import streamlit as st


def build_peak_hour_dashboard(
    peak_hour,
    peak_hour_share_fig
):

    st.subheader(
        "Peak Hour Performance Analysis (90%-100% of Peak Demand)"
    )

    st.caption(
        f"""
        During hours when system demand reached at least
        90% of peak demand, the following generating units
        supported the grid.

        Peak-demand threshold:
        {peak_hour['peak_threshold']:,.2f} MW

        Total Peak Hours:
        {len(peak_hour['peak_hours'])}
        """
    )

    snapshot = (
        peak_hour["peak_snapshot"]
    )

    top_contributor = (
        snapshot
        .sort_values(
            "PeakEnergySharePct",
            ascending=False
        )
        .iloc[0]["Plant"]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "90% Peak Threshold",
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
            snapshot["Plant"]
            .nunique()
        )

    with col4:
        st.metric(
            "Top Contributor",
            top_contributor
        )

    st.markdown(
        "##### Peak Hour Energy Contribution Share (90%-100% of Peak Demand)"
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
        "Peak Hour Snapshot (90%-100% of Peak Demand)",
        expanded=False
    ):

        display_cols = [
            col
            for col in [
                "Plant",
                "Unit",
                "AvgPeakMW",
                "MaxPeakMW",
                "PeakEnergyMWh",
                "PeakEnergySharePct",
                "PlantSharePct"
            ]
            if col in snapshot.columns
        ]

        st.dataframe(
            snapshot[
                display_cols
            ].round(2),
            use_container_width=True,
            hide_index=True
        )
