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

def zel_plot_city_histogram_plotly(df):
    # Group by 'city' and count occurrences
    city_counts = df.groupby(df['city']).size()

    # Filter for cities with more than 5 occurrences
    filtered_cities = city_counts[city_counts > 5].index
    filtered_df = df[df['city'].isin(filtered_cities)]

    # Get the filtered city counts
    city_value_counts = filtered_df['city'].value_counts()

    # Create the bar chart using Plotly
    fig = go.Figure()

    # Add the bar chart trace
    fig.add_trace(go.Bar(
        x=city_value_counts.index,   # Cities on the x-axis
        y=city_value_counts.values,  # Frequencies on the y-axis
        marker_color='#4682B4',      # Bar color (blue)
    ))

    # Update the layout of the chart
    fig.update_layout(
        title="Histograma de las Ciudades > 5",
        xaxis_title="Ciudad",
        yaxis_title="Frecuencia",
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        height=600,  # Adjust height as needed
        template="plotly_white"  # Use a clean white template
    )

    return fig

def zel_plot_scatter_age_vs_hospital_days(df):
    # Ensure 'birth_datetime', 'visit_start_date', and 'visit_end_date' are converted to datetime
    df['birth_datetime'] = pd.to_datetime(df['birth_datetime'], format='%d/%m/%Y', errors='coerce')
    df['visit_start_date'] = pd.to_datetime(df['visit_start_date'], format='%d/%m/%Y', errors='coerce')
    df['visit_end_date'] = pd.to_datetime(df['visit_end_date'], format='%d/%m/%Y', errors='coerce')

    # Calculate 'DiasHospitalizado' (days hospitalized) and 'Edad' (age)
    df['DiasHospitalizado'] = (df['visit_end_date'] - df['visit_start_date']).dt.days
    df['Edad'] = df['visit_start_date'].dt.year - df['birth_datetime'].dt.year

    # Create the scatter plot using Plotly
    fig = go.Figure()

    # Add the scatter trace
    fig.add_trace(go.Scatter(
        x=df['Edad'],  # Age on the x-axis
        y=df['DiasHospitalizado'],  # Days hospitalized on the y-axis
        mode='markers',  # Scatter plot (markers only)
        marker=dict(
            size=8,
            color='rgba(0, 123, 255, 0.7)',  # Blue color with transparency
            line=dict(width=1, color='DarkSlateGrey')  # Outline for the markers
        ),
        opacity=0.8  # Set the transparency of the markers
    ))

    # Update the layout for the plot
    fig.update_layout(
        title="Relación entre Edad y Días Hospitalizado",
        xaxis_title="Edad",
        yaxis_title="Días Hospitalizado",
        height=600,  # Adjust height as needed
        template="plotly_white"  # Use a clean white template
    )
    return fig

def zel_plot_boxplot_edad_plotly(df):
    """
    Creates a boxplot of the 'Edad' (age) using Plotly.

    Parameters:
    df (pd.DataFrame): DataFrame containing 'birth_datetime', 'visit_start_date', and 'Edad'.
    """

    # Ensure 'birth_datetime', 'visit_start_date', and 'visit_end_date' are converted to datetime
    df['birth_datetime'] = pd.to_datetime(df['birth_datetime'], format='%d/%m/%Y', errors='coerce')
    df['visit_start_date'] = pd.to_datetime(df['visit_start_date'], format='%d/%m/%Y', errors='coerce')
    df['visit_end_date'] = pd.to_datetime(df['visit_end_date'], format='%d/%m/%Y', errors='coerce')

    # Calculate 'Edad' (age) from 'visit_start_date' and 'birth_datetime'
    df['Edad'] = df['visit_start_date'].dt.year - df['birth_datetime'].dt.year

    # Create the boxplot using Plotly
    fig = go.Figure()

    # Add the boxplot trace (horizontal boxplot)
    fig.add_trace(go.Box(
        x=df['Edad'],  # Plotting 'Edad' on the x-axis
        name='Edad',
        boxmean=True,  # Show mean line
        orientation='h'  # Horizontal boxplot
    ))

    # Update the layout to match the original plot's appearance
    fig.update_layout(
        title="Boxplot de la Edad",
        xaxis_title="Edad",
        yaxis_title="Barranquilla",
        xaxis=dict(
            tickmode='array',
            tickvals=np.arange(df['Edad'].min(), df['Edad'].max() + 1, 10)  # Set custom ticks every 10 years
        ),
        height=400,  # Adjust height if needed
        template='plotly_white',
        showlegend=False,  # No legend is needed for a single boxplot
    )

    # Show grid
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)
    return fig

