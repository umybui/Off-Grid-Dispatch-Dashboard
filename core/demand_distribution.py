import pandas as pd
import plotly.graph_objects as go
import math

def build_demand_distribution(
    total_demand
):

    return {
        "daily_peak_fig": daily_peak_fig,
        "hourly_fig": hourly_fig,
        "load_factor": load_factor,
        "heatmap_fig": heatmap_fig
    }
