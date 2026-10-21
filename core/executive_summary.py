import streamlit as st

def build_executive_summary(
    reliability,
    kpis,
    capacity_planning
):
    peak_row = reliability["gap_df"].loc[
        reliability["gap_df"]["TotalDemand"].idxmax()
    ]
    
    peak_datetime = peak_row["Datetime"]
    
    r1c1, r1c2, r1c3, r1c4, r1c5, r1c6 = st.columns(6)
    
    with r1c1:
        st.metric(
            "Peak Demand",
            f"{reliability['peak_demand']:,.2f} MW"
        )

    with r1c2:
    st.metric(
            "Dependable Capacity",
            f"{capacity_planning['available_capacity']:,.2f} MW"
        )
    
    with r1c3:
        st.metric(
            "Demand Energy",
            f"{kpis['demand_energy_mwh']:,.2f} MWh"
        )
    
    with r1c4:
        st.metric(
            "Generated Energy",
            f"{kpis['generated_energy_mwh']:,.2f} MWh"
        )
    
    with r1c5:
        st.metric(
            "Unserved Energy",
            f"{reliability['unserved_energy']:,.2f} MWh"
        )
    
    with r1c6:
        st.metric(
            "Energy Served",
            f"{kpis['energy_served_pct']:.2f}%"
        )
    
    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    
    with r2c1:
        st.metric(
            "Hours with Shortage",
            f"{reliability['hours_with_shortage']:,}"
        )
    
    with r2c2:
        st.metric(
            "Low Reserve Hours",
            f"{reliability['hours_low_reserve']:,}"
        )
    
    with r2c3:
        st.metric(
            "Load Factor",
            f"{kpis['load_factor']:.1f}%"
        )
    
    with r2c4:
        st.metric(
            "Peak Demand Time",
            peak_datetime.strftime(
                "%Y-%m-%d %H:%M"
            )
        )
