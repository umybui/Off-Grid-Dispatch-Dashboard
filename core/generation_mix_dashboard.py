import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def build_generation_mix_dashboard(
    generation,
    config
):
    show_breakdown = st.toggle(
        "Break down by power plant",
        value=False
    )

    with st.sidebar.expander(
        "Technology Mapping",
        expanded=False
    ):
    
        plant_mapping = pd.DataFrame(
            {
                "Plant": sorted(
                    generation["Plant"]
                    .dropna()
                    .unique()
                )
            }
        )
    
        plant_mapping["Technology"] = (
            plant_mapping["Plant"]
            .map(
                config.get(
                    "TECHNOLOGY_MAPPING",
                    {}
                )
            )
            .fillna("Other")
        )
    
        plant_mapping = st.data_editor(
            plant_mapping,
            column_config={
                "Technology":
                st.column_config.SelectboxColumn(
                    "Technology",
                    options=[
                        "Bunker",
                        "Diesel",
                        "Thermal",
                        "Solar",
                        "Hydro",
                        "Wind",
                        "Biomass",
                        "Other"
                    ]
                )
            },
            hide_index=True,
            use_container_width=True
        )
    
        technology_map = dict(
            zip(
                plant_mapping["Plant"],
                plant_mapping["Technology"]
            )
        )

        st.caption(
            "Copy this dictionary into TECHNOLOGY_MAPPING in config."
        )
    
        st.code(
            repr(technology_map),
            language="python"
        )
    
    generation_mix = generation.copy()
    
    generation_mix["Technology"] = (
        generation_mix["Plant"]
        .map(technology_map)
        .fillna("Other")
    )
    
    tech_colors = {
        "Diesel": "#1565C0",
        "Thermal": "#E53935",
        "Bunker": "#FB8C00",
        "Solar": "#FDD835",
        "Hydro": "#00ACC1",
        "Wind": "#26A69A",
        "Biomass": "#7CB342",
        "Other": "#757575"
    }
    
    # =====================================================
    # TECHNOLOGY ORDER
    # =====================================================
    
    technology_order = (
        generation_mix
        .groupby(
            "Technology"
        )["Value"]
        .sum()
        .sort_values(
            ascending=False
        )
        .index
        .tolist()
    )
    
    # =====================================================
    # TOGGLE LOGIC
    # =====================================================
    
    if show_breakdown:
    
        tech_mix = (
            generation_mix
            .groupby(
                ["Technology", "Plant"],
                as_index=False
            )["Value"]
            .sum()
        )
    
        tech_mix["Share"] = (
            tech_mix["Value"]
            /
            tech_mix["Value"].sum()
            * 100
        )
    
        tech_mix["Technology"] = pd.Categorical(
            tech_mix["Technology"],
            categories=technology_order,
            ordered=True
        )
    
        tech_mix = tech_mix.sort_values(
            ["Technology", "Share"],
            ascending=[True, False]
        )
    
        tech_mix.rename(
            columns={
                "Plant": "Display"
            },
            inplace=True
        )
    
    else:
    
        tech_mix = (
            generation_mix
            .groupby(
                "Technology",
                as_index=False
            )["Value"]
            .sum()
        )
    
        tech_mix["Share"] = (
            tech_mix["Value"]
            /
            tech_mix["Value"].sum()
            * 100
        )
    
        tech_mix["Technology"] = pd.Categorical(
            tech_mix["Technology"],
            categories=technology_order,
            ordered=True
        )
    
        tech_mix = tech_mix.sort_values(
            "Technology"
        )
    
        tech_mix.rename(
            columns={
                "Technology": "Display"
            },
            inplace=True
        )
    
    fig_tech = go.Figure()
    
    for _, row in tech_mix.iterrows():
    
        fig_tech.add_trace(
            go.Bar(
                y=[""],
                x=[row["Share"]],
                name=row["Display"],
                orientation="h",
            marker_color=(
                tech_colors.get(
                    technology_map.get(
                        row["Display"],
                        "Other"
                    ),
                    "#757575"
                )
                if show_breakdown
                else
                tech_colors.get(
                    row["Display"],
                    "#757575"
                )
            ),
                text=(
                    f"{row['Display']}<br>"
                    f"{row['Share']:.1f}%"
                ),
                textposition="inside"
            )
        )

    fig_tech.update_layout(
        barmode="stack",
        height=220,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=40
        ),
        xaxis_title=
            "Share of Generated Energy (%)",
        showlegend=False
    )
    
    st.plotly_chart(
        fig_tech,
        use_container_width=True
    )

    # =====================================================
    # MONTHLY GENERATION SHARE BY TECHNOLOGY
    # =====================================================
    
    st.subheader(
        "Monthly Generation Share by Technology"
    )
    
    monthly_tech = generation_mix.copy()
    
    monthly_tech["Month"] = (
        monthly_tech["Datetime"]
        .dt.strftime("%b %Y")
    )
    
    # Hidden chronological sort column
    monthly_tech["MonthSort"] = (
        monthly_tech["Datetime"]
        .dt.to_period("M")
    )
    
    monthly_tech = (
        monthly_tech
        .groupby(
            ["Month", "MonthSort", "Technology"],
            as_index=False
        )["Value"]
        .sum()
    )
    
    # =====================================================
    # COMPUTE MONTHLY SHARE
    # =====================================================
    
    monthly_total = (
        monthly_tech
        .groupby("Month")["Value"]
        .transform("sum")
    )
    
    monthly_tech["SharePct"] = (
        monthly_tech["Value"]
        /
        monthly_total
        * 100
    )
    
    # =====================================================
    # CREATE MATRIX
    # =====================================================
    
    tech_matrix = (
        monthly_tech
        .pivot(
            index="Technology",
            columns="Month",
            values="SharePct"
        )
        .fillna(0)
    )
    
    # =====================================================
    # ENSURE MONTHS ARE PROPERLY SORTED
    # =====================================================
    
    month_order = (
        monthly_tech[
            ["Month", "MonthSort"]
        ]
        .drop_duplicates()
        .sort_values(
            "MonthSort"
        )["Month"]
        .tolist()
    )
    
    tech_matrix = tech_matrix[
        month_order
    ]
    
    # =====================================================
    # CONSISTENT TECHNOLOGY ORDER
    # =====================================================
    
    technology_order = [
        tech
        for tech in tech_colors.keys()
        if tech in tech_matrix.index
    ]
    
    tech_matrix = tech_matrix.reindex(
        technology_order
    )
    
    # =====================================================
    # HEATMAP
    # =====================================================
    
    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=tech_matrix.values,
            x=tech_matrix.columns,
            y=tech_matrix.index,
            text=
                tech_matrix.round(1)
                .astype(str)
                + "%",
            texttemplate="%{text}",
            colorscale="Blues",
            zmin=0,
            zmax=100,
            colorbar=dict(
                title="% Share"
            )
        )
    )
    
    # =====================================================
    # FORMAT LAYOUT OF HEATMAP
    # =====================================================
    
    fig_heatmap.update_layout(
        height=250,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )
    
    # =====================================================
    # DISPLAY HEATMAP
    # =====================================================
    
    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )
    
    # =====================================================
    # Matrix Table
    # =====================================================
    
    with st.expander(
        "View Monthly Technology Share Matrix (%)",
        expanded=False
    ):
    
        st.dataframe(
            tech_matrix.round(1),
            use_container_width=True
        )
