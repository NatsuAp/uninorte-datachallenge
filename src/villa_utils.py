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

def vill_plot_age_by_estrato(datosColombia23):
    # Convert 'estrato' column to numeric, handling errors
    datosColombia23['estrato'] = pd.to_numeric(datosColombia23['estrato'], errors='coerce')

    # Drop rows with missing values in 'estrato'
    datosColombia23 = datosColombia23.dropna(subset=['estrato'])

    # Create a Plotly figure
    fig = go.Figure()

    # Add a box plot for each 'estrato' category
    for estrato in sorted(datosColombia23['estrato'].unique()):
        fig.add_trace(go.Box(
            y=datosColombia23[datosColombia23['estrato'] == estrato]['EDAD'],
            name=f'Estrato {int(estrato)}',
            boxmean=True,  # Show mean line
            marker_color='skyblue',
            width=0.5  # Set the width of the boxes
        ))

    # Update layout for the plot
    fig.update_layout(
        title="Distribución de Edad por Estrato",
        xaxis_title="Estrato",
        yaxis_title="Edad",
        template="plotly_white",
        height=600,
        margin=dict(l=40, r=40, t=80, b=120),
        boxmode='group'  # Group the boxes by 'estrato'
    )
    return fig


def vill_plot_dengue_cases_by_estrato(datosColombia23):
    # Filter data for Dengue cases and count by 'estrato'
    dengue_by_estrato = datosColombia23[datosColombia23['Nombre_evento'] == 'DENGUE']['estrato'].value_counts().reset_index()
    dengue_by_estrato.columns = ['estrato', 'Frequency']
    dengue_by_estrato["estrato"] = dengue_by_estrato["estrato"].astype(str).apply(lambda x: x.strip())
    dengue_by_estrato_fil = dengue_by_estrato[dengue_by_estrato["estrato"] != ""]

    # Create the bar chart using Plotly
    fig = go.Figure()

    # Add the bar chart trace
    fig.add_trace(go.Bar(
        x=dengue_by_estrato_fil['estrato'],  # x-axis: estrato
        y=dengue_by_estrato_fil['Frequency'],  # y-axis: frequency of cases
        name='Casos de Dengue'
    ))

    # Update the layout of the chart
    fig.update_layout(
        title="Estrato vs Casos de Dengue",
        xaxis_title="Estrato",
        yaxis_title="Casos de Dengue",
        template="plotly_white",
        height=600,
        margin=dict(l=40, r=40, t=80, b=120)
    )

    # Show the interactive plot
    return fig

def vill_plot_dengue_age_comparison(datosColombia23):
    # Filter data for Dengue and Severe Dengue cases
    Dengue = datosColombia23[datosColombia23['Nombre_evento'].isin(['DENGUE', 'DENGUE GRAVE'])]

    # Create the box plot using Plotly
    fig = go.Figure()

    # Add a box trace for Dengue cases
    fig.add_trace(go.Box(
        y=Dengue[Dengue['Nombre_evento'] == 'DENGUE']['EDAD'],
        name='Dengue',
        boxmean=True,  # Show mean line
        marker_color='skyblue'
    ))

    # Add a box trace for Severe Dengue cases
    fig.add_trace(go.Box(
        y=Dengue[Dengue['Nombre_evento'] == 'DENGUE GRAVE']['EDAD'],
        name='Dengue Grave',
        boxmean=True,  # Show mean line
        marker_color='lightcoral'
    ))

    # Update layout for the plot
    fig.update_layout(
        title="Comparacion Tipo de Dengue por Edad",
        xaxis_title="Tipo de Dengue",
        yaxis_title="Edad",
        template="plotly_white",
        height=600,
        margin=dict(l=40, r=40, t=80, b=120)
    )

    return fig


