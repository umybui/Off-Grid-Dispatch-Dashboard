import streamlit as st
import pandas as pd
import plotly.graph_objects as go

try:
    from streamlit_sortables import sort_items
    SORTABLE_AVAILABLE = True
except:
    SORTABLE_AVAILABLE = False


def build_historical_dispatch_dashboard(
    generation,
    total_demand,
    total_generation
):

    st.subheader(
        "Historical Supply-Demand Dispatch"
    )

    peak_demand = (
        total_demand["Value"]
        .max()
    )

    peak_supply = (
        total_generation["TotalGeneration"]
        .max()
    )

    max_shortage = (
        (
            total_demand["Value"]
            -
            total_generation["TotalGeneration"]
        )
        .clip(lower=0)
        .max()
    )

    min_supply = (
        total_generation["TotalGeneration"]
        .min()
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Peak Demand",
            f"{peak_demand:,.2f} MW"
        )

    with c2:
        st.metric(
            "Peak Supply",
            f"{peak_supply:,.2f} MW"
        )

    with c3:
        st.metric(
            "Maximum Shortage",
            f"{max_shortage:,.2f} MW"
        )

    with c4:
        st.metric(
            "Minimum Supply",
            f"{min_supply:,.2f} MW"
        )

    merit_basis = st.selectbox(
        "Merit Order Basis",
        [
            "Largest Generator First",
            "Smallest Generator First",
            "Alphabetical",
            "Manual Override"
        ],
        key="historical_dispatch_order"
    )

    plant_stats = (
        generation
        .groupby(
            "Plant",
            as_index=False
        )
        .agg(
            AvgMW=("Value", "mean"),
            EnergyMWh=("Value", "sum")
        )
    )

    if merit_basis == "Alphabetical":

        plant_order = sorted(
            generation["Plant"]
            .dropna()
            .unique()
        )

    elif merit_basis == "Smallest Generator First":

        plant_order = (
            plant_stats
            .sort_values(
                "EnergyMWh",
                ascending=True
            )["Plant"]
            .tolist()
        )

    else:

        plant_order = (
            plant_stats
            .sort_values(
                "EnergyMWh",
                ascending=False
            )["Plant"]
            .tolist()
        )

    st.caption(
        """
        Largest Generator First:
        Dispatches high-capacity plants first.

        Smallest Generator First:
        Dispatches smaller units first.

        Alphabetical:
        Orders plants alphabetically.

        Manual Override:
        Allows custom dispatch sequencing.
        """
    )

    with st.expander(
        "View Merit Order Dispatch Scenario",
        expanded=False
    ):

        if (
            merit_basis
            == "Manual Override"
            and
            SORTABLE_AVAILABLE
        ):

            plant_order = sort_items(
                items=plant_order,
                direction="vertical"
            )

        merit_order_tbl = pd.DataFrame(
            {
                "Priority":
                range(
                    1,
                    len(plant_order) + 1
                ),
                "Plant":
                plant_order
            }
        )

        st.dataframe(
            merit_order_tbl,
            use_container_width=True,
            hide_index=True
        )

    fig = go.Figure()

    # -------------------------------------
    # STACKED GENERATION
    # -------------------------------------

    for plant in plant_order:

        temp = generation[
            generation["Plant"]
            == plant
        ]

        fig.add_trace(
            go.Scatter(
                x=temp["Datetime"],
                y=temp["Value"],
                mode="lines",
                stackgroup="generation",
                name=plant
            )
        )

    # -------------------------------------
    # TOTAL DEMAND
    # -------------------------------------

    fig.add_trace(
        go.Scatter(
            x=total_demand["Datetime"],
            y=total_demand["Value"],
            mode="lines",
            name="TOTAL DEMAND",
            line=dict(
                color="black",
                width=3
            )
        )
    )

    # -------------------------------------
    # SUPPLY CURVE FROM STACK
    # -------------------------------------

    gap_df = (
        total_demand
        .merge(
            total_generation.rename(
                columns={
                    "TotalGeneration":
                    "TotalSupply"
                }
            ),
            on="Datetime",
            how="inner"
        )
    )

    gap_df.rename(
        columns={
            "Value":
            "TotalDemand"
        },
        inplace=True
    )

    gap_df = gap_df.sort_values(
        "Datetime"
    )

    gap_df["ShortageArea"] = (
        gap_df["TotalDemand"]
        -
        gap_df["TotalSupply"]
    ).clip(lower=0)

    # -------------------------------------
    # INVISIBLE LOWER BOUNDARY
    # -------------------------------------

    fig.add_trace(
        go.Scatter(
            x=gap_df["Datetime"],
            y=gap_df["TotalSupply"],
            mode="lines",
            line=dict(
                width=0
            ),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    # -------------------------------------
    # ORANGE SHORTAGE GAP
    # -------------------------------------

    fig.add_trace(
        go.Scatter(
            x=gap_df["Datetime"],
            y=(
                gap_df["TotalSupply"]
                +
                gap_df["ShortageArea"]
            ),
            mode="lines",
            fill="tonexty",
            fillcolor="rgba(255,140,0,0.35)",
            line=dict(
                width=0
            ),
            name="SHORTAGE",
            customdata=list(
                zip(
                    gap_df["TotalDemand"],
                    gap_df["TotalSupply"],
                    gap_df["ShortageArea"]
                )
            ),
            
            hovertemplate=
                "<b>Supply Deficit</b><br>"
                "Demand: %{customdata[0]:.2f} MW<br>"
                "Supply: %{customdata[1]:.2f} MW<br>"
                "Shortage: %{customdata[2]:.2f} MW"
                "<extra></extra>""
        )
    )

    # -------------------------------------
    # LAYOUT
    # -------------------------------------

    fig.update_layout(
        title="Historical Dispatch Stack",
        hovermode="x unified",
        height=900,
        yaxis_title="MW",
        xaxis_title="Datetime",
        legend_title="Plant",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )

    fig.update_xaxes(
        rangeslider_visible=True
    )

    st.caption(
        """
        This chart compares historical generation dispatch
        against total system demand.

        • Black Line = Total Demand

        • Stacked Plant Areas = Total Supply

        • Orange Area = Supply Deficit / Shortage

        Hover over the orange region to view
        shortage magnitude.

        Dispatch order affects stacking sequence
        only and does not modify historical generation.
        """
    )

    st.caption(
        "Tip: Double-click any legend entry to isolate a plant."
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
