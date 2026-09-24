def build_reserve_assessment(
    reliability
):

    gap_df = reliability["gap_df"]

    total_hours = len(gap_df)

    hours_low_reserve = (
        gap_df["ReserveMargin"]
        <
        gap_df["RequiredReserve"]
    ).sum()

    reserve_compliance_pct = (
        (
            total_hours
            -
            hours_low_reserve
        )
        /
        total_hours
        * 100
        if total_hours > 0
        else 0
    )

    return {

        "hours_low_reserve":
            hours_low_reserve,

        "reserve_compliance_pct":
            reserve_compliance_pct,

        "max_reserve_margin":
            gap_df["ReserveMargin"].max(),

        "min_reserve_margin":
            gap_df["ReserveMargin"].min(),

        "average_reserve_margin":
            gap_df["ReserveMargin"].mean(),

        "average_required_reserve":
            gap_df["RequiredReserve"].mean()
    }