def vill_plot_dengue_proportion_by_gender(datosColombia23):
    # Calculate sizes for Dengue cases by gender
    dengueH = datosColombia23[(datosColombia23["SEXO"] == "M") & (datosColombia23["Nombre_evento"] == "DENGUE")]["SEXO"]
    dengueF = datosColombia23[(datosColombia23["SEXO"] == "F") & (datosColombia23["Nombre_evento"] == "DENGUE")]["SEXO"]
    sizes_dengue = [dengueH.shape[0], dengueF.shape[0]]

    # Calculate sizes for Severe Dengue cases by gender
    dengueGraveH = datosColombia23[(datosColombia23["SEXO"] == "M") & (datosColombia23["Nombre_evento"] == "DENGUE GRAVE")]["SEXO"]
    dengueGraveF = datosColombia23[(datosColombia23["SEXO"] == "F") & (datosColombia23["Nombre_evento"] == "DENGUE GRAVE")]["SEXO"]
    sizes_grave = [dengueGraveH.shape[0], dengueGraveF.shape[0]]

    # Labels for the pie charts
    labels = ['Hombres', 'Mujeres']

    # Create the first pie chart for Dengue cases
    fig = make_subplots(rows=1,
                        cols=2,
                        subplot_titles=("Proporción de Dengue por Género", "Proporción de Dengue Grave por Género"),
                        specs=[[{"type": "domain"},{"type": "domain"}]])

    fig.add_trace(go.Pie(
        labels=labels,
        values=sizes_dengue,
        textinfo='label+percent',
        hoverinfo='label+value+percent',
        marker=dict(colors=['skyblue', 'lightcoral']),
        hole=0.3,  # Optional: makes it a donut chart
        pull=[0.1, 0],  # "explode" effect for the first slice
    ), row=1, col=1)

    # Create the second pie chart for Severe Dengue cases
    fig.add_trace(go.Pie(
        labels=labels,
        values=sizes_grave,
        textinfo='label+percent',
        hoverinfo='label+value+percent',
        marker=dict(colors=['skyblue', 'lightcoral']),
        hole=0.3,  # Optional: makes it a donut chart
        pull=[0.1, 0],  # "explode" effect for the first slice
        domain=dict(x=[0.55, 1.0])  # Position it on the right
    ), row=1, col=2)

    # Update the layout for the subplots
    fig.update_layout(
        title="Proporción de Dengue y Dengue grave por Género (2023)",
        height=600,
        showlegend=False,
    )

    return fig

def vill_plot_stacked_dengue_cases(datosColombia23):
    # Filter data for "DENGUE" and "DENGUE GRAVE" and group by month
    casosDengueMes = datosColombia23[datosColombia23["Nombre_evento"] == "DENGUE"].groupby(datosColombia23["INI_SIN"].str.split("-").str[1]).size()
    casosDengueGraveMes = datosColombia23[datosColombia23["Nombre_evento"] == "DENGUE GRAVE"].groupby(datosColombia23["INI_SIN"].str.split("-").str[1]).size()

    # Rename columns for clarity
    casosDengueMes = casosDengueMes.rename('Cases_Dengue')
    casosDengueGraveMes = casosDengueGraveMes.rename('Cases_Grave')

    # Reset index and prepare data for merging
    casosDengueMes = casosDengueMes.reset_index(name='Cases_Dengue')
    casosDengueMes = casosDengueMes.rename(columns={'INI_SIN': 'Month'})
    casosDengueGraveMes = casosDengueGraveMes.reset_index(name='Cases_Grave')
    casosDengueGraveMes = casosDengueGraveMes.rename(columns={'INI_SIN': 'Month'})

    # Merge data for both Dengue and Severe Dengue cases
    casosDengue = pd.merge(casosDengueMes, casosDengueGraveMes, on='Month', suffixes=('_Dengue', '_Grave'))

    # Ensure the months are ordered correctly
    month_order = [str(i).zfill(2) for i in range(1, 13)]
    casosDengue['Month'] = pd.Categorical(casosDengue['Month'], categories=month_order, ordered=True)
    casosDengue = casosDengue.sort_values('Month')

    # Create the stacked bar chart using Plotly
    fig = go.Figure()

    # Add the bar for dengue cases
    fig.add_trace(go.Bar(
        x=casosDengue['Month'],
        y=casosDengue['Cases_Dengue'],
        name='Dengue',
        marker_color='rgb(55, 83, 109)'
    ))

    # Add the bar for severe dengue cases, stacked on top of dengue cases
    fig.add_trace(go.Bar(
        x=casosDengue['Month'],
        y=casosDengue['Cases_Grave'],
        name='Dengue Grave',
        marker_color='rgb(26, 118, 255)'
    ))

    # Update layout for stacked bars and axis labels
    fig.update_layout(
        barmode='stack',  # Stacked bar chart
        title="Casos de Dengue y Dengue grave por Mes",
        xaxis_title="Mes",
        yaxis_title="Numero de casos",
        xaxis=dict(
            tickmode='array',
            tickvals=month_order,
            ticktext=[f"{calendar.month_name[i]}" for i in range(1, 13)]
        ),
        template='plotly_white',
        height=600,
        margin=dict(l=40, r=40, t=80, b=120)
    )
    
    return fig


