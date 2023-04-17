import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import plotly.express as px

def main():
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
    components.html(html_temp, width=900, height=700)

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

    st.altair_chart(line_chart)

    countries_chart = Image.open('countries.png')
    st.image(countries_chart, caption='Rate of Adolescent Firearm Deaths by Country')
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
    df_countries.sort_values(by="rate", ascending=False, inplace=True)
    fig = px.bar(
        df_countries,
        x="rate",
        y="location",
        labels={"rate": "Rate of Adolescent Firearm Deaths", "location": "country"},
        title="Rate of Adolescent Firearm Deaths (self-harm, physical violence, unintentional) by Country",
    )
    fig

    df1901 = pd.read_csv("1999-2001.txt", sep="\t")
    df1901["Years"] = "1999-2001"
    df0205 = pd.read_csv("2002-2005.txt", sep="\t")
    df0205["Years"] = "2002-2005"
    df0609 = pd.read_csv("2006-2009.txt", sep="\t")
    df0609["Years"] = "2006-2009"
    df1013 = pd.read_csv("2010-2013.txt", sep="\t")
    df1013["Years"] = "2010-2013"
    df1417 = pd.read_csv("2014-2017.txt", sep="\t")
    df1417["Years"] = "2014-2017"
    df1821 = pd.read_csv("2018-2021.txt", sep="\t")
    df1821["Years"] = "2018-2021"

    finaldf = pd.concat([df1901, df0205, df0609, df1013, df1417, df1821], axis=0)
    finaldf.drop(columns="Injury Mechanism Code", inplace=True)
    finaldf.to_csv("deaths_by_cause.csv", index=False)
    df_firearm = pd.read_csv("raw_deaths_by_firearm_country.csv")
    df_firearm.drop(columns=["measure", "sex", "age"], inplace=True)
    df_firearm = df_firearm[df_firearm.metric == "Rate"]
    df_firearm.drop(columns=["metric"], inplace=True)
    print(df_firearm.location.unique())
    # df_firearm.to_csv("clean_firearm_deaths_country.csv", index=False)

    df_us_deaths = pd.read_csv("deaths_by_cause.csv")
    df_us_deaths = df_us_deaths.astype({"Deaths": int, "Crude Rate": float})
    deaths_fig = px.line(df_us_deaths, x="Years", y="Crude Rate", color="Injury Mechanism")
    deaths_fig

if __name__ == "__main__":    
    main()