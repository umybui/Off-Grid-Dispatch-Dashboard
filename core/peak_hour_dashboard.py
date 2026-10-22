with st.expander(
    "Peak Hour Snapshot (90%-100% of Peak Demand)",
    expanded=False
):

    display_cols = [
        col
        for col in [
            "Plant",
            "Unit",
            "AvgPeakMW",
            "MaxPeakMW",
            "PeakEnergyMWh",
            "PeakEnergySharePct",
            "PlantSharePct"
        ]
        if col in snapshot.columns
    ]

    st.dataframe(
        snapshot[
            display_cols
        ].round(2),
        use_container_width=True,
        hide_index=True
    )