def vill_plot_dengue_cases_by_month(datosColombia23):
    # Extract the 'INI_SIN' column (dates of cases)
    fechas = datosColombia23["INI_SIN"]

    # Ensure the 'fechas' column is string data and extract the month
    fechas = pd.to_datetime(fechas)
    fechas_count = fechas.dt.month_name()
    meses = fechas_count.value_counts().reset_index()
    meses.columns = ["Mes", "Count"]
    # Create a list of full month names from calendar.month_name, skipping the first empty string
    month_order = list(calendar.month_name[1:])

    # Convert 'Mes' column to categorical type with ordered month names
    meses['Mes'] = pd.Categorical(meses['Mes'], categories=month_order, ordered=True)

    # Sort the DataFrame by the ordered 'Mes' column
    meses = meses.sort_values('Mes')

    # Create a Plotly histogram
    fig = go.Figure()

    # Add the histogram trace
    fig.add_trace(go.Bar(
        x = meses["Mes"],
        y = meses["Count"],
        marker_color='rgb(55, 83, 109)',  # Custom color
        opacity=0.75,  # Slight transparency for better look
        name="Dengue Cases"  # Name of the trace
    ))

    # Update layout for the histogram
    fig.update_layout(
        title="Dengue Cases by Month - 2023",
        xaxis_title="Mes",
        yaxis_title="Número de Casos",
        template="plotly_white",
        margin=dict(l=40, r=40, t=80, b=120)  # Adjust margins to prevent overlap
    )

    # Show the interactive plot
    return fig

def vill_plot_dengue_density_bar_by_deparment(datosColombia23):
    # Load GeoJSON data for Colombia
    with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json') as response:
        geojson_data = json.load(response)

    # Group by department and event name to get Dengue cases
    densidadDengue = datosColombia23.groupby('Departamento_ocurrencia')['Nombre_evento'].apply(lambda x: (x == 'DENGUE').sum()).reset_index()
    densidadDengue.columns = ['Departamento', 'Dengue Cases']

    # Group by department and event name to get Severe Dengue cases
    densidadGrave = datosColombia23.groupby('Departamento_ocurrencia')['Nombre_evento'].apply(lambda x: (x == 'DENGUE GRAVE').sum()).reset_index()
    densidadGrave.columns = ['Departamento', 'Severe Dengue Cases']

    # Merge Dengue and Severe Dengue data
    datosDensidad = pd.merge(densidadDengue, densidadGrave, on='Departamento')

    # Adjust department names to match GeoJSON
    department_name_fixes = {
        "VALLE": "VALLE DEL CAUCA",
        "SAN ANDRES": "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA",
        "BOGOTA": "SANTAFE DE BOGOTA D.C",
        "GUAJIRA": "LA GUAJIRA",
        "NORTE SANTANDER": "NORTE DE SANTANDER"
    }
    datosDensidad['Departamento'] = datosDensidad['Departamento'].replace(department_name_fixes)

    # Add population data for each department
    datosDensidad["Poblacion"] = [
        81000, 6680000, 269000, 2580000, 2200000, 1250000, 1000000, 405000, 428000, 
        1400000, 1180000, 550000, 1800000, 3000000, 100000, 45000, 890000, 85000, 
        1280000, 1350000, 1130000, 1900000, 1460000, 350000, 545000, 980000, 62000, 
        2300000, 915000, 1440000, 4700000, 41000, 110000
    ]

    # Calculate incidence per 100k population (Riesgo)
    datosDensidad['riesgo'] = (datosDensidad['Dengue Cases'] / datosDensidad['Poblacion']) * 100000

    # Ensure department names in GeoJSON match DataFrame
    for feature in geojson_data['features']:
        feature['id'] = feature['properties']['NOMBRE_DPT']

    # Create the bar chart for "Incidencia por Departamento"
    fig_bar = go.Figure()

    # Shorten department names to 10 characters for readability
    shortened_departments = datosDensidad["Departamento"].apply(lambda x: x[:10])

    # Full department names for the hover
    full_department_names = datosDensidad["Departamento"]

    # Add the bar chart trace
    fig_bar.add_trace(go.Bar(
        x=shortened_departments,  # Shortened names on x-axis
        y=datosDensidad["riesgo"],  # Incidence values
        hovertext=full_department_names,  # Full names in hover
        hoverinfo='text+y',  # Show full department name and y value in hover
        marker_color='rgb(55, 83, 109)',  # Custom color
    ))

    # Customize the layout of the bar chart
    fig_bar.update_layout(
        title="Incidencia Dengue por Departamento",
        xaxis_title="Departamento",
        yaxis_title="Incidencia por cada 100.000",
        xaxis_tickangle=-90,  # Rotate x-axis labels
        height=600,
        template="plotly_white",
        margin=dict(l=40, r=40, t=80, b=120)  # Adjust margins to prevent label overlap
    )
    
    return fig_bar

