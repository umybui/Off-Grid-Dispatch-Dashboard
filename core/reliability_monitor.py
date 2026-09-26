def build_reliability_monitor(
    reliability,
    reserve,
    kpis
):

    energy_served = (
        kpis["energy_served_pct"]
    )

    reserve_compliance = (
        reserve[
            "reserve_compliance_pct"
        ]
    )

    shortage_hours = (
        reliability[
            "hours_with_shortage"
        ]
    )

    if (
        energy_served >= 99
        and
        reserve_compliance >= 95
    ):
        overall_status = "Healthy"

    elif (
        energy_served >= 95
        and
        reserve_compliance >=
    ):
        overall_status = "Monitor"

    else:
        overall_status = "Critical"

    return {

        "energy_served_pct":
            energy_served,

        "reserve_compliance_pct":
            reserve_compliance,

        "shortage_hours":
            shortage_hours,

        "overall_status":
            overall_status
    }
