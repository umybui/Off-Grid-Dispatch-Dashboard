import pandas as pd
import plotly.graph_objects as go
import math


def build_demand_distribution(
    total_demand
):

    peak_demand = total_demand["Value"].max()

    average_load = total_demand["Value"].mean()

    load_factor = (
        average_load
        / peak_demand
        * 100
        if peak_demand > 0
        else 0
    )

    # -----------------------------------------
    # Daily Peak Demand by Month
    # -----------------------------------------

    daily_peak = (
        total_demand.assign(
            Date=total_demand["Datetime"].dt.date,
            Month=total_demand["Datetime"].dt.strftime("%b")
        )
        .groupby(
            ["Month", "Date"],
            as_index=False
        )
        .agg(
            DailyPeak=("Value", "max")
        )
    )

    month_order = [
        "Jan","Feb","Mar","Apr",
        "May","Jun","Jul","Aug",
        "Sep","Oct","Nov","Dec"
    ]

    hourly_profile = total_demand.copy()

    hourly_profile["Hour"] = (
        hourly_profile["Datetime"]
        .dt.hour
    )

    common_min = min(
        daily_peak["DailyPeak"].quantile(0.01),
        hourly_profile["Value"].quantile(0.01)
    )

    common_max = max(
        daily_peak["DailyPeak"].quantile(0.99),
        hourly_profile["Value"].quantile(0.99)
    )

    y_min = math.floor(common_min / 5) * 5
    y_max = math.ceil(common_max / 5) * 5

    y_range = y_max - y_min

    if y_range <= 50:
        y_tick = 5
    elif y_range <= 100:
        y_tick = 10
    elif y_range <= 200:
        y_tick = 20
    else:
        y_tick = math.ceil(y_range / 10 / 5) * 5

    fig_peak = go.Figure()

    for month in month_order:

        temp = daily_peak[
            daily_peak["Month"] == month
        ]

        if len(temp) == 0:
            continue

        fig_peak.add_trace(
            go.Box(
                y=temp["DailyPeak"],
                name=month,
                boxmean=True
            )
        )

    fig_peak.update_layout(
        title="Daily Peak Demand by Month",
        yaxis_title="MW",
        height=450
    )

    fig_peak.update_yaxes(
        range=[y_min, y_max],
        dtick=y_tick
    )

    # -----------------------------------------
    # Hourly Demand Distribution
    # -----------------------------------------

    fig_hour = go.Figure()

    for hr in range(24):

        temp = hourly_profile[
            hourly_profile["Hour"] == hr
        ]

        if len(temp) == 0:
            continue

        fig_hour.add_trace(
            go.Box(
                y=temp["Value"],
                name=str(hr),
                boxmean=True
            )
        )

    fig_hour.update_layout(
        title="Hourly Demand Distribution",
        xaxis_title="Hour of Day",
        yaxis_title="MW",
        height=450
    )

    fig_hour.update_yaxes(
        range=[y_min, y_max],
        dtick=y_tick
    )

    # -----------------------------------------
    # Heatmap
    # -----------------------------------------

    heat_source = total_demand.copy()

    heat_source["Date"] = (
        heat_source["Datetime"]
        .dt.strftime("%Y-%m-%d")
    )

    heat_source["Hour"] = (
        heat_source["Datetime"]
        .dt.hour
    )

    heat_source["DemandPctPeak"] = (
        heat_source["Value"]
        / peak_demand
        * 100
    )

    heat_tbl = (
        heat_source
        .pivot_table(
            index="Hour",
            columns="Date",
            values="DemandPctPeak",
            aggfunc="mean"
        )
    )

    fig_heat = go.Figure(
        data=go.Heatmap(
            z=heat_tbl.values,
            x=heat_tbl.columns,
            y=heat_tbl.index,
            colorscale="RdYlGn_r",
            zmin=0,
            zmax=100,
            colorbar_title="% Peak"
        )
    )

    fig_heat.update_layout(
        title="Demand Heatmap (% of System Peak)",
        xaxis_title="Date",
        yaxis_title="Hour",
        height=500
    )

    return {
        "daily_peak_fig": fig_peak,
        "hourly_fig": fig_hour,
        "load_factor": load_factor,
        "heatmap_fig": fig_heat,
        "heatmap_table": heat_tbl
    }
