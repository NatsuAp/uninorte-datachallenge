import streamlit as st
from datetime import datetime
from src.data import mapping, CLIMATE_COL
from src.utils import (load_file,
                       zel_hist_months_vs_cases,
                       zel_pie_analysis_lab,
                       zel_box_plot_analysis,
                       zel_hist_estratos_vs_cases,
                       zel_pie_hist_departments,
                       zel_create_dengue_choropleth_map,
                       zel_data_per_deparments_and_montsh,
                       zel_plot_timeline_condition_start_date_plotly,
                       zel_plot_boxplot_edad_plotly,
                       zel_plot_scatter_age_vs_hospital_days,
                       zel_plot_city_histogram_plotly)
                       # zel_create_precipitation_map)

def zelaya_analysis():
    import streamlit as st
    st.header("EDA Dengue")
    data_selection = st.selectbox(label="Select Data to Analyze", options=mapping.keys())
    data_path = mapping[data_selection]
    if data_selection == "barranquilla":
        data = load_file(data_path, sep=";")
        st.table(data.head(2))
        st.write("Dengue en Barranquilla")

        if st.checkbox(label="Linea de Tiempo cuando la condición comenzó"):
            st.session_state["zel_plot_timeline_condition_start_date_plotly"] = zel_plot_timeline_condition_start_date_plotly(data)
        else:
            st.session_state["zel_plot_timeline_condition_start_date_plotly"] = None

        if st.session_state.get("zel_plot_timeline_condition_start_date_plotly"):
            st.write("Analisis Timeline condition start date by year")
            st.plotly_chart(st.session_state.get("zel_plot_timeline_condition_start_date_plotly"))

        if st.checkbox(label="Distribución de la edad en los casos de Barranquilla"):
            st.session_state["zel_plot_boxplot_edad_plotly"] = zel_plot_boxplot_edad_plotly(data)
        else:
            st.session_state["zel_plot_boxplot_edad_plotly"] = None

        if st.session_state.get("zel_plot_boxplot_edad_plotly"):
            st.write("Analisis BoxPlot de los Edad de los enfermos")
            st.plotly_chart(st.session_state.get("zel_plot_boxplot_edad_plotly"))

        if st.checkbox(label="Analisis Edad y Estadía en el hóspital"):
            st.session_state["zel_plot_scatter_age_vs_hospital_days"] = zel_plot_scatter_age_vs_hospital_days(data)
        else:
            st.session_state["zel_plot_scatter_age_vs_hospital_days"] = None

        if st.session_state.get("zel_plot_scatter_age_vs_hospital_days"):
            st.write("Analisis de relación entre la Edad y qué tan grave dio la enfermedad")
            st.plotly_chart(st.session_state.get("zel_plot_scatter_age_vs_hospital_days"))

        if st.checkbox(label="Analisis De ciudad o municipio de origen de los enfermos"):
            st.session_state["zel_plot_city_histogram_plotly"] = True
            
        else:
            st.session_state["zel_plot_city_histogram_plotly"] = None

        if st.session_state.get("zel_plot_city_histogram_plotly"):
            st.write("Analisis de relación entre la enfermedad y el municipio de origen")
            num_dep_selected = st.number_input(label="#Municipios/Ciudades", min_value=1, max_value=22, value=5)
            st.write(f"Mostrando análisis para los {num_dep_selected} municipios/ciudades con más casos de dengue.")
            st.plotly_chart(zel_plot_city_histogram_plotly(data, num_dep_selected))

    elif data_selection == "colombia":
        data = load_file(data_path, sep=",")
        st.table(data.head(2))
        st.write("Dengue en Colombia 2023")

        if st.checkbox(label="histograma meses vs casos"):
            st.session_state["zel_hist_months_vs_cases"] = zel_hist_months_vs_cases(data, "INI_SIN")
        else:
            st.session_state["zel_hist_months_vs_cases"] = None

        if st.session_state.get("zel_hist_months_vs_cases"):
            st.write("Analisis meses vs casos de dengue")
            st.plotly_chart(st.session_state.get("zel_hist_months_vs_cases"))

        if st.checkbox(label="Pie Laboratorio Analisis"):
            st.session_state["zel_pie_analysis_lab"] = zel_pie_analysis_lab(data)
        else:
            st.session_state["zel_pie_analysis_lab"] = None
        
        if st.session_state.get("zel_pie_analysis_lab"):
            st.write("Analisis resultados: Confirmado por laboratorio, Confirmado por Nexo Epidemiológico, Probable")
            st.plotly_chart(st.session_state.get("zel_pie_analysis_lab"))

        if st.checkbox(label="Analisis de la Edad"):
            st.session_state["zel_box_plot_analysis"] = zel_box_plot_analysis(data, "EDAD")
        else:
            st.session_state["zel_box_plot_analysis"] = None

        if st.session_state.get("zel_box_plot_analysis"):
            st.write("Analisis de la Edad de los afectados")
            st.plotly_chart(st.session_state.get("zel_box_plot_analysis"))

        if st.checkbox(label="Analisis del Estrato"):
            st.session_state["zel_hist_estratos_vs_cases"] = zel_hist_estratos_vs_cases(data, "estrato")
        else:
            st.session_state["zel_hist_estratos_vs_cases"] = None

        if st.session_state.get("zel_hist_estratos_vs_cases"):
            st.write("Analisis de la relación entre el Estrato y afectados")
            st.plotly_chart(st.session_state.get("zel_hist_estratos_vs_cases"))

        if st.checkbox(label="Analisis de casos por departamento"):
            st.session_state["zel_hist_departments"] = True
        else:
            st.session_state["zel_hist_departments"] = None

        if st.session_state.get("zel_hist_departments"):
            st.write("Analisis de casos de dengue por cada departamento")
            num_dep_selected = st.number_input(label="#Departamentos", min_value=5, max_value=40, value=10)
            st.write(f"Mostrando análisis para los {num_dep_selected} departamentos con más casos de dengue.")
            st.plotly_chart(zel_pie_hist_departments(data, "Departamento_ocurrencia", bins=num_dep_selected))

        if st.checkbox(label="Analisis de casos por departamento y por mes"):
            st.session_state["zel_data_per_deparments_and_montsh"] = True
        else:
            st.session_state["zel_data_per_deparments_and_montsh"] = None

        if st.session_state.get("zel_data_per_deparments_and_montsh"):
            st.write("Analisis de casos por departamento y por mes")
            num_dep_selected = st.number_input(label="#Departamentos", min_value=5, max_value=40, value=10)
            st.write(f"Mostrando análisis para los {num_dep_selected} departamentos con más casos de dengue por cada mes.")
            st.plotly_chart(zel_data_per_deparments_and_montsh(data, num_dep_selected))

        st.header("Visualización Mapa")
        st.plotly_chart(zel_create_dengue_choropleth_map(data, "Departamento_ocurrencia"))
        # st.plotly_chart(zel_create_precipitation_map(CLIMATE_COL))

def villadiego_analysis():
    import streamlit as st
    st.header("EDA Dengue")

#def all_join_analysis():
#    import streamlit as st
#    import pandas_profiling
#
#    from streamlit_pandas_profiling import st_profile_report
#
#    st.header("EDA Dengue")
#    data_selection = st.selectbox(label="Select Data to Analyze", options=mapping.keys())
#    data_path = mapping[data_selection]
#    if data_selection == "barranquilla":
#        data = load_file(data_path, sep=";")
#        pass
#    elif data_selection == "colombia":
#        data = load_file(data_path, sep=",")
#        st.table(data.head(2))
#        pr = data.profile_report()
#        st_profile_report(pr)

page_names_to_funcs = {
    "Zelaya interactive visualization": zelaya_analysis,
    "Villadiego interactive visualization": villadiego_analysis,
    #"Pandas Profile Report": all_join_analysis
}

demo_name = st.sidebar.selectbox("Choose Interactice Visualization To Review", page_names_to_funcs.keys())

page_names_to_funcs[demo_name]()