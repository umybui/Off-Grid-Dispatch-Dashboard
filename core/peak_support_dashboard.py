import streamlit as st


def build_peak_support_dashboard(
    peak_support,
    peak_support_chart
):

    st.subheader(
        "Peak Support Performance"
    )

    st.caption(
        """
        This assessment evaluates how effectively each
        generating plant supported system demand during
        peak-demand hours.

        Peak Support (%) compares the observed peak-hour
        output of each plant against its dependable
        generating capacity.

        Assets with lower realization during peak periods
        may require operational review or capacity
        improvement measures.
        """
    )

    with st.expander(
        "Peak Support Table",
        expanded=False
    ):

        st.dataframe(
            peak_support[
                [
                    "Plant",
                    "AvgPeakMW",
                    "MaxPeakMW",
                    "DependableMW",
                    "PeakSupportPct",
                    "RiskFlag",
                    "Remarks"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )

    ok_count = (
        peak_support["RiskFlag"]
        == "OK"
    ).sum()

    monitor_count = (
        peak_support["RiskFlag"]
        == "Monitor"
    ).sum()

    under_count = (
        peak_support["RiskFlag"]
        == "Underperforming"
    ).sum()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "OK",
            ok_count
        )

    with c2:
        st.metric(
            "Monitor",
            monitor_count
        )

    with c3:
        st.metric(
            "Underperforming",
            under_count
        )

    st.markdown(
        "##### Peak Support Achievement Chart"
    )

    st.caption(
        """
        Green bars indicate assets meeting expected
        peak-demand support levels.

        Yellow bars indicate assets requiring
        monitoring.

        Red bars indicate assets that did not deliver
        expected capability during peak-demand periods.
        """
    )

    st.plotly_chart(
        peak_support_chart,
        use_container_width=True
    )
