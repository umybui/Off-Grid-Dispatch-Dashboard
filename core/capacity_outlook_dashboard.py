import streamlit as st
import pandas as pd


def build_capacity_outlook_dashboard(
    capacity_planning,
    capacity_reference
):

    st.subheader(
        "Capacity Planning Assumptions"
    )

    col1, col2 = st.columns(2)

    with col1:

        growth_pct = st.slider(
            "Economic Growth (%)",
            min_value=1.0,
            max_value=10.0,
            value=3.0,
            step=0.5
        )

    with col2:

        retired_plants = st.multiselect(
            "Retired / Unavailable Plants",
            options=sorted(
                capacity_reference[
                    "Plant"
                ].unique()
            )
        )

    peak_demand = (
        capacity_planning[
            "peak_demand"
        ]
    )

    remaining_capacity = (
        capacity_reference[
            ~capacity_reference[
                "Plant"
            ].isin(
                retired_plants
            )
        ][
            "DependableMW"
        ].sum()
    )

    projected_peak = (
        peak_demand
        *
        (
            (1 + growth_pct / 100)
            ** 10
        )
    )

    additional_capacity = max(
        0,
        projected_peak
        -
        remaining_capacity
    )

    st.subheader(
        f"Capacity Outlook @ {growth_pct:.1f}% Economic Growth"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Current Peak Demand",
        f"{peak_demand:.2f} MW"
    )

    c2.metric(
        "Projected Peak Demand",
        f"{projected_peak:.2f} MW"
    )

    c3.metric(
        "Available Capacity",
        f"{remaining_capacity:.2f} MW"
    )

    c4.metric(
        "Additional Capacity Needed",
        f"{additional_capacity:.2f} MW"
    )

    margin = (
        remaining_capacity
        -
        projected_peak
    )

    if margin > 20:

        st.success(
            "Low Risk: Capacity remains sufficient under the selected planning assumptions."
        )

    elif margin > 10:

        st.info(
            "Moderate Risk: Capacity remains adequate but planning reserves are reduced."
        )

    elif margin > 0:

        st.warning(
            "High Risk: System reserve margin becomes very limited."
        )

    else:

        st.error(
            f"Capacity Deficit: Additional capacity of {abs(margin):.2f} MW is required."
        )

    projection_rows = []

    for year in range(11):

        forecast_peak = (
            peak_demand
            *
            (
                (1 + growth_pct / 100)
                ** year
            )
        )

        capacity_margin = (
            remaining_capacity
            -
            forecast_peak
        )

        required_capacity = max(
            0,
            forecast_peak
            -
            remaining_capacity
        )

        projection_rows.append(
            {
                "Year Ahead":
                    year,
                "Projected Peak MW":
                    round(
                        forecast_peak,
                        2
                    ),
                "Capacity Margin MW":
                    round(
                        capacity_margin,
                        2
                    ),
                "Additional Capacity Needed MW":
                    round(
                        required_capacity,
                        2
                    )
            }
        )

    projection_df = pd.DataFrame(
        projection_rows
    )

    st.caption(
        f"10-Year Capacity Outlook @ {growth_pct:.1f}% Economic Growth Assumption"
    )

    st.dataframe(
        projection_df,
        use_container_width=True,
        hide_index=True
    )
