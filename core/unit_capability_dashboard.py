import streamlit as st


def build_unit_capability_dashboard(
    unit_capability,
    unit_capability_chart
):

    st.subheader(
        "Unit Capability Realization"
    )

    st.markdown(
        """
        **Story:** Evaluates whether individual units
        can consistently sustain at least 80% of their
        dependable capacity throughout the study period,
        rather than merely reaching full output during
        isolated operating hours.

        **Sustained Capability (%)**
        = Hours Above 80% Dependable Capacity
        ÷ Total Operating Hours

        Units with high sustained capability are capable
        of maintaining dependable performance for long
        durations and not only during short peaks.
        """
    )

    st.markdown(
        "##### Unit Sustained Capability Assessment"
    )

    st.plotly_chart(
        unit_capability_chart,
        use_container_width=True
    )

    with st.expander(
        "View Unit Capability Realization Table",
        expanded=False
    ):

        display_df = (
            unit_capability[
                [
                    "Plant",
                    "Unit",
                    "DependableMW",
                    "AvgMW",
                    "MaxObservedMW",
                    "OperatingHours",
                    "HoursAbove80Pct",
                    "UtilizationFactorPct",
                    "CapabilityRealizationPct",
                    "SustainedCapabilityPct",
                    "RiskFlag",
                    "Remarks"
                ]
            ]
            .sort_values(
                ["Plant", "Unit"]
            )
            .round(2)
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
