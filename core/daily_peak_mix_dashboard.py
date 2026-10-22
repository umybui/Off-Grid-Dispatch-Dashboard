import streamlit as st


def build_daily_peak_mix_dashboard(
    daily_peak_mix
):

    st.subheader(
        "Generation Mix During Daily System Peaks"
    )

    st.caption(
        """
        Evaluates generation mix composition
        during each day's peak-demand hour.

        Values are expressed as the percentage
        contribution of each generating plant
        to daily system peak demand.
        """
    )

    st.plotly_chart(
        daily_peak_mix[
            "figure"
        ],
        use_container_width=True
    )

    with st.expander(
        "View Peak Hour Performance Table",
        expanded=False
    ):

        st.dataframe(
            daily_peak_mix[
                "performance_table"
            ].round(2),
            use_container_width=True,
            hide_index=True
        )
