import streamlit as st


def build_plant_contribution_dashboard(
    plant_contribution
):

    contribution = (
        plant_contribution[
            "contribution"
        ]
    )

    st.subheader(
        "Plant Contribution Analysis"
    )

    left, right = st.columns(
        [3, 1]
    )

    with left:

        st.plotly_chart(
            plant_contribution[
                "figure"
            ],
            use_container_width=True
        )

    with right:

        st.markdown(
            "#### Plant Contribution Data"
        )

        display_df = (
            contribution[
                [
                    "Plant",
                    "ContributionPct",
                    "EnergyMWh"
                ]
            ]
            .rename(
                columns={
                    "ContributionPct":
                    "Contribution %",
                    "EnergyMWh":
                    "Energy MWh"
                }
            )
            .round(2)
        )

        table_height = min(
            max(
                len(display_df) * 35,
                300
            ),
            800
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=table_height
        )

    st.caption(
        """
        Plant contribution is based on total
        generated energy over the selected
        study period.

        Contribution (%) =
        Plant Energy ÷ Total System Energy × 100

        The treemap area represents total
        generated energy while color intensity
        represents each plant's percentage
        contribution to total system generation.
        """
    )
