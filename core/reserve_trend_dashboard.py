import streamlit as st


def build_reserve_trend_dashboard(
    reserve_trend
):

    st.subheader(
        "Monthly Reserve Compliance Trend"
    )

    st.plotly_chart(
        reserve_trend["figure"],
        use_container_width=True
    )

    with st.expander(
        "Monthly Reserve Compliance Data",
        expanded=False
    ):

        st.dataframe(
            reserve_trend["monthly"],
            use_container_width=True
        )
