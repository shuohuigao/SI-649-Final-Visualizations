import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import plotly.express as px

def main():
    st.set_page_config(page_title="Gun Violence Dashboard", page_icon=":guardsman:", layout="wide")

    st.title("Gun Violence Dashboard")

    st.header("Gun Incidents in the United States (2013 - 2018)")
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
    components.html(html_temp, width=1000, height=700)

    st.header("Leading causes of death")

    df = pd.read_csv('Death-all1.csv')

    domain_col = ['Firearm', 'Motor Vehicle Traffic', 'Drowning', 'Fall', 'Fire/Flame',  'Other Pedestrian', 'Other land transport', 'Other specified, classifiable Injury','Poisoning', 'Suffocation', 'Unspecified Injury']
    range_col = ['red', 'lightgreen', 'darkblue', 'orange', 'pink', 'yellow', 'purple', 'lightblue', 'brown', 'grey', 'lightgreen' ]
    line_chart = alt.Chart(df, title = 'Leading causes of death in teenagers').mark_line(point = True).encode(
        y = alt.Y('Percentage',title='Percentage of all types'),
        x = alt.Y('Year',title='Year'),
        # color = 'Injury Mechanism',
        color = alt.Color('Injury Mechanism:N',scale=alt.Scale(domain=domain_col, range=range_col)),
        # opacity = alt.Opacity('Injury Mechanism:N',scale=alt.Scale(domain=domain_col, range=range_opa)),
        tooltip= ['Percentage','Injury Mechanism']
    ).properties(
        width=800,
        height=500,
    )

    # st.altair_chart(line_chart)

    image_tab1, image_tab2 = st.tabs(['Rate of Adolescent Firearm Deaths by Country', 'Cause of Death by Injury Mechanism'])

    with image_tab1:
        countries_chart = Image.open('countries.png')
        st.image(countries_chart, caption='Rate of Adolescent Firearm Deaths by Country')
    with image_tab2:
        cod = Image.open('causeofdeath.png')
        st.image(cod, caption='Cause of Death by Injury Mechanism')


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
        labels={"rate": "Rate of Adolescent Firearm Deaths", "location": "country"},
        title="Rate of Adolescent Firearm Deaths (self-harm, physical violence, unintentional) by Country",
    )
    # fig

    # df1901 = pd.read_csv("1999-2001.txt", sep="\t")
    # df1901["Years"] = "1999-2001"
    # df0205 = pd.read_csv("2002-2005.txt", sep="\t")
    # df0205["Years"] = "2002-2005"
    # df0609 = pd.read_csv("2006-2009.txt", sep="\t")
    # df0609["Years"] = "2006-2009"
    # df1013 = pd.read_csv("2010-2013.txt", sep="\t")
    # df1013["Years"] = "2010-2013"
    # df1417 = pd.read_csv("2014-2017.txt", sep="\t")
    # df1417["Years"] = "2014-2017"
    # df1821 = pd.read_csv("2018-2021.txt", sep="\t")
    # df1821["Years"] = "2018-2021"

    # finaldf = pd.concat([df1901, df0205, df0609, df1013, df1417, df1821], axis=0)
    # finaldf.drop(columns="Injury Mechanism Code", inplace=True)
    # finaldf.to_csv("deaths_by_cause.csv", index=False)
    # df_firearm = pd.read_csv("raw_deaths_by_firearm_country.csv")
    # df_firearm.drop(columns=["measure", "sex", "age"], inplace=True)
    # df_firearm = df_firearm[df_firearm.metric == "Rate"]
    # df_firearm.drop(columns=["metric"], inplace=True)
    # print(df_firearm.location.unique())
    # df_firearm.to_csv("clean_firearm_deaths_country.csv", index=False)

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
    # df_us_deaths.sort_values(by="Crude Rate", ascending=False, inplace=True)
    df_us_deaths.sort_values(by="Years", inplace=True)

    crude_fig = px.scatter(
        df_us_deaths,
        x="Years",
        y="Crude Rate",
        color="Injury Mechanism",
        title="Crude Rate of U.S. Adolescent Deaths by Cause (1999-2021)",
    )

    crude_fig.update_traces(mode="lines+markers")
    crude_fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        }
    )
    # crude_fig

    tab1, tab2, tab3 = st.tabs(['Leading Cause of Death in Teenagers', 'Adolescent Firearm Deaths by Country', 'U.S. Adolescent Deaths by Cause'])

    with tab1:
        st.altair_chart(line_chart, use_container_width=True)
    with tab2:
        st.plotly_chart(fig, use_container_width=True)
    with tab3:
        st.plotly_chart(crude_fig, use_container_width=True)

    # df_us_deaths = pd.read_csv("deaths_by_cause.csv")
    # df_us_deaths = df_us_deaths.astype({"Deaths": int, "Crude Rate": float})
    # deaths_fig = px.line(df_us_deaths, x="Years", y="Crude Rate", color="Injury Mechanism")
    # deaths_fig
    st.header("Fatal Gun Incidents on Campus (2000 - 2023)")
    classroom_simulation = open("classroom_simulation.html", 'r', encoding='utf-8')
    source_code = classroom_simulation.read()
    components.html(source_code, width=1000, height=700)

    st.header("School Shooting Incidents")
    inc_tab1, inc_tab2, inc_tab3 = st.tabs(['School Shooting Incidents by Year (1990-2022)', 'School Shootings this Century', 'School Shooting Incidents'])

    with inc_tab1:
        incidents_per_year = open("incidents_per_year.html", 'r', encoding='utf-8')
        source_code = incidents_per_year.read() 
        components.html(source_code, width=1200, height=1200)
    with inc_tab2:
        incidents = open("incidents.html", 'r', encoding='utf-8')
        source_code = incidents.read() 
        components.html(source_code, width=1200, height=1200)
    with inc_tab3:
        incidents_binned = open("incidents_binned.html", 'r', encoding='utf-8')
        source_code = incidents_binned.read() 
        components.html(source_code, width=1200, height=1200)



if __name__ == "__main__":   
    main()
