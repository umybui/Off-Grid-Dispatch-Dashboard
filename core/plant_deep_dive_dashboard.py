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
    
    monthly_perf = (
        plant_gen
        .assign(
            MonthDate=
            plant_gen["Datetime"]
            .dt.to_period("M")
            .dt.to_timestamp(),
    
            Month=
            plant_gen["Datetime"]
            .dt.strftime("%b %Y")
        )
        .groupby(
            ["MonthDate", "Month"],
            as_index=False
        )
        .agg(
            PeakMW=("Value", "max"),
            AvgMW=("Value", "mean"),
            EnergyMWh=("Value", "sum")
        )
        .sort_values(
            "MonthDate"
        )
    )
    
    fig_monthly = go.Figure()
    
    fig_monthly.add_trace(
        go.Scatter(
            x=monthly_perf["Month"],
            y=monthly_perf["PeakMW"],
            mode="lines+markers",
            name="Monthly Peak MW"
        )
    )
    
    fig_monthly.add_trace(
        go.Scatter(
            x=monthly_perf["Month"],
            y=monthly_perf["AvgMW"],
            mode="lines+markers",
            name="Monthly Average MW"
        )
    )
    
    if dependable_mw > 0:
    
        fig_monthly.add_hline(
            y=dependable_mw,
            line_dash="dash",
            line_color="red",
            annotation_text=
                f"Dependable MW ({dependable_mw:.2f})"
        )
    
    fig_monthly.update_layout(
        title=
            f"{selected_plant} Capability Performance by Month",
        xaxis_title="Month",
        yaxis_title="MW",
        height=450
    )
    
    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

    st.caption(
        """
        Monthly Performance evaluates whether the plant
        can consistently achieve its dependable capacity.
    
        • Monthly Peak MW shows the highest output achieved each month.
    
        • Monthly Average MW shows how heavily the plant was utilized.
    
        • The dashed red line represents dependable capacity.
    
        Interpretation:
    
        • Peak MW reaching the dependable line indicates the plant
          remains capable of delivering its rated output.
    
        • A growing gap between Peak MW and Dependable MW may indicate
          derating, maintenance activity, resource limitations,
          fuel constraints, or dispatch restrictions.
    
        • A wide gap between Peak MW and Average MW generally indicates
          peaking or reserve-support operation.
        """
    )
    
    view_mode = st.radio(
        "Performance Resolution",
        [
            "Monthly",
            "Daily Detail"
        ],
        horizontal=True,
        key="plant_perf_resolution"
    )

    if view_mode == "Daily Detail":
    
        available_months = (
            plant_gen["Datetime"]
            .dt.to_period("M")
            .dt.to_timestamp()
            .drop_duplicates()
            .sort_values()
            .tolist()
        )
    
        selected_month = st.selectbox(
            "Select Month",
            available_months,
            format_func=lambda x: x.strftime("%b %Y"),
            key="plant_daily_month"
        )
    
        daily_df = (
            plant_gen[
                plant_gen["Datetime"]
                .dt.to_period("M")
                .dt.to_timestamp()
                ==
                selected_month
            ]
            .copy()
        )
    
        daily_perf = (
            daily_df
            .assign(
                Day=
                daily_df["Datetime"]
                .dt.strftime("%Y-%m-%d")
            )
            .groupby(
                "Day",
                as_index=False
            )
            .agg(
                PeakMW=("Value", "max"),
                AvgMW=("Value", "mean"),
                EnergyMWh=("Value", "sum")
            )
        )
    
        fig_daily = go.Figure()
    
        fig_daily.add_trace(
            go.Scatter(
                x=daily_perf["Day"],
                y=daily_perf["PeakMW"],
                mode="lines+markers",
                name="Daily Peak MW"
            )
        )
    
        fig_daily.add_trace(
            go.Scatter(
                x=daily_perf["Day"],
                y=daily_perf["AvgMW"],
                mode="lines+markers",
                name="Daily Average MW"
            )
        )
    
        if dependable_mw > 0:
    
            fig_daily.add_hline(
                y=dependable_mw,
                line_dash="dash",
                line_color="red",
                annotation_text=
                    f"Dependable MW ({dependable_mw:.2f})"
            )
    
        fig_daily.update_layout(
            title=
                f"{selected_plant} Daily Performance",
            xaxis_title="Date",
            yaxis_title="MW",
            height=450
        )
    
        st.plotly_chart(
            fig_daily,
            use_container_width=True
        )
    
        st.caption(
            """
            Daily Detail allows operators to identify
            specific days where plant performance
            deviated from dependable capability.
            """
        )
        
    with st.expander(
        "View Detailed Plant Analytics",
        expanded=False
    ):

        monthly = (
            plant_gen
            .assign(
                MonthDate=
                plant_gen["Datetime"]
                .dt.to_period("M")
                .dt.to_timestamp(),
        
                Month=
                plant_gen["Datetime"]
                .dt.strftime("%b %Y")
            )
            .groupby(
                ["MonthDate", "Month"],
                as_index=False
            )
            .agg(
                EnergyMWh=("Value", "sum"),
                PeakMW=("Value", "max"),
                AvgMW=("Value", "mean")
            )
            .sort_values(
                "MonthDate"
            )
        )

        st.markdown(
            "##### Monthly Performance"
        )

        monthly_display = (
            monthly.copy()
            .drop(
                columns=["MonthDate"]
            )
        )
        
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

    monthly_asset = monthly.copy()

        monthly_asset["DependableMW"] = dependable_mw
        
        monthly_asset["CapabilityPct"] = (
            monthly_asset["PeakMW"]
            /
            dependable_mw
            * 100
            if dependable_mw > 0
            else 0
        )
        
        monthly_asset["UtilizationPct"] = (
            monthly_asset["AvgMW"]
            /
            dependable_mw
            * 100
            if dependable_mw > 0
            else 0
        )
        
        monthly_asset["PeakSupportPct"] = peak_support_pct
        
        monthly_asset = (
            monthly_asset[
                [
                    "Month",
                    "DependableMW",
                    "CapabilityPct",
                    "UtilizationPct",
                    "PeakSupportPct"
                ]
            ]
        )
        
        monthly_asset["DependableMW"] = (
            monthly_asset["DependableMW"]
            .map(lambda x: f"{x:,.2f}")
        )
        
        monthly_asset["CapabilityPct"] = (
            monthly_asset["CapabilityPct"]
            .map(lambda x: f"{x:,.2f}%")
        )
        
        monthly_asset["UtilizationPct"] = (
            monthly_asset["UtilizationPct"]
            .map(lambda x: f"{x:,.2f}%")
        )
        
        monthly_asset["PeakSupportPct"] = (
            monthly_asset["PeakSupportPct"]
            .map(lambda x: f"{x:,.2f}%")
        )
        
        st.markdown(
            "##### Monthly Asset Summary"
        )
        
        st.dataframe(
            monthly_asset,
            use_container_width=True,
            hide_index=True
        )


        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )
