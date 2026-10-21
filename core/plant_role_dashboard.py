import streamlit as st
import plotly.express as px


def build_plant_role_dashboard(
    plant_role_matrix
):

    st.subheader(
        "Plant Role Matrix"
    )

    st.markdown(
        """
        ##### How to Read This Chart

        • Higher = larger annual energy contribution

        • Further right = larger contribution during peak-demand periods

        • Larger bubbles = larger annual energy production

        ##### Quadrants

        🟩 Upper Right = Core System Assets
        (high energy + high peak support)

        🟦 Upper Left = Baseload-Oriented Assets
        (high energy, lower peak support)

        🟧 Lower Right = Peaking Assets
        (critical during peaks, lower annual energy)

        🟥 Lower Left = Support Assets
        (limited contribution to both energy and peak demand)
        """
    )

    df = plant_role_matrix.copy()

    x_mid = df["PeakSharePct"].median()
    y_mid = df["EnergySharePct"].median()

    role_colors = {
        "Core Asset": "#43A047",
        "Baseload Asset": "#1E88E5",
        "Peaking Asset": "#FB8C00",
        "Support Asset": "#D81B60"
    }
    
    fig = px.scatter(
        df,
        x="PeakSharePct",
        y="EnergySharePct",
        size="EnergyMWh",
        size_max=90,
        color="Role",
        text="Plant",
        color_discrete_map=role_colors,
        hover_data={
            "EnergyMWh": ":,.2f",
            "EnergySharePct": ":.2f",
            "PeakSharePct": ":.2f",
            "Role": True
        }
    )

    seen_roles = set()
    
    for trace in fig.data:
    
        if trace.name in seen_roles:
            trace.showlegend = False
        else:
            seen_roles.add(trace.name)
            trace.showlegend = True

    fig.update_traces(
        textposition="top center",
        textfont=dict(
            size=12,
            color="black"
        ),
        marker=dict(
            line=dict(
                width=1,
                color="white"
            ),
            opacity=0.80
        )
    )

    fig.add_vline(
        x=x_mid,
        line_dash="dash",
        line_color="gray"
    )

    fig.add_hline(
        y=y_mid,
        line_dash="dash",
        line_color="gray"
    )

    fig.add_annotation(
        x=df["PeakSharePct"].max() * 0.75,
        y=df["EnergySharePct"].max() * 0.92,
        text="CORE ASSETS",
        showarrow=False,
        font=dict(size=12)
    )

    fig.add_annotation(
        x=df["PeakSharePct"].max() * 0.15,
        y=df["EnergySharePct"].max() * 0.92,
        text="BASELOAD",
        showarrow=False,
        font=dict(size=12)
    )

    fig.add_annotation(
        x=df["PeakSharePct"].max() * 0.75,
        y=df["EnergySharePct"].max() * 0.05,
        text="PEAKING",
        showarrow=False,
        font=dict(size=12)
    )

    fig.add_annotation(
        x=df["PeakSharePct"].max() * 0.15,
        y=df["EnergySharePct"].max() * 0.05,
        text="SUPPORT",
        showarrow=False,
        font=dict(size=12)
    )

    fig.update_layout(
        height=700,
        xaxis_title="Peak Demand Contribution (%)",
        yaxis_title="Annual Energy Contribution (%)",
        legend_title_text="Role",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.markdown(
        "##### Plant Role Matrix"
    )
    
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    with st.expander(
        "View Plant Role Matrix Data",
        expanded=False
    ):

        st.dataframe(
            df[
                [
                    "Plant",
                    "EnergyMWh",
                    "EnergySharePct",
                    "PeakSharePct",
                    "Role"
                ]
            ]
            .sort_values(
                "EnergySharePct",
                ascending=False
            )
            .round(2),
            use_container_width=True,
            hide_index=True
        )
