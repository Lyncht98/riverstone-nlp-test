from shiny import ui, reactive, App, render
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
df = df.fillna("NaN")

# add year and month columns
df['Y'] = pd.to_datetime(df["time_created"], unit="s").dt.to_period("Y").astype(str)
df['M'] = pd.to_datetime(df["time_created"], unit="s").dt.to_period("M").astype(str)
df['cluster'] = df['cluster'].astype(str)
# make dictionary of cluster and theme column combinations
clusters_dict = df[["cluster", "theme"]].drop_duplicates().set_index("cluster").to_dict()["theme"]

#initialize plot as Y
plot_data = df['Y'].value_counts().sort_index().to_dict()
# initialize selected cluster as the first in the dictionary
df_selected_cluster = df[df["cluster"] == list(clusters_dict.keys())[0]]
table_data = df[["date_created", "up_votes", "title"]]
# set up dictionary for timescale
timescale_dict = {"Y": "Yearly", "M": "Monthly"}

app_ui = ui.page_fluid(
    # select the cluster
    ui.input_radio_buttons("cluster", "Cluster:", choices=clusters_dict),
    # select bins to be month or year
    ui.input_select("timescale", "Timescale:", choices=timescale_dict),
    output_widget("histogram"),
    output_widget("table"),
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
    table = go.FigureWidget(
        data = [
            go.Table(
                header = dict(values = list(table_data.columns)),
                cells = dict(values = table_data.transpose().values.tolist()
                ),
                columnwidth = [2, 1, 10],
            )
        ]
    )


    register_widget("histogram", histogram)
    register_widget('table', table)

    @reactive.Effect
    @reactive.event(input.timescale, input.cluster)
    def _():
        df_selected_cluster = df[df["cluster"] == input.cluster()]
        plot_data = df_selected_cluster[input.timescale()].value_counts().sort_index().to_dict()
        table_data = df_selected_cluster[["date_created", "up_votes", "title"]]

        histogram.data[0].x = list(plot_data.keys())
        histogram.data[0].y = list(plot_data.values())

        table.data[0].header = dict(values = list(table_data.columns))
        table.data[0].cells = dict(values = table_data.transpose().values.tolist())



# This is a shiny.App object. It must be named `app`.
app = App(app_ui, server, debug=True)

if __name__ == "__main__":
    app.run()