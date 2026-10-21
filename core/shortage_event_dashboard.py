import streamlit as st


def build_shortage_event_dashboard(
    shortage_events
):

    if shortage_events["events"].empty:

        st.subheader(
            "Shortage Event Analysis"
        )

        st.success(
            "No shortage events detected."
        )

        return

    events = shortage_events["events"]

    largest_event = (
        shortage_events[
            "largest_event"
        ]
    )

    longest_event = (
        shortage_events[
            "longest_event"
        ]
    )

    highest_shortage = (
        shortage_events[
            "highest_shortage"
        ]
    )

    monthly_summary = (
        shortage_events[
            "monthly_summary"
        ]
    )

    st.subheader(
        "Shortage Event Analysis"
    )

    st.plotly_chart(
        shortage_events["figure"],
        use_container_width=True
    )

    worst_month = (
        monthly_summary.loc[
            monthly_summary[
                "UnservedEnergyMWh"
            ].idxmax()
        ]
    )

    st.info(
        f"Worst Reliability Month: "
        f"{worst_month['Month']}"
        f"\n\n"
        f"• Unserved Energy: "
        f"{worst_month['UnservedEnergyMWh']:.2f} MWh "
        f"• Shortage Hours: "
        f"{worst_month['ShortageHours']} "
        f"• Maximum Shortage: "
        f"{worst_month['MaxShortageMW']:.2f} MW"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Largest Event",
            f"{largest_event['UnservedEnergyMWh']:.2f} MWh"
        )

        st.caption(
            largest_event["Month"]
        )

    with c2:

        st.metric(
            "Longest Event",
            f"{int(longest_event['DurationHours'])} hrs"
        )

        st.caption(
            longest_event["Month"]
        )

    with c3:

        st.metric(
            "Highest Shortage",
            f"{highest_shortage['MaxShortageMW']:.2f} MW"
        )

        st.caption(
            highest_shortage["Month"]
        )

    with st.expander(
        "View Shortage Event Data",
        expanded=False
    ):

        st.dataframe(
            events[
                [
                    "Event Number",
                    "Month",
                    "Start",
                    "End",
                    "DurationHours",
                    "MaxShortageMW",
                    "UnservedEnergyMWh"
                ]
            ].rename(
                columns={
                    "DurationHours":
                    "Duration Hours",

                    "MaxShortageMW":
                    "Max Shortage MW",

                    "UnservedEnergyMWh":
                    "Unserved Energy MWh"
                }
            ).round(2),
            use_container_width=True,
            hide_index=True
        )