def zel_plot_timeline_condition_start_date_plotly(DF):
    # Convert 'condition_start_date' to datetime
    DF['condition_start_date'] = pd.to_datetime(DF['condition_start_date'], dayfirst=True)

    # Extract the year from the 'condition_start_date' column
    DF['Year'] = DF['condition_start_date'].dt.year

    # Group by year and count the number of cases
    fechasYear = DF.groupby(DF['Year']).size()

    # Create a bar chart using Plotly
    fig = go.Figure()

    # Add bar trace to the figure
    fig.add_trace(go.Bar(
        x=fechasYear.index,   # X-axis: Years
        y=fechasYear.values,  # Y-axis: Number of cases
        text=fechasYear.values,  # Text labels on top of bars
        textposition='outside',  # Show labels outside bars
        marker_color='blue',   # Color of the bars
    ))

    # Update layout for the figure
    fig.update_layout(
        title="Timeline of condition_start_date",
        xaxis_title="Year",
        yaxis_title="Number of Cases",
        xaxis_tickformat='%Y',  # Format x-axis for years
        xaxis=dict(
            tickmode='array',
            tickvals=fechasYear.index,  # Ensure all years are shown as ticks
            ticktext=[f'{year}\nYear' for year in fechasYear.index],  # Custom tick labels with "Year"
            tickangle=-45,  # Rotate the labels to match the matplotlib version
        ),
        height=600,  # Adjust the figure height
        margin=dict(l=50, r=50, t=100, b=50),  # Margins to make room for labels
        template='plotly_white',  # Clean template
    )

    # Show the interactive plot
    return fig

