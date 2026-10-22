import streamlit as st


def build_asset_performance_dashboard(
    asset_performance,
    asset_performance_chart
):

    st.subheader(
        "Plant Asset Performance Assessment"
    )

    st.markdown(
        """
        **Story:** Evaluates whether each generating plant
        was capable of realizing its available capability at
        any point during the study period, independent of
        system peak demand.
    
        **Capability Realization (%)**
        = Maximum Observed Output ÷ Dependable Capacity
    
        **Utilization Factor (%)**
        = Average Output ÷ Dependable Capacity
    
        **Interpretation:**
        High Capability Realization indicates the plant was
        capable of reaching its dependable rating.
        High Utilization Factor indicates the plant was
        heavily utilized during the study period.
        """
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
