import streamlit as st


def build_asset_performance_dashboard(
    asset_performance,
    asset_performance_chart
):

    st.subheader(
        "Plant Asset Performance Assessment"
    )

    st.caption(
        """
        Story:

        Evaluates whether each generating plant was capable
        of realizing its available capability at any point
        during the study period, independent of system peak
        demand conditions.

        Capability Realization (%) =
        Maximum Observed Output ÷ Dependable Capacity

        Utilization Factor (%) =
        Average Output ÷ Dependable Capacity

        Plants achieving high capability realization
        are capable of reaching their dependable rating.
        """
    )

    with st.expander(
        "View Historical Plant Asset Performance Table",
        expanded=False
    ):

        st.dataframe(
            asset_performance[
                [
                    "Plant",
                    "DependableMW",
                    "AvgMW",
                    "MaxObservedMW",
                    "UtilizationFactorPct",
                    "CapabilityRealizationPct",
                    "RiskFlag",
                    "Remarks"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )

    ok_count = (
        asset_performance["RiskFlag"]
        == "OK"
    ).sum()

    monitor_count = (
        asset_performance["RiskFlag"]
        == "Monitor"
    ).sum()

    underperforming_count = (
        asset_performance["RiskFlag"]
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
            underperforming_count
        )

    st.markdown(
        "### Plant Capability Scenario"
    )

    st.caption(
        """
        Exclude retired or unavailable plants to evaluate
        plant capability realization under an adjusted fleet
        configuration.
        """
    )

    excluded_plants = st.multiselect(
        "Exclude Units",
        options=sorted(
            asset_performance["Plant"]
            .unique()
        ),
        key="asset_performance_exclusion"
    )

    scenario_df = (
        asset_performance[
            ~asset_performance["Plant"]
            .isin(excluded_plants)
        ]
        .copy()
    )

    historical_capacity = (
        asset_performance[
            "DependableMW"
        ].sum()
    )

    scenario_capacity = (
        scenario_df[
            "DependableMW"
        ].sum()
    )

    removed_capacity = (
        historical_capacity
        -
        scenario_capacity
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Historical Capacity",
            f"{historical_capacity:,.2f} MW"
        )

    with c2:
        st.metric(
            "Scenario Capacity",
            f"{scenario_capacity:,.2f} MW"
        )

    with c3:
        st.metric(
            "Capacity Removed",
            f"{removed_capacity:,.2f} MW"
        )

    st.markdown(
        "##### Capability Realization by Plant (Scenario)"
    )

    st.plotly_chart(
        asset_performance_chart,
        use_container_width=True
    )

    with st.expander(
        "View Scenario Plant Asset Performance Table",
        expanded=False
    ):

        st.dataframe(
            scenario_df[
                [
                    "Plant",
                    "DependableMW",
                    "AvgMW",
                    "MaxObservedMW",
                    "UtilizationFactorPct",
                    "CapabilityRealizationPct",
                    "RiskFlag",
                    "Remarks"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )
