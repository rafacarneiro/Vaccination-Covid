import streamlit as st
import pandas as pd

st.title('COVID DATA VISUALIZATION')
st.markdown('This dataset intend to track COVID-19 vaccination evolution, focused in understanding the situation in Brazil comparing with the other countries')
st.markdown('To compare the situation, in some parts of this dataset, 7 countries were be chosen. They are: Argentina, Brazil, Chile, China, Italy, United Kingdom, United States')
st.markdown('The source of data is https://ourworldindata.org/covid-deaths and they have a lot of more information there.')
st.markdown('Last update: 29/03/2021 ')
df = pd.read_csv('datasets/df_covid.csv')
import datetime
from datetime import timedelta, datetime
df['date'] = pd.to_datetime(df['date'])
df = df[df['location'].map(lambda x:str(x)!="World")]
df = df[df['location'].map(lambda x:str(x)!="South America")]
df = df[df['location'].map(lambda x:str(x)!="Asia")]
df = df[df['location'].map(lambda x:str(x)!="North America")]
df = df[df['location'].map(lambda x:str(x)!="Europe")]
df = df[df['location'].map(lambda x:str(x)!="European Union")]
df = df[df['location'].map(lambda x:str(x)!="Africa")]
print(df.tail(10))
overview = df.groupby(["location", "iso_code"])['population', 'population_density', 'median_age', 'gdp_per_capita',
                                                                      'human_development_index',
                                                                      ].max().reset_index()
overview.head(1)
import seaborn as sns
import plotly.express as px
st.cache(allow_output_mutation=True)
def get_data(path):
    df = pd.read_csv(path)

    return df

path = 'datasets/df_covid.csv'
df = get_data(path)

st.write(df.head(10))

st.title('WORLD OVERVIEW')
st.markdown('WORLD POPULATION ')

top20_population = overview.nlargest(20,'population')
import seaborn as sns
ax = sns.factorplot(x="population", y="location",  data = top20_population , kind="bar",
                    size=10, aspect=1.5, palette='PuBuGn_d')
ax.set_xticklabels(fontsize=14)
ax.set_yticklabels(fontsize=14)
ax.fig.subplots_adjust(top=0.92)
ax.fig.suptitle('WORLD POPULATION', fontsize=24)
st.pyplot(ax)
import plotly.express as px
fig = px.choropleth(overview,
                     locations="iso_code",
                     color="population",
                     hover_name="location",
                     projection="natural earth",
                     color_continuous_scale= 'tempo',
                     range_color=[0,1450000000])
st.plotly_chart(fig)
fig = px.choropleth(overview,
                     locations="iso_code",
                     color="median_age",
                     hover_name="location",
                     projection="natural earth",
                     color_continuous_scale= 'tempo',
                     range_color=[10,60])
st.markdown('MEDIAN AGE ')
st.plotly_chart(fig)
st.markdown('HUMAN DEVELOPMENT INDEX ')
fig = px.choropleth(overview,
                     locations="iso_code",
                     color="human_development_index",
                     hover_name="location",
                     projection="natural earth",
                     color_continuous_scale= 'tempo',
                     range_color=[0.3,1])
st.plotly_chart(fig)

st.title('DEATHS INFORMATIONS')
st.markdown('WORLD TOTAL DEATHS ')
deaths_total = df.groupby(["location", "iso_code"])['total_deaths', 'total_deaths_per_million',
                                                                      ].max().sort_values(by='total_deaths', ascending=False).reset_index()

fig = px.treemap(deaths_total, path = ['location'], values = 'total_deaths')
st.plotly_chart(fig)

fig = px.choropleth(deaths_total,
                     locations="iso_code",
                     color="total_deaths",
                     hover_name="location",
                     projection="natural earth",
                     color_continuous_scale= 'tempo',
                     range_color=[0,600000])
st.plotly_chart(fig)

st.markdown('WORLD TOTAL DEATHS PER MILLION')
top30_deaths_million = deaths_total.nlargest(30,'total_deaths_per_million')
ax = sns.factorplot(x="total_deaths_per_million", y="location",  data = top30_deaths_million , kind="bar",
                    size=10, aspect=1.5, palette='PuBuGn_d')
ax.set_xticklabels(fontsize=14)
ax.set_yticklabels(fontsize=14)
ax.fig.subplots_adjust(top=0.92)
ax.fig.suptitle('WORLD TOTAL DEATHS PER MILLION', fontsize=24)
st.pyplot(ax)

fig = px.choropleth(deaths_total,
                     locations="iso_code",
                     color="total_deaths_per_million",
                     hover_name="location",
                     projection="natural earth",
                     color_continuous_scale= 'tempo',
                     range_color=[0,2300])
st.plotly_chart(fig)


st.markdown('DAILY DEATHS ')
new_deaths = df[(df["location"]=="Brazil") |(df["location"]=="Mexico")|(df["location"]=='United States') |(df["location"]=='United Kingdom') |(df["location"]=='China') |(df["location"]=='Italy')|(df["location"]=='Argentina')]
new_deaths['rol7'] = new_deaths.new_deaths.rolling(7).mean().shift(0)

fig = px.line(new_deaths, x="date", y="rol7", color='location', title='Daily Deaths (Moving Average)')
st.plotly_chart(fig)

st.markdown('DAILY DEATHS PER MILLION')