def zel_data_per_deparments_and_montsh(df, num_deparments):
    # Convert 'INI_SIN' to datetime and extract the month
    df['INI_SIN'] = pd.to_datetime(df['INI_SIN'])
    df['Mes'] = df['INI_SIN'].dt.month

    # Create subplots: 4 rows, 3 columns (12 months)

    fig = make_subplots(
        rows=4, cols=3, 
        subplot_titles=[calendar.month_name[mes] for mes in range(1, 13)],  # Add month names as titles
        vertical_spacing=0.1,  # Adjust spacing between rows
        horizontal_spacing=0.09  # Adjust spacing between columns
    )

    # Iterate over the months to create each subplot
    for i, mes in enumerate(range(1, 13)):
        # Filter data for the current month
        df_mes = df[df['Mes'] == mes]
        department_counts = df_mes['Departamento_ocurrencia'].value_counts().reset_index()

        department_counts.columns = ['Departamento', 'Frecuencia']
        
        # Create the bar plot using Plotly
        department_counts = department_counts.iloc[:num_deparments, :]

        # Get row and column for the current subplot
        row = (i // 3) + 1
        col = (i % 3) + 1

        # Add bar chart for the current month
        fig.add_trace(
            go.Bar(
                x=department_counts['Departamento'], 
                y=department_counts['Frecuencia'], 
                name=calendar.month_name[mes]
            ),
            row=row, col=col
        )

        # Update layout for each subplot (rotate x-axis labels)
        fig.update_xaxes(tickangle=45, tickmode='array', row=row, col=col)
        fig.update_yaxes(title_text="Número de casos", row=row, col=col)

    # Update layout for the entire figure
    fig.update_layout(
        height=1200,  # Adjust the height to fit the 12 subplots
        title="Número de casos por Departamento para cada mes",
        showlegend=False,  # Hide legend as month names are shown as titles
        template="plotly_white"
    )

    return fig


def load_netcdf_file(f_path):
        data = Dataset(f_path, mode='r') # read the data
        x = data["X"][:]
        y = data["Y"][:]
        time = data["T"][:]
        pre = data["precipitation"][:]
        return x, y, time, pre

#def zel_create_precipitation_map(netcdf_file_path):
#    x, y, _, pre = load_netcdf_file(netcdf_file_path)
#    title = u"Average daily surface precipitation in 2023 "
#    # Create a meshgrid for the coordinates (similar to the Basemap approach)
#    lon, lat = np.meshgrid(x,y)  #this converts coordinates into 2D arrray
#    mp = Basemap(projection='merc',
#             llcrnrlon=min(x),   # lower longitude
#             llcrnrlat=min(y),    # lower latitude
#             urcrnrlon=max(x),   # uppper longitude
#             urcrnrlat=max(y),   # uppper latitude
#            resolution = 'i')
#    x,y = mp(lon,lat) #mapping them together
#    c_scheme = mp.pcolor(x,y,np.squeeze(pre[0,:,:])) # [0,:,:] is for the first day of the year
#
#    # consider this as the outline for the map that is to be created
#    mp.drawcoastlines()
#    mp.drawstates()
#    mp.drawcountries()
#
#    cbar = mp.colorbar(c_scheme,location='right',pad = '10%') # map information
#    # Create a scattergeo plot
#    return fig



def zel_create_dengue_choropleth_map(df, column_name='Departamento_ocurrencia'):
    # Load the GeoJSON data for Colombia
    with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json') as response:
        geojson_data = json.load(response)

    # Calculate dengue density per department
    densidadDengue = df.groupby(column_name)['Nombre_evento'].apply(lambda x: (x == 'DENGUE').sum()).reset_index()
    densidadDengue.columns = ['Departamento', 'Dengue Cases']

    # Population data for each department
    densidadDengue['Poblacion']= [
        81000, 6680000, 269000, 2580000, 2200000, 1250000, 1000000, 405000, 428000, 
        1400000, 1180000, 550000, 1800000, 3000000, 100000, 45000, 890000, 85000, 
        1280000, 1350000, 1130000, 1900000, 1460000, 350000, 545000, 980000, 62000, 
        2300000, 915000, 1440000, 4700000, 41000, 110000
    ]

    # Calculate incidence per 100,000 people
    densidadDengue['Incidencia'] = (densidadDengue['Dengue Cases'] / densidadDengue['Poblacion']) * 100000

    # Calculate severe dengue density per department
    densidadGrave = df.groupby(column_name)['Nombre_evento'].apply(lambda x: (x == 'DENGUE GRAVE').sum()).reset_index()
    densidadGrave.columns = ['Departamento', 'Severe Dengue Cases']

    # Additional population-based calculations
    densidadDengue['PoblacionSinDengue'] = densidadDengue['Poblacion'] - densidadDengue['Dengue Cases']
    densidadDengue['IncidenciaNE'] = (densidadDengue['PoblacionSinDengue'] / densidadDengue['Poblacion']) * 100000
    densidadDengue['REM'] = (densidadDengue['Incidencia'] / densidadDengue['IncidenciaNE']) * 10000

    # Merge the severe dengue cases into the main dataframe
    datosDensidad = pd.merge(densidadDengue, densidadGrave, on='Departamento')

    # Fix department name inconsistencies for matching with GeoJSON
    datosDensidad.loc[datosDensidad['Departamento'] == "VALLE", 'Departamento'] = "VALLE DEL CAUCA"
    datosDensidad.loc[datosDensidad['Departamento'] == "SAN ANDRES", 'Departamento'] = "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA"
    datosDensidad.loc[datosDensidad['Departamento'] == "BOGOTA", 'Departamento'] = "SANTAFE DE BOGOTA D.C"
    datosDensidad.loc[datosDensidad['Departamento'] == "GUAJIRA", 'Departamento'] = "LA GUAJIRA"
    datosDensidad.loc[datosDensidad['Departamento'] == "NORTE SANTANDER", 'Departamento'] = "NORTE DE SANTANDER"

    # Set the 'id' field in the GeoJSON to match department names
    for feature in geojson_data['features']:
        feature['id'] = feature['properties']['NOMBRE_DPT']

    # Create the choropleth map figure
    fig = go.Figure()

    # Add the trace for dengue cases
    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=datosDensidad['Departamento'],
        z=datosDensidad['Dengue Cases'],
        colorscale='Viridis',
        colorbar_title="Dengue Cases",
        visible=True,
        featureidkey="properties.NOMBRE_DPT"
    ))

    # Add the trace for incidence
    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=datosDensidad['Departamento'],
        z=datosDensidad['Incidencia'],
        colorscale='Viridis',
        colorbar_title="Incidencia (100k Personas)",
        visible=False,  # Initially hidden
        featureidkey="properties.NOMBRE_DPT"
    ))

    # Add the trace for incidence NE
    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=datosDensidad['Departamento'],
        z=datosDensidad['IncidenciaNE'],
        colorscale='redor',
        colorbar_title="Incidencia No Expuestos",
        visible=False,  # Initially hidden
        featureidkey="properties.NOMBRE_DPT"
    ))

    # Add the trace for REM
    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=datosDensidad['Departamento'],
        z=datosDensidad['REM'],
        colorscale='redor',
        colorbar_title="REM",
        visible=False,  # Initially hidden
        featureidkey="properties.NOMBRE_DPT"
    ))

    # Update layout for interactivity
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=2,
        mapbox_center={"lat": 4.5709, "lon": -74.2973},
        title=dict(
            text="Casos de Dengue en Colombia - 2023",
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=18)
        ),
        annotations=[
            dict(
                x=0.5, y=-0.1, xref='paper', yref='paper',
                text='Nota: Bogotá es la única entidad sin población en riesgo.',
                showarrow=False, font=dict(size=12)
            )
        ],
        updatemenus=[
            dict(
                type="buttons",
                direction="down",
                buttons=list([
                    dict(
                        args=[{"visible": [True, False, False, False]}],
                        label="Casos de Dengue",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [False, True, False, False]}],
                        label="Incidencia",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [False, False, True, False]}],
                        label="Incidencia NE",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [False, False, False, True]}],
                        label="REM",
                        method="update"
                    )
                ])
            )
        ]
    )

    return fig

