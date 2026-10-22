import streamlit as st

def build_executive_summary(
    reliability,
    kpis,
    capacity_planning,
    transfer_flow=none
):
    peak_row = reliability["gap_df"].loc[
        reliability["gap_df"]["TotalDemand"].idxmax()
    ]
    
    peak_datetime = peak_row["Datetime"]

    reserve_margin = (
        capacity_planning["available_capacity"]
        -
        reliability["peak_demand"]
    )
    
    reserve_margin_pct = (
        reserve_margin
        /
        reliability["peak_demand"]
        * 100
        if reliability["peak_demand"] > 0
        else 0
    )
    
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
    
    r2c1, r2c2, r2c3, r2c4, r2c5, r2c6 = st.columns(6)
    
    with r2c1:
        st.metric(
            "Hours with Shortage",
            f"{reliability['hours_with_shortage']:,}"
        )
    
    with r2c2:
        st.metric(
            "Reserve Margin",
            f"{reserve_margin:,.2f} MW",
        )

    with r2c3:
            st.metric(
                "Low Reserve Hours",
                f"{reliability['hours_low_reserve']:,}"
            )
    
    with r2c4:
        st.metric(
            "Load Factor",
            f"{kpis['load_factor']:.1f}%"
        )
    
    with r2c5:
        st.metric(
            "Peak Demand Time",
            peak_datetime.strftime(
                "%Y-%m-%d %H:%M"
            )
        )

    max_transfer_mw = 0
    transfer_energy_mwh = 0
    
    if (
        transfer_flow is not None
        and not transfer_flow.empty
    ):
    
        transfer_col = None
    
        for col in [
            "TransferMW",
            "ImportSupport",
            "Value"
        ]:
    
            if col in transfer_flow.columns:
                transfer_col = col
                break
    
        if transfer_col:
    
            max_transfer_mw = (
                transfer_flow[transfer_col]
                .abs()
                .max()
            )
    
            transfer_energy_mwh = (
                transfer_flow[transfer_col]
                .abs()
                .sum()
            )
    
    with r2c6:
    
        if transfer_energy_mwh > 0:
    
            st.metric(
                "Interconnection Support",
                f"{transfer_energy_mwh:,.0f} MWh",
                delta=f"Peak {max_transfer_mw:.2f} MW"
            )
    
        else:
    
            st.metric(
                "Interconnection Support",
                "N/A"
            )
