import streamlit as st


def build_reserve_security_dashboard(
    reserve,
    reserve_dashboard
):

    st.subheader(
        "Reserve Security Assessment"
    )
    
    st.caption(
        """
        This assessment focuses on hours where customer demand
        was successfully served.
    
        Reserve adequacy is evaluated against the operating
        reserve requirement consisting of:
    
        • 2.8% Regulating / Load-Following Reserve
    
        • 10% Contingency Reserve based on Total
          Synchronized Generation
    
        Hours with unserved demand are excluded from
        this assessment and are reported separately
        in the Reliability Health Monitor.
        """
    )
    )
    
    r1, r2, r3 = st.columns(3)
    
    with r1:
        st.metric(
            "Avg Regulating Reserve",
            f"{reserve_dashboard['avg_regulating_reserve']:.2f} MW"
        )
    
    with r2:
        st.metric(
            "Avg Contingency Reserve",
            f"{reserve_dashboard['avg_contingency_reserve']:.2f} MW"
        )
    
    with r3:
        st.metric(
            "Avg Total Required Reserve",
            f"{reserve_dashboard['avg_required_reserve']:.2f} MW"
        )
    
    st.divider()
    
    r1, r2, r3, r4 = st.columns(4)
    
    with r1:
        st.metric(
            "Hours Evaluated",
            reserve_dashboard["total_hours"]
        )
    
    with r2:
        st.metric(
            "Unserved Hours",
            reserve_dashboard["unserved_hours"]
        )
    
    with r3:
        st.metric(
            "Demand Served Hours",
            reserve_dashboard["served_hours"]
        )
    
    with r4:
        st.metric(
            "Served Hours %",
            f"{reserve_dashboard['served_hours_pct']:.1f}%"
        )
    
    st.divider()
    
    r1, r2, r3, r4 = st.columns(4)
    
    with r1:
        st.metric(
            "Reserve Compliance",
            f"{reserve_dashboard['reserve_compliance']:.1f}%"
        )
    
    with r2:
        st.metric(
            "Hours Meeting Requirement",
            reserve_dashboard["hours_meeting_requirement"]
        )
    
    with r3:
        st.metric(
            "Hours Below Requirement",
            reserve_dashboard["hours_below_requirement"]
        )
    
    with r4:
        st.metric(
            "Worst Reserve Deficiency",
            f"{reserve_dashboard['worst_reserve_deficiency']:.2f} MW"
        )
