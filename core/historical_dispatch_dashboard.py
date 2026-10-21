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


    with st.expander(
        "Merit Order Dispatch Scenario",
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

    fig.add_trace(
        go.Scatter(
            x=total_generation["Datetime"],
            y=total_generation[
                "TotalGeneration"
            ],
            mode="lines",
            name="TOTAL SUPPLY",
            line=dict(
                color="red",
                width=2
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=total_demand["Datetime"],
            y=total_demand["Value"],
            mode="lines",
            name="TOTAL DEMAND",
            line=dict(
                color="black",
                width=4
            )
        )
    )

    gap_df = (
        total_demand
        .merge(
            total_generation,
            on="Datetime",
            how="inner"
        )
    )

    gap_df["ShortageArea"] = (
        gap_df["Value"]
        -
        gap_df["TotalGeneration"]
    ).clip(lower=0)

    fig.add_trace(
        go.Scatter(
            x=gap_df["Datetime"],
            y=gap_df["TotalGeneration"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=gap_df["Datetime"],
            y=(
                gap_df["TotalGeneration"]
                +
                gap_df["ShortageArea"]
            ),
            mode="lines",
            fill="tonexty",
            fillcolor="rgba(255,140,0,0.8)",
            line=dict(width=0),
            name="SHORTAGE"
        )
    )

    fig.update_layout(
        title="Historical Supply-Demand Dispatch",
        hovermode="x unified",
        height=900,
        yaxis_title="MW",
        xaxis_title="Datetime",
        legend_title="Plant"
    )

    fig.update_xaxes(
        rangeslider_visible=True
    )

    st.caption(
        """
        The dispatch stack shows the contribution of each
        generating plant over time.

        Black Line = Total Demand

        Red Line = Total Supply

        Orange Area = Supply Deficit / Shortage

        The merit-order selector allows simulation of
        alternative dispatch priorities.
        """
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
