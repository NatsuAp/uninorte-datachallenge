import streamlit as st
from datetime import datetime
from src.data import mapping, CLIMATE_COL
from src.villa_utils import (
    vill_plot_boxplot_duration_internado_plotly,
    vill_plot_pie_chart_city_distribution,
    vill_plot_age_distribution_by_gender_plotly,
    vill_plot_frequency_of_visits_over_time_plotly,
    vill_plot_dengue_choropleth,
    vill_plot_dengue_density_bar_by_deparment,
    vill_plot_dengue_cases_by_month,
    vill_plot_stacked_dengue_cases,
    vill_plot_dengue_proportion_by_gender,
    vill_plot_dengue_age_comparison,
    vill_plot_dengue_cases_by_estrato,
    vill_plot_age_by_estrato
)
from src.utils import (load_file)

def villadiego_analysis():
    
    st.header("EDA Dengue")
    data_selection = st.selectbox(label="Escoge datos a analizar", options=mapping.keys())
   
    data_path = mapping[data_selection]
    if data_selection == "barranquilla":
        data_path
        data = load_file(data_path, sep=";")
        # st.table(data.head(2))  *Da error al montar en streamlit
        st.write("Dengue en Barranquilla")

        if st.checkbox(label="Analisis duración de internado de casos de dengue"):
            st.session_state["vill_plot_boxplot_duration_internado_plotly"] = vill_plot_boxplot_duration_internado_plotly(data)
        else:
            st.session_state["vill_plot_boxplot_duration_internado_plotly"] = None

        if st.session_state.get("vill_plot_boxplot_duration_internado_plotly"):
            st.write("Analisis duración de internado de casos de dengue")
            st.plotly_chart(st.session_state.get("vill_plot_boxplot_duration_internado_plotly"))

        if st.checkbox(label="Analisis de distribucion de casos de dengue en los municipios"):
            st.session_state["vill_plot_pie_chart_city_distribution"] = vill_plot_pie_chart_city_distribution(data)
        else:
            st.session_state["vill_plot_pie_chart_city_distribution"] = None

        if st.session_state.get("vill_plot_pie_chart_city_distribution"):
            st.write("Analisis de distribucion de casos de dengue en los municipios con más casos")
            st.plotly_chart(st.session_state.get("vill_plot_pie_chart_city_distribution"))

        if st.checkbox(label="Analisis de distribucion de casos de dengue por Sexo"):
            st.session_state["vill_plot_age_distribution_by_gender_plotly"] = vill_plot_age_distribution_by_gender_plotly(data)
        else:
            st.session_state["vill_plot_age_distribution_by_gender_plotly"] = None

        if st.session_state.get("vill_plot_age_distribution_by_gender_plotly"):
            st.write("Analisis de distribucion de casos de dengue por Sexo")
            st.plotly_chart(st.session_state.get("vill_plot_age_distribution_by_gender_plotly"))

        if st.checkbox(label="Analisis de Frecuencia de visitas sobre el tiempo registrado"):
            st.session_state["vill_plot_frequency_of_visits_over_time_plotly"] = vill_plot_frequency_of_visits_over_time_plotly(data)
        else:
            st.session_state["vill_plot_frequency_of_visits_over_time_plotly"] = None

        if st.session_state.get("vill_plot_frequency_of_visits_over_time_plotly"):
            st.write("Analisis de Frecuencia de visitas sobre el tiempo registrado")
            st.plotly_chart(st.session_state.get("vill_plot_frequency_of_visits_over_time_plotly"))

    elif data_selection == "colombia":
        data_path
        data = load_file(data_path, sep=",")
        #st.table(data.head(2)) *Da error al montar en streamlit
        st.write("Dengue en Colombia 2023")

        if st.checkbox(label="Analisis de incidencia Dengue por departamento"):
            st.session_state["vill_plot_dengue_density_bar_by_deparment"] = vill_plot_dengue_density_bar_by_deparment(data)
        else:
            st.session_state["vill_plot_dengue_density_bar_by_deparment"] = None

        if st.session_state.get("vill_plot_dengue_density_bar_by_deparment"):
            st.write("Analisis de incidencia Dengue por departamento")
            st.plotly_chart(st.session_state.get("vill_plot_dengue_density_bar_by_deparment"))
            
        if st.checkbox(label="Analisis de distribución del dengue por Mes"):
            st.session_state["vill_plot_dengue_cases_by_month"] = vill_plot_dengue_cases_by_month(data)
        else:
            st.session_state["vill_plot_dengue_cases_by_month"] = None

        if st.session_state.get("vill_plot_dengue_cases_by_month"):
            st.write("Analisis de distribución del dengue por Mes")
            st.plotly_chart(st.session_state.get("vill_plot_dengue_cases_by_month"))

        if st.checkbox(label="Analisis apilado de dengues y dengues graves por mes"):
            st.session_state["vill_plot_stacked_dengue_cases"] = vill_plot_stacked_dengue_cases(data)
        else:
            st.session_state["vill_plot_stacked_dengue_cases"] = None

        if st.session_state.get("vill_plot_stacked_dengue_cases"):
            st.write("Analisis apilado de dengues y dengues graves por mes")
            st.plotly_chart(st.session_state.get("vill_plot_stacked_dengue_cases"))

        if st.checkbox(label="Analisis Dengue por Sexo (Masculino/Femenino) vs Dengue/Dengue Grave"):
            st.session_state["vill_plot_dengue_proportion_by_gender"] = vill_plot_dengue_proportion_by_gender(data)
        else:
            st.session_state["vill_plot_dengue_proportion_by_gender"] = None

        if st.session_state.get("vill_plot_dengue_proportion_by_gender"):
            st.write("Analisis Dengue por Sexo (Masculino/Femenino) vs Dengue/Dengue Grave")
            st.plotly_chart(st.session_state.get("vill_plot_dengue_proportion_by_gender"))

        if st.checkbox(label="Analisis de Edad vs Tipo de Dengue"):
            st.session_state["vill_plot_dengue_age_comparison"] = vill_plot_dengue_age_comparison(data)
        else:
            st.session_state["vill_plot_dengue_age_comparison"] = None

        if st.session_state.get("vill_plot_dengue_age_comparison"):
            st.write("Analisis de Edad vs Tipo de Dengue")
            st.plotly_chart(st.session_state.get("vill_plot_dengue_age_comparison"))

        if st.checkbox(label="Analisis de casos de dengue por Estrato"):
            st.session_state["vill_plot_dengue_cases_by_estrato"] = vill_plot_dengue_cases_by_estrato(data)
        else:
            st.session_state["vill_plot_dengue_cases_by_estrato"] = None

        if st.session_state.get("vill_plot_dengue_cases_by_estrato"):
            st.write("Analisis de casos de dengue por Estrato usando el siguiente plot")
            st.plotly_chart(st.session_state.get("vill_plot_dengue_cases_by_estrato"))

        if st.checkbox(label="Analisis de Casos y Estratos (1, 2, 3, 4, 5, 6) usando boxplot"):
            st.session_state["vill_plot_age_by_estrato"] = vill_plot_age_by_estrato(data)
        else:
            st.session_state["vill_plot_age_by_estrato"] = None

        if st.session_state.get("vill_plot_age_by_estrato"):
            st.write("Analisis de Casos vs Estratos usando boxplot")
            st.plotly_chart(st.session_state.get("vill_plot_age_by_estrato"))

        st.header("Visualización Mapa")
        st.plotly_chart(vill_plot_dengue_choropleth(data))

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
    "Villadiego interactive visualization": villadiego_analysis,
    #"Pandas Profile Report": all_join_analysis
}

demo_name = st.sidebar.selectbox("Choose Interactice Visualization To Review", page_names_to_funcs.keys())

page_names_to_funcs[demo_name]()