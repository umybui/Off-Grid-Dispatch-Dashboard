import streamlit as st


def build_capacity_planning_dashboard(
    capacity_planning
):

    st.subheader(
        "Capacity Outlook"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Current Peak Demand",
            f"{capacity_planning['peak_demand']:,.2f}"
        )

    with c2:
        st.metric(
            "Projected Peak Demand",
            f"{capacity_planning['projected_peak']:,.2f}"
        )

    with c3:
        st.metric(
            "Available Capacity",
            f"{capacity_planning['available_capacity']:,.2f}"
        )

    with c4:
        st.metric(
            "Additional Capacity Needed",
            f"{capacity_planning['required_capacity']:,.2f}"
        )

    with st.expander(
        "10-Year Capacity Planning Outlook",
        expanded=False
    ):

        st.dataframe(
            capacity_planning["projection_df"],
            use_container_width=True,
            hide_index=True
        )
