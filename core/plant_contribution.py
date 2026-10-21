import plotly.express as px


def build_plant_contribution(
    generation
):

    contribution = (
        generation
        .groupby(
            "Plant",
            as_index=False
        )
        .agg(
            EnergyMWh=(
                "MW",
                "sum"
            )
        )
    )

    total_energy = (
        contribution["EnergyMWh"]
        .sum()
    )

    contribution["ContributionPct"] = (
        contribution["EnergyMWh"]
        /
        max(total_energy, 1)
        * 100
    )

    contribution = (
        contribution
        .sort_values(
            "ContributionPct",
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )

    fig = px.treemap(
        contribution,
        path=["Plant"],
        values="EnergyMWh",
        color="ContributionPct",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        title="Generation Share Treemap",
        height=500,
        margin=dict(
            t=40,
            l=10,
            r=10,
            b=10
        )
    )

    return {

        "figure":
            fig,

        "contribution":
            contribution
    }
