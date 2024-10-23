import pandas as pd
import numpy as np
import plotly.graph_objects as go

import plotly.express as px
from plotly.subplots import make_subplots
import calendar
from mpl_toolkits.basemap import Basemap
from scipy.io import netcdf
from netCDF4 import Dataset


import json
from urllib.request import urlopen

def vill_plot_frequency_of_visits_over_time_plotly(datosBquilla):
    # Convert 'visit_start_date' to datetime if not already
    datosBquilla["visit_start_date"] = pd.to_datetime(datosBquilla["visit_start_date"], format='%d/%m/%Y', errors='coerce')

    # Group by month and count the visits
    visitasenMes = datosBquilla.groupby(datosBquilla["visit_start_date"].dt.to_period("M")).size()

    # Convert the PeriodIndex to string for Plotly
    visit_start_dates = visitasenMes.index.astype(str)

    # Create the line chart using Plotly
    fig = go.Figure()

    # Add the line plot trace
    fig.add_trace(go.Scatter(
        x=visit_start_dates,  # X-axis: Visit start dates (as strings)
        y=visitasenMes.values,  # Y-axis: Frequency of visits
        mode='lines+markers',  # Line with markers
        marker=dict(color='blue'),  # Line color
        name="Frequency of Visits"
    ))

    # Customize the layout of the graph
    fig.update_layout(
        title="Frequency of Visits Over Time",
        xaxis_title="Visit Start Date",
        yaxis_title="Frequency",
        height=600,  # Adjust height as needed
        template='plotly_white',  # Use a clean white template
        xaxis_tickangle=84,  # Rotate x-axis labels for better readability
        margin=dict(l=50, r=50, t=100, b=50)  # Adjust margins to prevent label overlap
    )

    # Adjust x-axis ticks to show every 3rd month
    fig.update_xaxes(
        tickvals=visit_start_dates[::3],  # Show every 3rd month on the x-axis
        ticktext=visit_start_dates[::3]   # Set custom tick text
    )

    # Show the plot
    return fig

def vill_plot_age_distribution_by_gender_plotly(datosBquilla):
    # Ensure 'birth_datetime' is converted to datetime if not already
    datosBquilla["visit_start_date"] = pd.to_datetime(datosBquilla['visit_start_date'], errors='coerce')
    datosBquilla['birth_datetime'] = pd.to_datetime(datosBquilla['birth_datetime'], errors='coerce')

    # Calculate 'Edad' (age) in years
    datosBquilla["Edad"] = ((datosBquilla["visit_start_date"] - datosBquilla["birth_datetime"]).dt.days / 365)

    # Create the boxplot using Plotly
    fig = go.Figure()

    # Add the boxplot traces, one for each gender
    for gender in datosBquilla['gender_source_value'].unique():
        gender_data = datosBquilla[datosBquilla['gender_source_value'] == gender]
        
        fig.add_trace(go.Box(
            y=gender_data['Edad'],  # Age on the y-axis
            x=[gender] * len(gender_data),  # Gender on the x-axis
            name=gender,  # Gender name for the trace
            boxmean=True,  # Show mean line inside the box
            marker_color='#4682B4',  # Color of the box
        ))

    # Update the layout to match the original plot's appearance
    fig.update_layout(
        title="Distribuicion de Edad por Sexo",
        xaxis_title="Sexo",
        yaxis_title="Edad",
        height=600,  # Adjust the height of the plot
        template='plotly_white',  # Use a clean white template
        showlegend=False  # No need for legend as gender is shown on the x-axis
    )
    return fig


def vill_plot_boxplot_duration_internado_plotly(datosBquilla):
    # Ensure 'visit_start_date', 'visit_end_date', and 'birth_datetime' are converted to datetime
    datosBquilla['visit_start_date'] = pd.to_datetime(datosBquilla['visit_start_date'], format='%d/%m/%Y', errors='coerce')
    datosBquilla['visit_end_date'] = pd.to_datetime(datosBquilla['visit_end_date'], format='%d/%m/%Y', errors='coerce')
    datosBquilla["birth_datetime"] = pd.to_datetime(datosBquilla["birth_datetime"], format='%d/%m/%Y', errors='coerce')

    # Calculate 'Duracion Internado' (days hospitalized)
    datosBquilla["Duracion Internado"] = datosBquilla["visit_end_date"] - datosBquilla["visit_start_date"]
    datosBquilla["Duracion Internado"] = datosBquilla["Duracion Internado"].dt.days

    # Create the boxplot using Plotly
    fig = go.Figure()

    # Add the boxplot trace
    fig.add_trace(go.Box(
        x=datosBquilla["Duracion Internado"],  # Plotting 'Duracion Internado' on the x-axis
        name='Dur Hosp',
        boxmean=True,  # Show mean line inside the box
        orientation='h',  # Horizontal boxplot
        marker_color='#4682B4',  # Box color
    ))

    # Update the layout to match the original plot's appearance
    fig.update_layout(
        title="Duracion Internado",
        xaxis_title="Dias",
        yaxis_title="",
        height=600,  # Adjust the height of the plot
        template='plotly_white',  # Use a clean white template
        showlegend=False,  # No need for legend in a single plot
    )

    return fig

def vill_plot_pie_chart_city_distribution(datosBquilla):
    # Count occurrences of each city
    city_counts = datosBquilla['city'].value_counts()

    # Calculate percentages
    total_cases = city_counts.sum()
    city_percentages = (city_counts / total_cases) * 100

    # Filter cities with less than 1% representation
    other_cities = city_percentages[city_percentages < 1]

    # Group cities with less than 1% as "Otras Ciudades"
    other_cities_sum = other_cities.sum()
    main_pie_data = city_percentages[city_percentages >= 1]
    main_pie_data['Otras Ciudades'] = other_cities_sum

    # Create the pie chart using Plotly
    fig = go.Figure()

    # Add pie chart trace
    fig.add_trace(go.Pie(
        labels=main_pie_data.index,  # Labels are the cities
        values=main_pie_data.values,  # Values are the percentages
        hoverinfo='label+percent',  # Show labels and percentages on hover
        textinfo='percent',  # Show percentages on the slices
        textposition='inside',  # Position the text inside the pie chart
        hole=0.3,  # Optional: to create a donut chart, adjust or remove for a full pie chart
    ))

    # Update layout for the plot
    fig.update_layout(
        title="Distribución de ciudades",
        height=600,  # Adjust height as needed
        template='plotly_white'  # Clean white background template
    )
    
    return fig
