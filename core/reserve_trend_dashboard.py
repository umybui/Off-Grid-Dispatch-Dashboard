import streamlit as st


def build_reserve_trend_dashboard(
    reserve_trend
):

    st.subheader(
        "Monthly Reserve Compliance Trend"
    )

    st.caption(
        """
        Reserve Adequacy (%) is computed as:

        (Hours Meeting Reserve Requirement ÷
        Demand Served Hours) × 100

        Compliance is evaluated hourly using:

        Reserve Margin ≥ Required Reserve
        """
    )

    st.plotly_chart(
        reserve_trend["figure"],
        use_container_width=True
    )

    st.caption(
        """
        Reserve Adequacy Legend:

        ≥95% = Excellent

        90–94.9% = Good

        80–89.9% = Fair

        <80% = Poor
        """
    )

    with st.expander(
        "Monthly Reserve Compliance Data",
        expanded=False
    ):

        st.dataframe(
            reserve_trend["monthly"],
            use_container_width=True,
            hide_index=True
        )
