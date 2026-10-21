import streamlit as st


def build_reserve_deficiency_dashboard(
    operating_condition,
    reserve_deficiency_table
):

    st.subheader(
        "Operating Condition Breakdown"
    )

    st.caption(
        """
        Operating conditions are categorized into:

        • Adequate Reserve Hours

        • Reserve Deficient Hours

        • Unserved Demand Hours

        This provides a high-level view of system
        security and reliability throughout the
        selected study period.
        """
    )

    st.plotly_chart(
        operating_condition["figure"],
        use_container_width=True
    )

    with st.expander(
        "Reserve Deficient Hours",
        expanded=False
    ):

        st.dataframe(
            reserve_deficiency_table.round(
                {
                    "TotalDemand": 2,
                    "TotalSupply": 2,
                    "ReserveMargin": 2,
                    "RequiredReserve": 2,
                    "ReserveDeficiency": 2
                }
            ),
            use_container_width=True,
            hide_index=True
        )
