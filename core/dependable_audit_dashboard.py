import streamlit as st


def build_dependable_audit_dashboard(
    dependable_audit
):

    st.subheader(
        "Dependable Capacity Audit Trail"
    )
    
    has_unit_data = (
        dependable_audit.get(
            "has_unit_data",
            False
        )
    )
    
    if not has_unit_data:
    
        st.info(
            "Unit-level dependable capacity data "
            "is not available for this system. "
            "Only plant-level dependable capacity "
            "is maintained."
        )
    
    with st.expander(
        "View Dependable Capacity Audit Trail",
        expanded=False
    ):

        st.markdown(
            "##### Plant-Level Dependable Capacity"
        )

        st.dataframe(
            plant_totals.round(2),
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------
        # PALAWAN / CATANDUANES
        # ----------------------------------

        if has_unit_data:

            unit_breakdown = (
                dependable_audit[
                    "unit_breakdown"
                ]
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
                ]
                .sum()
            )

            st.metric(
                "Plant Total Dependable Capacity",
                f"{total_dependable:,.2f} MW"
            )

        # ----------------------------------
        # MINDORO
        # ----------------------------------

        else:

            st.info(
                "Unit-level dependable capacity data "
                "is not available for this system."
            )
