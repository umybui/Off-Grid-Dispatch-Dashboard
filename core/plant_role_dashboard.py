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

        • Larger bubbles = larger average generation output

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

    fig = px.scatter(
        df,
        x="PeakSharePct",
        y="EnergySharePct",
        size="AvgMW",
        color="Plant",
        text="Plant",
        hover_data=[
            "Role"
        ]
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
        x=x_mid * 1.5,
        y=y_mid * 1.5,
        text="CORE ASSETS",
        showarrow=False
    )

    fig.add_annotation(
        x=x_mid * 0.5,
        y=y_mid * 1.5,
        text="BASELOAD",
        showarrow=False
    )

    fig.add_annotation(
        x=x_mid * 1.5,
        y=y_mid * 0.5,
        text="PEAKING",
        showarrow=False
    )

    fig.add_annotation(
        x=x_mid * 0.5,
        y=y_mid * 0.5,
        text="SUPPORT",
        showarrow=False
    )

    fig.update_layout(
        height=600,
        xaxis_title="Peak Demand Contribution (%)",
        yaxis_title="Annual Energy Contribution (%)"
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
                    "AvgMW",
                    "EnergySharePct",
                    "PeakSharePct",
                    "Role"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )
