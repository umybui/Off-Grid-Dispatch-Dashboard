import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def build_plant_deep_dive_dashboard(
    generation,
    asset_performance,
    peak_support,
    capacity_reference
):

    st.subheader(
        "Plant Intelligence Center"
    )

    st.caption(
        """
        Provides a focused operational and planning view
        of a selected generating plant.

        This section consolidates production,
        capability realization, dependable capacity,
        utilization, and peak-demand support into a
        single asset profile for planners,
        operators, and management.
        """
    )

    plants = sorted(
        generation["Plant"]
        .dropna()
        .unique()
    )

    selected_plant = st.selectbox(
        "Select Plant",
        plants,
        key="plant_intelligence_center"
    )

    plant_gen = (
        generation[
            generation["Plant"]
            ==
            selected_plant
        ]
        .copy()
    )

    energy_mwh = (
        plant_gen["Value"]
        .sum()
    )

    avg_mw = (
        plant_gen["Value"]
        .mean()
    )

    peak_mw = (
        plant_gen["Value"]
        .max()
    )

    hours_operated = (
        plant_gen["Value"]
        .gt(0)
        .sum()
    )

    asset_row = (
        asset_performance[
            asset_performance["Plant"]
            ==
            selected_plant
        ]
    )

    dependable_mw = 0
    capability_pct = 0
    utilization_pct = 0
    risk_flag = "N/A"

    if not asset_row.empty:

        dependable_mw = float(
            asset_row[
                "DependableMW"
            ]
            .iloc[0]
        )

        capability_pct = float(
            asset_row[
                "CapabilityRealizationPct"
            ]
            .iloc[0]
        )

        utilization_pct = float(
            asset_row[
                "UtilizationFactorPct"
            ]
            .iloc[0]
        )

        risk_flag = (
            asset_row[
                "RiskFlag"
            ]
            .iloc[0]
        )

    peak_row = (
        peak_support[
            peak_support["Plant"]
            ==
            selected_plant
        ]
    )

    peak_support_pct = 0

    if not peak_row.empty:

        peak_support_pct = float(
            peak_row[
                "PeakSupportPct"
            ]
            .max()
        )

    c1, c2, c3, c4, c5, c6 = (
        st.columns(6)
    )

    with c1:
        st.metric(
            "Dependable MW",
            f"{dependable_mw:,.2f}"
        )

    with c2:
        st.metric(
            "Peak MW",
            f"{peak_mw:,.2f}"
        )

    with c3:
        st.metric(
            "Average MW",
            f"{avg_mw:,.2f}"
        )

    with c4:
        st.metric(
            "Energy MWh",
            f"{energy_mwh:,.0f}"
        )

    with c5:
        st.metric(
            "Capability %",
            f"{capability_pct:,.1f}%"
        )

    with c6:
        st.metric(
            "Peak Support %",
            f"{peak_support_pct:,.1f}%"
        )

    ldc = (
        plant_gen["Value"]
        .sort_values(
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )

    percent_time = (
        (ldc.index + 1)
        /
        len(ldc)
        * 100
    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(
            x=percent_time,
            y=ldc,
            mode="lines",
            name=selected_plant,
            line=dict(
                width=3
            )
        )
    )

    if dependable_mw > 0:

        fig.add_hline(
            y=dependable_mw,
            line_dash="dash",
            annotation_text=
                f"Dependable MW ({dependable_mw:.2f})"
        )

    fig.update_layout(
        title=
            f"{selected_plant} Output Duration Curve",
        xaxis_title=
            "Percent of Time Exceeded (%)",
        yaxis_title=
            "Output (MW)",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        """
        How to read the Output Duration Curve:
    
        • The curve ranks all operating hours from highest output to lowest output.
    
        • The left side represents the plant's strongest operating hours.
    
        • The right side represents periods when the plant carried less load or was unavailable.
    
        • A flatter curve indicates a consistently utilized plant capable of sustaining output over long periods.
    
        • A steep curve indicates a plant that is primarily used for peak support, reserve support, or intermittent service.
    
        • The dashed line represents the plant's dependable capacity.
    
        Interpretation:
    
        • If the curve stays near the dependable-capacity line for a large portion of the study period, the plant is providing sustained dependable service.
    
        • If output exceeds dependable capacity, the unit occasionally delivered performance above its dependable rating.
    
        • Significant drop-offs or long low-output tails may indicate dispatch limitations, outages, maintenance activity, fuel constraints, seasonal resource limitations, or peaking operation.
        """
    )
    
    with st.expander(
        "View Detailed Plant Analytics",
        expanded=False
    ):

        monthly = (
            plant_gen
            .assign(
                Month=
                plant_gen[
                    "Datetime"
                ]
                .dt.strftime("%b %Y")
            )
            .groupby(
                "Month",
                as_index=False
            )
            .agg(
                EnergyMWh=(
                    "Value",
                    "sum"
                ),
                PeakMW=(
                    "Value",
                    "max"
                ),
                AvgMW=(
                    "Value",
                    "mean"
                )
            )
        )

        st.markdown(
            "##### Monthly Performance"
        )

        monthly_display = monthly.copy()
        
        monthly_display["EnergyMWh"] = (
            monthly_display["EnergyMWh"]
            .map(lambda x: f"{x:,.2f}")
        )
        
        monthly_display["PeakMW"] = (
            monthly_display["PeakMW"]
            .map(lambda x: f"{x:,.2f}")
        )
        
        monthly_display["AvgMW"] = (
            monthly_display["AvgMW"]
            .map(lambda x: f"{x:,.2f}")
        )
        
        st.dataframe(
            monthly_display,
            use_container_width=True,
            hide_index=True
        )

        summary = pd.DataFrame(
            {
                "Metric": [
                    "Dependable MW",
                    "Peak MW",
                    "Average MW",
                    "Energy MWh",
                    "Operating Hours",
                    "Capability %",
                    "Utilization %",
                    "Peak Support %",
                    "Risk Flag"
                ],
                "Value": [
                    dependable_mw,
                    peak_mw,
                    avg_mw,
                    energy_mwh,
                    hours_operated,
                    capability_pct,
                    utilization_pct,
                    peak_support_pct,
                    risk_flag
                ]
            }
        )

        summary["Value"] = summary["Value"].apply(
            lambda x:
            (
                f"{x:,.2f}"
                if isinstance(
                    x,
                    (int, float)
                )
                else x
            )
        )
        
        st.markdown(
            "##### Asset Summary"
        )

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )
