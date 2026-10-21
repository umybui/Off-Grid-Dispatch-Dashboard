import streamlit as st
import plotly.graph_objects as go

def build_historical_dispatch_dashboard(
    historical_dispatch
):

  st.subheader(
      "Historical Supply-Demand Dispatch"
  )
  
  st.caption(
      """
      Historical dispatch view comparing
      total system demand against plant
      generation output.
  
      Dispatch ordering may be adjusted
      for scenario analysis and merit-order
      planning studies.
      """
  )

  dispatch_basis = st.selectbox(
      "Merit Order Basis",
      [
          "Largest Generator First",
          "Smallest Generator First",
          "Alphabetical",
          "Manual Override"
      ]
  )

  dispatch_df = (
      historical_dispatch[
          "dispatch_order"
      ]
      .copy()
  )

  if dispatch_basis == "Largest Generator First":
  
      pass

  elif dispatch_basis == "Smallest Generator First":
  
      dispatch_df = (
          dispatch_df
          .sort_values(
              "Priority",
              ascending=False
          )
          .reset_index(
              drop=True
          )
      )
  
      dispatch_df[
          "Priority"
      ] = range(
          1,
          len(dispatch_df)+1
      )

  elif dispatch_basis == "Alphabetical":
  
      dispatch_df = (
          dispatch_df
          .sort_values(
              "Plant"
          )
          .reset_index(
              drop=True
          )
      )
  
      dispatch_df[
          "Priority"
      ] = range(
          1,
          len(dispatch_df)+1
      )

  elif dispatch_basis == "Manual Override":
  
      dispatch_df = st.data_editor(
          dispatch_df,
          use_container_width=True,
          hide_index=True
      )

  with st.expander(
      "Merit Order Dispatch Scenario",
      expanded=True
  ):
  
      st.dataframe(
          dispatch_df,
          use_container_width=True,
          hide_index=True
      )

  generation = (
      historical_dispatch[
          "generation"
      ]
  )
  
  total_demand = (
      historical_dispatch[
          "total_demand"
      ]
  )

  fig = go.Figure()

  for plant in dispatch_df["Plant"]:
  
      plant_df = (
          generation[
              generation["Plant"]
              == plant
          ]
      )
  
      fig.add_trace(
          go.Scatter(
              x=plant_df["Datetime"],
              y=plant_df["Value"],
              stackgroup="one",
              name=plant
          )
      )

  total_supply = (
      generation
      .groupby(
          "Datetime",
          as_index=False
      )["Value"]
      .sum()
  )

  fig.add_trace(
      go.Scatter(
          x=total_supply["Datetime"],
          y=total_supply["Value"],
          line=dict(
              color="red",
              width=2
          ),
          name="TOTAL SUPPLY"
      )
  )

  fig.add_trace(
      go.Scatter(
          x=total_demand["Datetime"],
          y=total_demand["DemandMW"],
          line=dict(
              color="black",
              width=3
          ),
          name="TOTAL DEMAND"
      )
  )

  fig.update_layout(
      height=700,
      yaxis_title="MW",
      xaxis_title="Datetime",
      hovermode="x unified"
  )

  st.plotly_chart(
      fig,
      use_container_width=True
  )
