import streamlit as st


def build_reserve_deficiency_dashboard(
    operating_condition,
    reserve_deficiency_table
):

    st.subheader(
        "Operating Condition Breakdown"
    )

    st.plotly_chart(
        operating_condition["figure"],
        use_container_width=True
    )

    with st.expander(
        "Operating Condition Data",
        expanded=False
    ):

        st.write(
            f"Adequate Reserve Hours: "
            f"{operating_condition['adequate_hours']:,}"
        )

        st.write(
            f"Reserve Deficient Hours: "
            f"{operating_condition['reserve_deficient_hours']:,}"
        )

        st.write(
            f"Unserved Demand Hours: "
            f"{operating_condition['shortage_hours']:,}"
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
