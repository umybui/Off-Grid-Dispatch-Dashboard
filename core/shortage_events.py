import pandas as pd
import plotly.express as px


def build_shortage_events(
    reliability
):

    gap_df = reliability["gap_df"].copy()

    shortage_df = gap_df[
        gap_df["ShortageMW"] > 0
    ].copy()

    if shortage_df.empty:

        return {
            "events": pd.DataFrame(),
            "monthly_summary": pd.DataFrame(),
            "largest_event": None,
            "longest_event": None,
            "highest_shortage": None,
            "figure": px.scatter()
        }

    shortage_df = shortage_df.sort_values(
        "Datetime"
    )

    shortage_df["HourGap"] = (
        shortage_df["Datetime"]
        .diff()
        .dt.total_seconds()
        .div(3600)
    )

    shortage_df["NewEvent"] = (
        shortage_df["HourGap"]
        .fillna(1)
        .gt(1)
    )

    shortage_df["EventID"] = (
        shortage_df["NewEvent"]
        .cumsum()
    )

    events = (
        shortage_df
        .groupby(
            "EventID"
        )
        .agg(
            Start=(
                "Datetime",
                "min"
            ),
            End=(
                "Datetime",
                "max"
            ),
            DurationHours=(
                "Datetime",
                "count"
            ),
            MaxShortageMW=(
                "ShortageMW",
                "max"
            ),
            UnservedEnergyMWh=(
                "ShortageMW",
                "sum"
            )
        )
        .reset_index()
    )

    events["Month"] = (
        events["Start"]
        .dt.strftime("%b %Y")
    )

    events["Event Number"] = (
        range(
            1,
            len(events) + 1
        )
    )

    monthly_summary = (
        shortage_df
        .assign(
            Month=lambda df:
            df["Datetime"]
            .dt.strftime("%b %Y")
        )
        .groupby(
            "Month"
        )
        .agg(
            UnservedEnergyMWh=(
                "ShortageMW",
                "sum"
            ),
            ShortageHours=(
                "ShortageMW",
                "count"
            ),
            MaxShortageMW=(
                "ShortageMW",
                "max"
            )
        )
        .reset_index()
    )

    fig = px.scatter(
        monthly_summary,
        x="Month",
        y="UnservedEnergyMWh",
        size="ShortageHours",
        color="MaxShortageMW",
        text="Month",
        color_continuous_scale="Reds",
        title="Monthly Reliability Impact Overview"
    )

    fig.update_traces(
        textposition="top center"
    )

    fig.update_layout(
        height=500,
        yaxis_title="Unserved Energy (MWh)",
        xaxis_title="Month"
    )

    largest_event = (
        events.loc[
            events[
                "UnservedEnergyMWh"
            ].idxmax()
        ]
    )

    longest_event = (
        events.loc[
            events[
                "DurationHours"
            ].idxmax()
        ]
    )

    highest_shortage = (
        events.loc[
            events[
                "MaxShortageMW"
            ].idxmax()
        ]
    )

    return {

        "figure":
            fig,

        "events":
            events,

        "monthly_summary":
            monthly_summary,

        "largest_event":
            largest_event,

        "longest_event":
            longest_event,

        "highest_shortage":
            highest_shortage
    }
