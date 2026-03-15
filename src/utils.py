import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

import plotly.express as px
from plotly.subplots import make_subplots
import calendar
from mpl_toolkits.basemap import Basemap
from scipy.io import netcdf
from netCDF4 import Dataset


import json
from urllib.request import urlopen

def load_netcdf_file(f_path):
        data = Dataset(f_path, mode='r') # read the data
        x = data["X"][:]
        y = data["Y"][:]
        time = data["T"][:]
        pre = data["precipitation"][:]
        return x, y, time, pre

@st.cache_data
def load_file(filename, sep=","):
    df = None
    try:
        df = pd.read_csv(filename, sep=sep)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    except Exception as e:
        st.write(f"Error al cargar el archivo: {e}")
          
    
    return df


    # Calculate the interquartile range (IQR) and outliers
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    upper_bound = Q3 + 1.5 * IQR
    lower_bound = Q1 - 1.5 * IQR

    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    percentage_outliers = (len(outliers) / len(df)) * 100

    # Print the percentage of outliers
    print(f"Porcentaje de datos atipicos: {percentage_outliers:.2f}%")

    # Create the box plot with Plotly
    fig = go.Figure()

    # Add the box plot
    fig.add_trace(go.Box(
        x=df[col],
        boxmean=True,  # Shows the mean line
        marker_color='#4682B4',  # Set the box color
        name=col
    ))

    # Update layout
    fig.update_layout(
        title=f"Boxplot de la columna: {col}",
        xaxis_title=f"{col}",
        yaxis_title="Colombia",
        xaxis=dict(
            tickmode='array',
            tickvals=np.arange(min(df[col]), max(df[col]) + 1, 8)  # Set custom ticks
        ),
        template='plotly_white',
        showlegend=False
    )

    # Show the plot
    return fig