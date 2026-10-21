import streamlit as st


def build_reserve_security_dashboard(
    reserve,
    reserve_dashboard,
    reliability
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

    st.divider()

    with st.expander(
        "How Reserve Requirement Was Calculated",
        expanded=False
    ):
        gap_df = reliability["gap_df"].copy()
    
        gap_df["Month"] = (
            gap_df["Datetime"]
            .dt.strftime("%b %Y")
        )
    
        selected_month = st.selectbox(
            "Month",
            sorted(
                gap_df["Month"].unique()
            )
        )
    
        month_df = (
            gap_df[
                gap_df["Month"]
                == selected_month
            ]
        )
    
        selected_day = st.selectbox(
            "Day",
            sorted(
                month_df["Datetime"]
                .dt.date
                .astype(str)
                .unique()
            )
        )
    
        day_df = (
            month_df[
                month_df["Datetime"]
                .dt.date
                .astype(str)
                ==
                selected_day
            ]
        )
    
        selected_hour = st.selectbox(
            "Hour",
            day_df["Datetime"]
            .dt.strftime("%H:%M")
            .tolist()
        )
    
        row = day_df[
            day_df["Datetime"]
            .dt.strftime("%H:%M")
            ==
            selected_hour
        ].iloc[0]
    
        c1, c2, c3, c4, c5 = st.columns(5)
    
        with c1:
            st.metric(
                "Demand",
                f"{row['TotalDemand']:.2f} MW"
            )
    
        with c2:
            st.metric(
                "Generation",
                f"{row['TotalGeneration']:.2f} MW"
            )
    
        with c3:
            st.metric(
                "Reserve Margin",
                f"{row['ReserveMargin']:.2f} MW"
            )
    
        with c4:
            st.metric(
                "Required Reserve",
                f"{row['RequiredReserve']:.2f} MW"
            )
    
        with c5:
            st.metric(
                "Reserve Gap",
                f"{row['ReserveMargin'] - row['RequiredReserve']:.2f} MW"
            )
    
        st.markdown("---")
    
        st.markdown(
            "### Reserve Requirement Computation"
        )
    
        st.markdown(
            f"""
            #### Regulating Reserve
    
            = Total Demand × 2.8%
    
            = {row['TotalDemand']:.2f} × 2.8%
    
            = **{row['RegulatingReserve']:.2f} MW**
            """
        )
    
        st.markdown(
            f"""
            #### Contingency Reserve
    
            = Total Generation × 10%
    
            = {row['TotalGeneration']:.2f} × 10%
    
            = **{row['ContingencyReserve']:.2f} MW**
            """
        )
    
        st.markdown(
            f"""
            #### Required Reserve
    
            = Regulating Reserve + Contingency Reserve
    
            = {row['RegulatingReserve']:.2f}
            + {row['ContingencyReserve']:.2f}
    
            = **{row['RequiredReserve']:.2f} MW**
            """
        )
    
        st.markdown(
            f"""
            #### Actual Reserve Margin
    
            = Total Generation − Total Demand
    
            = {row['TotalGeneration']:.2f}
            − {row['TotalDemand']:.2f}
    
            = **{row['ReserveMargin']:.2f} MW**
            """
        )
    
        reserve_gap = (
            row["ReserveMargin"]
            -
            row["RequiredReserve"]
        )
    
        st.markdown(
            "#### Compliance Check"
        )
    
        st.write(
            "Reserve Margin ≥ Required Reserve"
        )
    
        st.write(
            f"{row['ReserveMargin']:.2f} MW "
            f"≥ "
            f"{row['RequiredReserve']:.2f} MW"
        )
    
        if reserve_gap >= 0:
    
            st.success(
                "✓ Reserve Requirement Met"
            )
    
        else:
    
            st.error(
                "✗ Reserve Deficient"
            )
