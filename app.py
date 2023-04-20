from shiny import ui, reactive, App
from shinywidgets import output_widget, register_widget

# making a shiny app that shows a histogram of the selected cluster over time

# packages
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import plotly.graph_objs as go


# data of top three clusters
df = pd.read_csv("./data/df_top_three_clusters.csv")
# make dictionary of cluster and theme column combinations
clusters_dict = df[["cluster", "theme"]].drop_duplicates().set_index("cluster").to_dict()["theme"]

df['Y'] = pd.to_datetime(df["time_created"], unit="s").dt.to_period("Y").astype(str)
df['M'] = pd.to_datetime(df["time_created"], unit="s").dt.to_period("M").astype(str)

#initialize plot as Y
plot_data = df['Y'].value_counts().sort_index().to_dict()

app_ui = ui.page_fluid(
    # select the cluster
    ui.input_radio_buttons("cluster", "Cluster:", choices=clusters_dict),
    # select bins to be month or year
    ui.input_radio_buttons("bins", "Bins:", ["year", "month"]),
    output_widget("histogram"),
)

def server(input, output, session):
    histogram = go.FigureWidget(
        data = [
            go.Bar(
                x = list(plot_data.keys()),
                y = list(plot_data.values()),
            )
        ],
    )

    register_widget("histogram", histogram)

    @reactive.Effect
    def _():
        selected_cluster = input.cluster()
        df_selected_cluster = df[df["cluster"] == selected_cluster]
        if input.bins() == "month":
            plot_data = df['M'].value_counts().sort_index().to_dict()
        else:
            plot_data = df['Y'].value_counts().sort_index().to_dict()
        histogram.data[0].x = list(plot_data.keys())
        histogram.data[0].y = list(plot_data.values())


# This is a shiny.App object. It must be named `app`.
app = App(app_ui, server, debug=True)

if __name__ == "__main__":
    app.run()