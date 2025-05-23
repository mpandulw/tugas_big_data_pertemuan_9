import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px

st.title("Visualisasi Data Pengeluaran Perkapita Berdasarkan Gender Tahun 2024")

# Configuration MongoDB
client = MongoClient("mongodb+srv://maozalpandu123:crims0n123@cluster0.spabcda.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Update if using Atlas
db = client["big_data_uts"]
collection = db["data_pengeluaran_perkapita"]

data = list(collection.find({}, {"_id": 0})) 
df = pd.DataFrame(data)

st.dataframe(df)

bar_chart = pd.DataFrame({
    'Wilayah' : df['wilayah'],
    'Pria' : pd.to_numeric(df['Pria'])
}).set_index("Wilayah")

st.subheader("Perbandingan Pengeluaran Pria")
st.bar_chart(bar_chart, horizontal = True, color = "#ffaa00")

# Bar Chart perbandingan pria dan wanita
total_pengeluaran_pria = pd.to_numeric(df['Pria']).sum()
total_pengeluaran_wanita = pd.to_numeric(df['Wanita']).sum()

bar_chart2 = pd.DataFrame({
    'Jenis Kelamin' : ['Pria', 'Wanita'],
    'Total Pengeluaran' : [total_pengeluaran_pria, total_pengeluaran_wanita]
}).set_index('Jenis Kelamin')

st.subheader('Perbandingan Pengeluaran Pria dengan Wanita')
st.bar_chart(bar_chart2)

# Pie Chart Wilayah dengan spender terbanyak
df['Total'] = pd.to_numeric(df['Pria']) + pd.to_numeric(df['Wanita'])

fig = px.pie(
    df,
    names='wilayah',
    values='Total',
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.subheader('Pie Chart Pengeluaran Per Wilayah')
st.plotly_chart(fig)

