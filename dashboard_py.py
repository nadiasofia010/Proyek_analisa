import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

sns.set(style='white')
st.set_option('deprecation.showPyplotGlobalUse', False)

df = pd.read_csv("hour_cleaned.csv")

def humidity_f(df):
    humidity_v = df.groupby(['Humidity'])['Total_rental'].sum().reset_index()
    return humidity_v

def workingday_f(df):
    workingday_v = df.groupby(['Workingday'])['Total_rental'].sum().reset_index()
    return workingday_v

humidity_plt = humidity_f(df)
workingday_plt = workingday_f(df)

with st.sidebar:
    st.image("https://i.pinimg.com/236x/e4/09/6f/e4096f0afce5bbb76ef00df733a2e951.jpg")
    day_select = st.multiselect("Filter Hari kerja", workingday_plt['Workingday'].unique(), default=workingday_plt['Workingday'].unique())

st.header(':arrow: Analisis Rental Sepeda')
st.subheader(':bike: Total Customer')

columns = st.columns(1)

with columns[0]:
    total_rental_sum = df['Total_rental'].sum()
    st.metric('Total Customer saat ini', total_rental_sum)

# Container for filter humidity
with st.container():
    st.subheader('Distribusi penyewaan sepeda berdasarkan waktu pada hari kerja dan hari libur:')

if selected_intervals:
    filter_humidity = humidity_plt[humidity_plt['Humidity'].isin(selected_intervals)]
else:
    filter_humidity = humidity_plt

# Visualize data
plt.figure(figsize=(12, 6))  
if not filter_humidity.empty:
    sns.boxplot(x='Hour', 
                y='Total_rental', 
                hue='Workingday', 
                data=df)  
    plt.xlabel('Jam (Hour)')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.legend(title='Hari Kerja')
    plt.tight_layout()
    st.pyplot()

with st.container():
    st.subheader('Perbedaan pola penyewaan sepeda antara hari kerja dan hari libur:')
    filtered_day = df[df['Workingday'].isin(day_select)]

    
    workingday_plot = filtered_day.groupby('Workingday')['Total_rental'].sum().reset_index()

    plt.figure(figsize=(12, 6))  
if not workingday_plot.empty:
    sns.lineplot(x='Hour', 
                 y='Total_rental', 
                 hue='Workingday', 
                 data=df, 
                 ci=None)  
    plt.xlabel('Jam (Hour)')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.legend(title='Hari Kerja')
    plt.tight_layout()
    st.pyplot()
else:
    st.write("Mohon Untuk Memilih Minimal Satu Filter")

