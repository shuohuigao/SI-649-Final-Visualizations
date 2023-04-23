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
    g, h = st.columns([0.6, 1.2])

    with g:
        st.header("Schools have become a common site for gun violence")
        st.markdown("School shootings have become all too common tragedies in the United States. The number of school shootings in this country have increased exponentially in the last 20 years. Parents should not have to live in fear when they send their children off to school. This is an urgent issue that needs action.")
    with h:
        incidents_per_year = open("incidents_per_year.html", "r", encoding="utf-8")
        source_code = incidents_per_year.read()
        components.html(source_code, width=900, height=500)

        incidents = open("incidents.html", "r", encoding="utf-8")
        source_code = incidents.read()
        components.html(source_code, width=900, height=500)

        incidents_binned = open("incidents_binned.html", "r", encoding="utf-8")
        source_code = incidents_binned.read()
        st.components.v1.html(source_code, width=900, height=500, scrolling=True)

        classroom_simulation = open("classroom_simulation.html", "r", encoding="utf-8")
        source_code = classroom_simulation.read()
        components.html(source_code, width=900, height=700)

    df = pd.read_csv("Death-all1.csv")

    df['Year'] = df['Year'].astype('int64')
    df['Percentage'] = df['Percentage'].round(3)
    df['Percentage'] = df['Percentage']*100
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
            ).properties(
                width=800,
                height=500,
            ).configure(
                background='#FFFFFF'
            ).configure_title(
                color='black'
            ).configure_axis(
                labelColor='black',
                titleColor='black',
                gridColor='lightgray',
            ).configure_legend(
                labelColor='black',
                titleColor='black'
            )
    )

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
    df_countries.replace({'United States of America': 'USA'}, regex=True, inplace=True)
    df_countries['rate'] = df_countries['rate'].round(3)
    fig = (
            alt.Chart(df_countries, 
                      title="Percent of Adolescents Dying due to Firearms (self-harm, physical violence, unintentional) by Country for 2019")
            .mark_bar()
            .encode(
                x=alt.X("sum(rate)", title="Percent of Adolescents Dying due to Firearms"),
                y=alt.Y("location", title="Country",sort='-x'),
                tooltip=["rate", "location"],
            ).transform_filter(
                (alt.datum.year == 2019)
            ).configure(
                background='#FFFFFF'
            ).configure_title(
                color='black'
            ).configure_axis(
                labelColor='black',
                titleColor='black',
                gridColor='lightgray',
            ).configure_legend(
                labelColor='black',
                titleColor='black'
            )
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
        st.header("Firearms have become the leading cause of death in adolescents")
        st.markdown("Gun violence has now become the leading cause of death for adolescents in the United States, now ahead of motor vehicle accidents.")
    with d:
        st.altair_chart(line_chart, use_container_width=True)

    e, f = st.columns([0.6, 1.2])

    with e:
        st.header("A uniquely American problem")
        st.markdown("The rate of adolescent firearm deaths in the United States is higher than any other country in the world by at least 6 times.")
    with f:
        st.altair_chart(fig, use_container_width=True)

    col1, col2 = st.columns([0.6, 1.2])

    with col1:
        st.header("Not just affecting the youth")
        st.markdown("Gun violence is a nationwide epidemic that is not just impacting the youth of this country. Gun incidents are a daily occurence. This map shows over 240,000 incidents between the years 2013 and 2018.")

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
        components.html(html_temp, width=900, height=600)
    
    st.header("Action must be taken")
    st.markdown("Gun violence is one of the most pressing issues in this country and it shows no signs of slowing down. Whether it is through gun legislation, community outreach, increased mental health resources, or any other potential solution, we can no longer stand by and do nothing. Action needs to be taken so that we can secure a safer future for our children.")

if __name__ == "__main__":
    main()
