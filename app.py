from shiny import ui, render, App

# making a shiny app that shows a histogram of the selected cluster over time

# packages
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

# data of top three clusters
df = pd.read_csv("./data/df_top_three_clusters.csv")
df['cluster'] = df['cluster'].astype(str)
clusters = df["cluster"].unique()
df['M'] = pd.to_datetime(df["time_created"], unit="s").dt.to_period("M").astype(str)
df['Y'] = pd.to_datetime(df["time_created"], unit="s").dt.to_period("Y").astype(str)

# app_ui
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            # select the cluster
            ui.input_radio_buttons("cluster", "Cluster:", list(clusters)),
            # select bins to be month or year
            ui.input_radio_buttons("bins", "Bins:", ["month", "year"]),
        ),
        ui.panel_main(
            ui.output_plot("histogram"),
        ),
    ),
)

def server(input, output, session):
    @output
    @render.plot(alt="A histogram")
    def histogram():
        # get the selected cluster
        selected_cluster = input.cluster()
        # get the data of the selected cluster
        df_selected_cluster = df[df["cluster"] == selected_cluster]

        if input.bins() == "month":
            plot_data = df['M'].value_counts().sort_index().to_dict()
        else:
            plot_data = df['Y'].value_counts().sort_index().to_dict()
        plt.bar(plot_data.keys(), plot_data.values(), color="blue")
        plt.xticks(rotation=60)

    

    

# This is a shiny.App object. It must be named `app`.
app = App(app_ui, server, debug=True)

if __name__ == "__main__":
    app.run()