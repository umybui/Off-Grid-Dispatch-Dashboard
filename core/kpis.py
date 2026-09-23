def build_kpis(
    total_demand,
    total_generation,
    reliability
):

    peak_generation_mw = (
        total_generation["TotalGeneration"]
        .max()
    )

    demand_energy_mwh = (
        total_demand["Value"]
        .sum()
    )

    generated_energy_mwh = (
        total_generation["TotalGeneration"]
        .sum()
    )

    energy_served_pct = (
        (
            demand_energy_mwh
            -
            reliability["unserved_energy"]
        )
        /
        demand_energy_mwh
        * 100
        if demand_energy_mwh > 0
        else 0
    )

    average_load = (
        total_demand["Value"]
        .mean()
    )

    load_factor = (
        average_load
        /
        reliability["peak_demand"]
        * 100
        if reliability["peak_demand"] > 0
        else 0
    )

    return {
        "peak_generation_mw": peak_generation_mw,
        "demand_energy_mwh": demand_energy_mwh,
        "generated_energy_mwh": generated_energy_mwh,
        "energy_served_pct": energy_served_pct,
        "average_load": average_load,
        "load_factor": load_factor
    }
