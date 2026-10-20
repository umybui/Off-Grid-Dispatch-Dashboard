def build_reserve_dashboard(
    reserve,
    reliability
):

    gap_df = reliability["gap_df"]

    total_hours = len(gap_df)

    unserved_hours = (
        gap_df["ShortageMW"] > 0
    ).sum()

    served_hours = (
        total_hours
        - unserved_hours
    )

    reserve_deficient_hours = (
        gap_df["ReserveMargin"]
        <
        gap_df["RequiredReserve"]
    ).sum()

    worst_reserve_deficiency = (
        (
            gap_df["ReserveMargin"]
            -
            gap_df["RequiredReserve"]
        ).min()
    )

    hours_meeting_requirement = (
        gap_df["ReserveMargin"]
        >=
        gap_df["RequiredReserve"]
    ).sum()

    reserve_security_score = (
        hours_meeting_requirement
        /
        max(served_hours, 1)
        * 100
    )

    avg_regulating_reserve = (
        gap_df["RegulatingReserve"]
        .mean()
    )
    
    avg_contingency_reserve = (
        gap_df["ContingencyReserve"]
        .mean()
    )
    
    avg_required_reserve = (
        gap_df["RequiredReserve"]
        .mean()
    )
    
    hours_below_requirement = (
        gap_df["ReserveMargin"]
        <
        gap_df["RequiredReserve"]
    ).sum()
    
    served_hours_pct = (
        served_hours
        /
        max(total_hours, 1)
        * 100
    )
    
    reserve_compliance = (
        hours_meeting_requirement
        /
        max(served_hours, 1)
        * 100
    )
    
    return {

        "total_hours":
            total_hours,

        "served_hours":
            served_hours,

        "unserved_hours":
            unserved_hours,

        "reserve_deficient_hours":
            reserve_deficient_hours,

        "worst_reserve_deficiency":
            worst_reserve_deficiency,

       "hours_meeting_requirement":
        hours_meeting_requirement,
    
        "reserve_security_score":
        reserve_security_score,

        "avg_regulating_reserve":
            avg_regulating_reserve,
        
        "avg_contingency_reserve":
            avg_contingency_reserve,
        
        "avg_required_reserve":
            avg_required_reserve,
        
        "served_hours_pct":
            served_hours_pct,
        
        "reserve_compliance":
            reserve_compliance,
        
        "hours_below_requirement":
            hours_below_requirement,
        
    }
