import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import plotly.express as px


def main():
    st.set_page_config(
        page_title="Gun Violence Facing Our Youth", page_icon="chart_with_upwards_trend", layout="wide"
    )

    st.title("Gun Violence Facing Our Youth")
    st.markdown("Gun violence is a pertinent issue in today’s America. The use of firearms to commit horrific acts of violence has left devastating impacts on individuals, families, and communities. The prevalence of mass shootings in America has become so extreme that they often just blend into the background of daily news headlines. The regularity of mass shootings also underscores the need to understand and address the root causes of this violence, including access to firearms, mental health, and societal factors such as income inequality and social isolations. This data journalism article presents a narrative, accompanied by visualizations, to highlight these issues.")

    col1, col2 = st.columns([0.6, 1.2])

    with col1:
        st.header("Gun Incidents in the United States (2013 - 2018)")
        st.markdown("Map of the U.S. showing all gun related incidents in the years 2013-2018. The data was sourced from Kaggle and downloaded from the Gun Violence Archive. The dataset contains almost 240,000 gun-related incidents that are displayed on the map. It is clear that this has been a major issue in this country for quite some time.")

    with col2:
        html_temp = """<div class='tableauPlaceholder' id='viz1681572080122' style='position: relative'><noscript><a href='#'>
            <img alt='Gun Incidents in the United States 2013 - 2018 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Gu&#47;GunViolenceintheU_S__16815277936410&#47;Map&#47;1_rss.png' style='border: none' /></a></noscript>
            <object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
            <param name='embed_code_version' value='3' /> <param name='site_root' value='' />
            <param name='name' value='GunViolenceintheU_S__16815277936410&#47;Map' /><param name='tabs' value='no' />
            <param name='toolbar' value='yes' />
            <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Gu&#47;GunViolenceintheU_S__16815277936410&#47;Map&#47;1.png' /> 
            <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' />
            <param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object>
        </div>                
        <script type='text/javascript'>                    
            var divElement = document.getElementById('viz1681572080122');                    
            var vizElement = divElement.getElementsByTagName('object')[0];                    
            vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    
            var scriptElement = document.createElement('script');                    
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
            vizElement.parentNode.insertBefore(scriptElement, vizElement);                
        </script>"""
        components.html(html_temp, width=900, height=800)

    df = pd.read_csv("Death-all1.csv")

    df['Year'] = df['Year'].astype('int64')
    domain_col = [
            "Firearm",
            "Motor Vehicle Traffic",
            "Drowning",
            "Fall",
            "Fire/Flame",
            "Other Pedestrian",
            "Other land transport",
            "Other specified, classifiable Injury",
            "Poisoning",
            "Suffocation",
            "Unspecified Injury",
        ]
    range_col = [
            "red",
            "lightgreen",
            "darkblue",
            "orange",
            "pink",
            "yellow",
            "purple",
            "lightblue",
            "brown",
            "grey",
            "lightgreen",
        ]
    line_chart = (
            alt.Chart(df, title="Leading causes of death in adolescents")
            .mark_line(point=True)
            .encode(
                x=alt.X("Year:O", title="Year"),
                y=alt.Y("Percentage", title="Percentage of all types"),
                color=alt.Color(
                    "Injury Mechanism:N",
                    scale=alt.Scale(domain=domain_col, range=range_col),
                ),
                tooltip=["Percentage", "Injury Mechanism"],
            )
            .properties(
                width=800,
                height=500,
            )
    ).configure(background='#D9E9F0')

    df_countries = pd.read_csv("clean_firearm_deaths_country.csv")
    countries = [
        "Canada",
        "Australia",
        "United Kingdom",
        "Germany",
        "France",
        "Japan",
        "South Korea",
        "Netherlands",
        "Sweden",
        "Switzerland",
        "Norway",
        "Denmark",
        "Finland",
        "Austria",
        "United States of America",
    ]
    df_countries = df_countries[df_countries.location.isin(countries)]
    df_countries.sort_values(by="rate", inplace=True)
    fig = px.bar(
        df_countries,
        x="rate",
        y="location",
        labels={"rate": "Rate of Adolescent Firearm Deaths", "location": "Country"},
        title="Rate of Adolescent Firearm Deaths (self-harm, physical violence, unintentional) by Country",
    )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        }
    )

    df_us_deaths = pd.read_csv("deaths_by_cause.csv")
    causes_to_exclude = [
        "Other specified, classifiable Injury",
        "Other specified, not elsewhere classified Injury",
        "Unspecified Injury",
        "Non-Injury: Other complications of pregnancy, childbirth and the puerperium",
        "Non-Injury: Complications of medical and surgical care",
        "Other transport",
        "Other land transport",
        "Other Pedal cyclist",
        "Other Pedestrian",
        "Struck by or against",
    ]
    df_us_deaths = df_us_deaths[
        ~df_us_deaths["Injury Mechanism"].isin(causes_to_exclude)
    ]
    df_us_deaths = df_us_deaths.astype({"Deaths": int, "Crude Rate": float})
    df_us_deaths.sort_values(by="Years", inplace=True)

    c, d = st.columns([0.6, 1.2])


    with c:
        st.header("Leading Cause of Death in Adolescents")
        st.markdown("This visualization was constructed using data provided by the CDC, through WONDER, a system meant to disseminate government public health data and information. Data exploration was done on all of the data provided by the CDC, before narrowing down the causes to the top 10-15 leading causes of death that were also relevant to the narrative of our visualization. After this, a scatter plot was created with a line connecting each scatter plot in order to show that while motor vehicle deaths used to be the leading cause of deaths for adolescents, measures have clearly been taken to reduce the number of deaths attributed to this cause, while firearm death clearly continues to only rise, overtaking motor vehicle deaths as the number one cause.")
    with d:
        st.altair_chart(line_chart, use_container_width=True)

    e, f = st.columns([0.6, 1.2])

    with e:
        st.header("Adolescent Firearm Deaths by Country")
        st.markdown("This visualization was constructed using data provided by IHME. The original data consisted of around 50 different countries. Through data exploration and research, the top 9 countries that are comparable to the United States in terms of economic and socio-cultural aspects were the only countries left to be included in the final visualization so that it was more readable and the data presented was more realistic. Ultimately, we ended up portraying the US outpacing other economically/socially comparable countries in the number of self-harm, intentional, and accidental adolescent firearm deaths.")
    with f:
        st.plotly_chart(fig, use_container_width=True)

    # tab1, tab2 = st.tabs(
    #     [
    #         "Leading Cause of Death in Adolescents",
    #         "Adolescent Firearm Deaths by Country",
    #     ]
    # )

    # with tab1:
    #     st.altair_chart(line_chart, use_container_width=True)
    # with tab2:
    #     st.plotly_chart(fig, use_container_width=True)

    a, b = st.columns([0.6, 1.2])

    with a:
        st.header("Fatal Gun Incidents on US School Campus (2000 - 2023)")
        st.markdown("This visualization was created using data provided by the CHDS. Instead of using data as a chart/table, an animation is made to embed both the number of casualties and description of the incidents to show how these numbers are kids’ lives by illustrating them in a classroom setting. The animation is made by Javascript. And the duration of each incident will be shorter and shorter to remind us how urgent the fatal gun incidents are happening among US school campuses.")
    with b:
        classroom_simulation = open("classroom_simulation.html", "r", encoding="utf-8")
        source_code = classroom_simulation.read()
        components.html(source_code, width=900, height=700)

    # st.header("School Shooting Incidents")
    # st.markdown("These three visualizations highlight school shooting incidents in the United States.")

    g, h = st.columns([0.6, 1.2])
    i, j = st.columns([0.6, 1.2])
    k, l = st.columns([0.6, 1.2])

    with g:
        st.header("School Shooting Incidents by Year (1970 - 2022)")
        st.markdown("This visualization was created using data provided by the CHDS. Prior knowledge surrounding school shootings suggested that there might be a sharp increase in incidents in recent years. To investigate this prior belief, scatter plots of the number of incidents vs. the year were plotted. Initially, the scatter plots created were just used to visualize the trend expected (which turned out to be reality). The scatter plot was then turned into a scatter + line plot to show increases/decreases more effectively. A red color encoding was used to remind the user that these incidents often resulted in death or injury. Tooltips were added to grant users more information if wanted. Lastly, animation was added to add emphasis to the alarming spike in school shootings from the past 5 years.")
    with h:
        incidents_per_year = open("incidents_per_year.html", "r", encoding="utf-8")
        source_code = incidents_per_year.read()
        components.html(source_code, width=900, height=500)
    
    with i:
        st.header("School Shootings this Century")
        st.markdown("This visualization was created using data scraped from Wikipedia. This plot combines deaths and injuries to visualize the magnitude of different school shootings. It’s animated temporarily to give the user a ‘real time’ feel of these events occurring. A death and injury counter was added to the top left of the chart to display the overall impact school shootings had this century. Tooltips are included which gives the user more details about a specific incident (summary, location, etc.). Each incident is colored red to fit with the theme of gun violence.")
    with j:
        incidents = open("incidents.html", "r", encoding="utf-8")
        source_code = incidents.read()
        components.html(source_code, width=900, height=500)
    
    with k:
        st.header("Fatalities in School Shootings (1970 - 2022)")
        st.markdown("This visualization was created using data provided by the CHDS. Instead of visualizing the number of deaths as a simple line chart, we decided to switch to a stacked bar chart where the area of each rectangle corresponds to the number of fatalities for one specific incident. Initially, the bar chart was monochromatic and unsorted. Incidents with a large number of fatalities were moved to the top and colored red to stand out. The incident at Sandy Hook Elementary School has its own annotation since it was one of the first mass school shootings which resulted in a large number of deaths. Tooltips were added to specify specific schools and fatality counts.")
    with l:
        incidents_binned = open("incidents_binned.html", "r", encoding="utf-8")
        source_code = incidents_binned.read()
        components.html(source_code, width=900, height=500)

    # inc_tab1, inc_tab2, inc_tab3 = st.tabs(
    #     [
    #         "School Shooting Incidents by Year (1990-2022)",
    #         "School Shootings this Century",
    #         "School Shooting Incidents",
    #     ]
    # )

    # with inc_tab1:
    #     incidents_per_year = open("incidents_per_year.html", "r", encoding="utf-8")
    #     source_code = incidents_per_year.read()
    #     components.html(source_code, width=1200, height=500)
    # with inc_tab2:
    #     incidents = open("incidents.html", "r", encoding="utf-8")
    #     source_code = incidents.read()
    #     components.html(source_code, width=1200, height=500)
    # with inc_tab3:
    #     incidents_binned = open("incidents_binned.html", "r", encoding="utf-8")
    #     source_code = incidents_binned.read()
    #     components.html(source_code, width=1200, height=500)


if __name__ == "__main__":
    main()
