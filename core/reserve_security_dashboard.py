import streamlit as st


def build_reserve_security_dashboard(
    reserve,
    reserve_dashboard
):

    st.subheader(
        "Reserve Security Assessment"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Hours Evaluated",
            reserve_dashboard["total_hours"]
        )

    with c2:
        st.metric(
            "Demand Served Hours",
            reserve_dashboard["served_hours"]
        )

    with c3:
        st.metric(
            "Unserved Hours",
            reserve_dashboard["unserved_hours"]
        )

    with c4:
        st.metric(
            "Worst Deficiency",
            f"{reserve_dashboard['worst_reserve_deficiency']:,.2f}"
        )

    st.subheader(
        "Reserve Validation"
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Low Reserve Hours",
            reserve["hours_low_reserve"]
        )

    with c2:
        st.metric(
            "Reserve Compliance %",
            f"{reserve['reserve_compliance_pct']:.2f}%"
        )