new_deaths['rol7_x'] = new_deaths.new_deaths_per_million.rolling(7).mean().shift(0)

fig = px.line(new_deaths, x="date", y="rol7_x", color='location', title='Daily Deaths per Million (Moving Average)')
st.plotly_chart(fig)

st.title('WORLD VACCINATION')
st.markdown('TOTAL VACCINATION ')

vaccine = df.groupby(["location", "iso_code"])['total_vaccinations',
                                                                       'total_vaccinations_per_hundred',
                                                                      'new_vaccinations',
                                                                      'new_vaccinations_smoothed',
                                                                      'people_vaccinated',
                                                                      'people_vaccinated_per_hundred',
                                                                       'people_fully_vaccinated', 'people_fully_vaccinated_per_hundred'
                                                                      ].max().reset_index()
vaccine.columns = ["Country", "iso_code", "Total vaccinations", "Percent", "Daily vaccinations",
                           "Daily vaccinations per million", "People vaccinated", "People vaccinated per hundred",
                           'People fully vaccinated', 'People fully vaccinated percent']

vaccine = vaccine[vaccine['Country'].map(lambda x:str(x)!="World")]
vaccine = vaccine[vaccine['Country'].map(lambda x:str(x)!="South America")]
vaccine = vaccine[vaccine['Country'].map(lambda x:str(x)!="Asia")]
vaccine = vaccine[vaccine['Country'].map(lambda x:str(x)!="North America")]
vaccine = vaccine[vaccine['Country'].map(lambda x:str(x)!="Europe")]
vaccine = vaccine[vaccine['Country'].map(lambda x:str(x)!="European Union")]
vaccine = vaccine[vaccine['Country'].map(lambda x:str(x)!="Africa")]

fig = px.treemap(vaccine, path = ['Country'], values = 'Total vaccinations',
                title="TOTAL VACCINES PER COUNTRY")
st.plotly_chart(fig)

fig = px.choropleth(vaccine,
                     locations="iso_code",
                     color="Total vaccinations",
                     hover_name="Country",
                     projection="natural earth",
                     color_continuous_scale= 'tempo',
                     range_color=[0,150000000])
st.plotly_chart(fig)

st.markdown('POPULATION OF POPULATION VACCINATED')
top30_percent_vaccine = vaccine.nlargest(30,'Percent')
ax = sns.factorplot(x="Percent", y="Country",  data = top30_percent_vaccine , kind="bar",
                    size=10, aspect=1.5, palette='PuBuGn_d')
ax.set_xticklabels(fontsize=12)
ax.set_yticklabels(fontsize=12)
ax.fig.subplots_adjust(top=0.92)
ax.fig.suptitle('Percent Vaccine per Country', fontsize=24)
st.pyplot(ax)

fig = px.choropleth(vaccine,
                     locations="iso_code",
                     color="Percent",
                     hover_name="Country",
                     projection="natural earth",
                     color_continuous_scale= 'tempo',
                     range_color=[0,100])
st.plotly_chart(fig)

st.markdown('PEOPLE FULLY VACCINATED')

top30_fully_vaccinated = vaccine.nlargest(30,'People fully vaccinated')
ax = sns.factorplot(x="People fully vaccinated", y="Country",  data = top30_fully_vaccinated , kind="bar",
                    size=10, aspect=1.5, palette='PuBuGn_d')
ax.set_xticklabels(fontsize=12)
ax.set_yticklabels(fontsize=12)
ax.fig.subplots_adjust(top=0.92)
ax.fig.suptitle('People Fully Vaccinated', fontsize=24)
st.pyplot(ax)

fig = px.choropleth(vaccine,
                     locations="iso_code",
                     color="People fully vaccinated",
                     hover_name="Country",
                     projection="natural earth",
                     color_continuous_scale= 'tempo',
                     range_color=[0,60000000])
st.plotly_chart(fig)

st.markdown('PERCENT OF PEOPLE FULLY VACCINATED')
fig = px.choropleth(vaccine,
                     locations="iso_code",
                     color="People fully vaccinated percent",
                     hover_name="Country",
                     projection="natural earth",
                     color_continuous_scale= 'tempo',
                     range_color=[0,100])
st.plotly_chart(fig)

st.markdown('DAILY VACCINATIONS')

vac_daily = df[(df["location"]=="Brazil") |(df["location"]=="Mexico")|(df["location"]=='United States') |(df["location"]=='United Kingdom') |(df["location"]=='Chile')  |(df["location"]=="China") |(df["location"]=="Italy") |(df["location"]=='Argentina')]
vac_daily = vac_daily[(vac_daily['date'] > '2021-01-01') & (vac_daily['date'] < '2021-04-01')]
vac_daily['rol7'] = vac_daily.new_vaccinations_smoothed.rolling(7).mean().shift(0)

fig = px.line(vac_daily, x="date", y="rol7", color='location', title='Daily Vaccinations')
st.plotly_chart(fig)

st.markdown('DAILY VACCINATIONS PER MILLION')

vac_daily['rol7_x'] = vac_daily.new_vaccinations_smoothed_per_million.rolling(7).mean().shift(0)

fig = px.line(vac_daily, x="date", y="rol7_x", color='location', title='Daily Vaccinations per Million')
st.plotly_chart(fig)

st.title('TO BE CONTINUED')