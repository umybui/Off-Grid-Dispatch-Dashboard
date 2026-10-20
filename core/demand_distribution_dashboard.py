import streamlit as st

def build_demand_distribution_dashboard(
    demand_distribution
):

    st.subheader(
        "Demand Distribution Analysis"
    )
    
    b1, b2 = st.columns(2)
    
    with b1:
    
        st.plotly_chart(
            demand_distribution[
                "daily_peak_fig"
            ],
            use_container_width=True
        )
    
    with b2:
    
        st.plotly_chart(
            demand_distribution[
                "hourly_fig"
            ],
            use_container_width=True
        )

    st.caption(
        """
        Demand variability is summarized using box-and-whisker analysis.
    
        Daily Peak Demand by Month illustrates the monthly distribution of daily system peaks. Median,
        interquartile range, whiskers, and outliers provide insight into seasonal demand behavior,
        peak-growth trends, and extreme loading events.
    
        Hourly Demand Distribution illustrates demand variability by hour of day across the selected
        study period. This reveals characteristic load shapes, demand concentration during peak hours,
        overnight minimum-load periods, and the consistency of hourly demand patterns.
    
        Outliers represent atypical demand observations that may warrant further investigation.
        Together, the charts provide a concise view of both monthly peak-demand variability and
        intraday load behavior.
        """
    )

    st.subheader(
        "Hour-Date Demand Heatmap (% of Peak Demand)"
    )
    
    st.plotly_chart(
        demand_distribution[
            "heatmap_fig"
        ],
        use_container_width=True
    )
    
    with st.expander(
        "View Heatmap Source Data",
        expanded=False
    ):
    
        st.dataframe(
            demand_distribution[
                "heatmap_table"
            ].round(1),
            use_container_width=True
        )