def vill_plot_dengue_choropleth(datosColombia23):
    # Load GeoJSON data for Colombia
    with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json') as response:
        geojson_data = json.load(response)

    # Group by department and event name to get Dengue cases
    densidadDengue = datosColombia23.groupby('Departamento_ocurrencia')['Nombre_evento'].apply(lambda x: (x == 'DENGUE').sum()).reset_index()
    densidadDengue.columns = ['Departamento', 'Dengue Cases']

    # Group by department and event name to get Severe Dengue cases
    densidadGrave = datosColombia23.groupby('Departamento_ocurrencia')['Nombre_evento'].apply(lambda x: (x == 'DENGUE GRAVE').sum()).reset_index()
    densidadGrave.columns = ['Departamento', 'Severe Dengue Cases']

    # Merge Dengue and Severe Dengue data
    datosDensidad = pd.merge(densidadDengue, densidadGrave, on='Departamento')

    # Adjust department names to match GeoJSON
    department_name_fixes = {
        "VALLE": "VALLE DEL CAUCA",
        "SAN ANDRES": "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA",
        "BOGOTA": "SANTAFE DE BOGOTA D.C",
        "GUAJIRA": "LA GUAJIRA",
        "NORTE SANTANDER": "NORTE DE SANTANDER"
    }
    datosDensidad['Departamento'] = datosDensidad['Departamento'].replace(department_name_fixes)

    # Add population data for each department
    datosDensidad["Poblacion"] = [
        81000, 6680000, 269000, 2580000, 2200000, 1250000, 1000000, 405000, 428000, 
        1400000, 1180000, 550000, 1800000, 3000000, 100000, 45000, 890000, 85000, 
        1280000, 1350000, 1130000, 1900000, 1460000, 350000, 545000, 980000, 62000, 
        2300000, 915000, 1440000, 4700000, 41000, 110000
    ]

    # Calculate incidence per 100k population (Riesgo)
    datosDensidad['riesgo'] = (datosDensidad['Dengue Cases'] / datosDensidad['Poblacion']) * 100000

    # Ensure department names in GeoJSON match DataFrame
    for feature in geojson_data['features']:
        feature['id'] = feature['properties']['NOMBRE_DPT']

    # Create the choropleth map figure
    fig = go.Figure()

    # Add the initial trace for dengue cases
    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=datosDensidad['Departamento'],
        z=datosDensidad['Dengue Cases'],
        colorscale='sunsetdark',
        colorbar_title="Casos de Dengue",
        visible=True,
        featureidkey="properties.NOMBRE_DPT"
    ))

    # Add trace for severe dengue cases (initially hidden)
    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=datosDensidad['Departamento'],
        z=datosDensidad['Severe Dengue Cases'],
        colorscale='redor',
        colorbar_title="Casos de Dengue Grave",
        visible=False,
        featureidkey="properties.NOMBRE_DPT"
    ))

    # Add trace for incidence (Riesgo) (initially hidden)
    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=datosDensidad['Departamento'],
        z=datosDensidad['riesgo'],
        colorscale='YlOrRd',
        colorbar_title="Riesgo por 100k",
        visible=False,
        featureidkey="properties.NOMBRE_DPT"
    ))

    # Update layout for interactivity
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3.4,
        mapbox_center={"lat": 4.5709, "lon": -74.2973},
        title=dict(
            text="Enfermedad del Dengue - Colombia - 2023",
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=18)
        ),
        annotations=[
            dict(x=0, y=-0.1, xref='paper', yref='paper',
                 text='-Bogotá es la única entidad sin población en riesgo. ', showarrow=False, font=dict(size=9)),
            dict(x=0, y=-0.15, xref='paper', yref='paper',
                 text='-Datos de Población es una estimación en 2023 de los Datos recogidos por el Censo Nacional de Población y Vivienda en 2018',
                 showarrow=False, font=dict(size=9))
        ],
        updatemenus=[
            dict(
                type="buttons",
                direction="down",
                buttons=[
                    dict(
                        args=[{"visible": [True, False, False]}],
                        label="Casos de Dengue",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [False, True, False]}],
                        label="Casos de Dengue Grave",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [False, False, True]}],
                        label="Incidencia",
                        method="update"
                    )
                ]
            )
        ]
    )
    return fig

def vill_plot_frequency_of_visits_over_time_plotly(datosBquilla):
    # Convert 'visit_start_date' to datetime if not already
    datosBquilla["visit_start_date"] = pd.to_datetime(datosBquilla["visit_start_date"], format='%d/%m/%Y', errors='coerce', dayfirst=True)

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
    datosBquilla['visit_start_date'] = pd.to_datetime(datosBquilla['visit_start_date'], format='%d/%m/%Y', errors='coerce', dayfirst=True)
    datosBquilla['visit_end_date'] = pd.to_datetime(datosBquilla['visit_end_date'], format='%d/%m/%Y', errors='coerce', dayfirst=True)
    datosBquilla["birth_datetime"] = pd.to_datetime(datosBquilla["birth_datetime"], format='%d/%m/%Y', errors='coerce', dayfirst=True)

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
