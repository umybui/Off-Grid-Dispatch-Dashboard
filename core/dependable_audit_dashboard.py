import streamlit as st


def build_dependable_audit_dashboard(
    dependable_audit
):

    st.subheader(
        "Dependable Capacity Audit Trail"
    )

    with st.expander(
        "View Dependable Capacity Audit Trail",
        expanded=False
    ):

        st.caption(
            """
            This table shows the plant-level
            dependable capacity used in the
            asset assessment.

            Select a plant to view the
            contributing unit-level breakdown.
            """
        )

        plant_totals = (
            dependable_audit[
                "plant_totals"
            ]
        )

        unit_breakdown = (
            dependable_audit[
                "unit_breakdown"
            ]
        )

        st.markdown(
            "##### Plant-Level Dependable Capacity"
        )

        st.dataframe(
            plant_totals.round(2),
            use_container_width=True,
            hide_index=True
        )

        selected_plant = st.selectbox(
            "Show Unit-Level Breakdown",
            plant_totals["Plant"]
            .tolist()
        )

        unit_table = (
            unit_breakdown[
                unit_breakdown["Plant"]
                ==
                selected_plant
            ]
        )

        st.markdown(
            f"##### {selected_plant} Unit Breakdown"
        )

        st.dataframe(
            unit_table.round(2),
            use_container_width=True,
            hide_index=True
        )

        total_dependable = (
            unit_table[
                "DependableMW"
            ].sum()
        )

        st.metric(
            "Plant Total Dependable Capacity",
            f"{total_dependable:,.2f} MW"
        )
