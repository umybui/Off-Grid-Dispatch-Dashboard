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

    available_months = sorted(
        df["Month"].dropna().unique()
    )

    selected_months = st.sidebar.multiselect(
        "Month",
        options=available_months,
        default=available_months,
        format_func=lambda x: month_names.get(x, x)
    )

    available_days = sorted(
        df["Day"].dropna().unique()
    )

    selected_days = st.sidebar.multiselect(
        "Day of Month",
        options=available_days,
        default=available_days
    )

    show_demand = st.sidebar.checkbox(
        "Show Total Demand",
        value=True
    )

    return {
        "selected_months": selected_months,
        "selected_days": selected_days,
        "show_demand": show_demand
    }
