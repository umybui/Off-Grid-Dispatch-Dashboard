import streamlit as st


def get_filters(df):

    st.sidebar.header("Filters")

    month_names = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }

    # ----------------------------------
    # YEAR
    # ----------------------------------

    available_years = sorted(
        df["Datetime"]
        .dt.year
        .dropna()
        .unique()
    )

    selected_years = st.sidebar.multiselect(
        "Year",
        options=available_years,
        default=available_years
    )

    # ----------------------------------
    # MINDORO AREA
    # ----------------------------------

    selected_areas = []

    if "SourceWorkbook" in df.columns:

        selected_areas = st.sidebar.multiselect(
            "Mindoro Area",
            [
                "Oriental Mindoro",
                "Occidental Mindoro"
            ],
            default=[
                "Oriental Mindoro",
                "Occidental Mindoro"
            ]
        )

    # ----------------------------------
    # MONTH
    # ----------------------------------

    available_months = sorted(
        df["Month"]
        .dropna