def zel_pie_hist_departments(df, column_name='Departamento_ocurrencia', bins=32):
    # Count the occurrences of each department
    department_counts = df[column_name].value_counts().reset_index()
    department_counts.columns = ['Departamento', 'Frecuencia']
    
    # Create the bar plot using Plotly
    department_counts = department_counts.iloc[:bins, :]
    
    # Create subplots: 1 row, 2 columns
    fig = make_subplots(rows=2,
                        cols=1,
                        subplot_titles=("Histograma Departments vs Cases", "Pie Plot Cases percentage"),
                        specs=[[{"type": "xy"}],[{"type": "domain"}]])

    fig.add_trace(go.Bar(
        x=department_counts['Departamento'], 
        y=department_counts['Frecuencia'], 
        name='Bar Plot', 
        marker_color='#4682B4'
    ), row=1, col=1)
    
    fig.add_trace(go.Pie(
        labels=department_counts['Departamento'], 
        values=department_counts['Frecuencia'], 
        name='Pie Chart',
    ), row=2, col=2)

    # Update layout
    fig.update_layout(
        title_text="Analisis de casos por departamento",
        showlegend=False,  # Hide legend since it's repetitive across subplots
        height=400,
        template="plotly_white"
    )

    # Show the plot
    return fig

def zel_hist_estratos_vs_cases(df, col):
    # Clean the 'estrato' column by stripping whitespace and filtering out empty strings
    df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    filtered_df = df[df[col] != ""]

    # Group the data by 'estrato' and count the occurrences
    estratos = filtered_df.groupby(col).size().reset_index(name='count')

    # Create a bar chart with Plotly
    fig = px.bar(estratos, x=col, y='count', labels={col: 'Estratos', 'count': 'Frecuencia'}, color_discrete_sequence=['#4682B4'])

    # Update the layout with title and axis labels
    fig.update_layout(
        title="Histograma de los Estratos",
        xaxis_title="Estratos",
        yaxis_title="Frecuencia",
        xaxis=dict(
            tickvals=[1, 2, 3, 4, 5, 6],  # Set the custom tick values to [1, 2, 3, 4, 5, 6]
            ticktext=[1, 2, 3, 4, 5, 6]   # Ensure correct labels appear
        ),
        template='plotly_white'
    )

    # Show the interactive plot
    return fig

def load_file(filename, sep=","):
    df = pd.read_csv(filename, sep=sep)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

def zel_hist_months_vs_cases(df, col):
    # Ensure the date column is in datetime format
    df[col] = pd.to_datetime(df[col])

    # Group the data by month
    fechasMes = df.groupby(df[col].dt.month).size()

    # Get the month names
    month_names = [calendar.month_name[i] for i in range(1, 13)]

    # Create a new DataFrame for Plotly
    plot_df = pd.DataFrame({
        'Month': month_names[:len(fechasMes)],  # Limit the months to the available data
        'Cases': fechasMes.values
    })

    # Create the bar chart with Plotly
    fig = px.bar(plot_df, x='Month', y='Cases', title='CASOS EN EL 2023', labels={'Month': 'Meses', 'Cases': 'Cantidad de casos por mes'})

    # Update the layout for better appearance
    fig.update_layout(
        xaxis_title='Meses',
        yaxis_title='Cantidad de casos por mes',
        xaxis_tickangle=-45,  # Rotate x-axis labels
        template='plotly_white',  # Set a clean template
        height=600,  # Set the figure size
    )
    return fig

def zel_pie_analysis_lab(df):
    # Calculate the percentages
    case_counts = df['nom_est_f_caso'].value_counts()
    PerConfs = case_counts['Confirmado por laboratorio'] / len(df) * 100
    PerNexos = case_counts['Confirmado por Nexo Epidemiológico'] / len(df) * 100
    PerProbs = case_counts['Probable'] / len(df) * 100

    # Data for the pie chart
    Per = [PerConfs, PerNexos, PerProbs]
    labels = ['Confirmado por laboratorio', 'Confirmado por Nexo Epidemiológico', 'Probable']

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=Per, hoverinfo='label+percent', textinfo='percent', textfont_size=15)])

    # Customize the layout
    fig.update_layout(
        title_text="Distribución de Casos",
        template="plotly_white"
    )
    return fig

def zel_box_plot_analysis(df, col):
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