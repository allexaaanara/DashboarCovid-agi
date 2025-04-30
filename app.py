import streamlit as st
from data import *

def judul():
    st.title("🏨Dashboard COVID-19🖥️")
    st.markdown("Selamat Datang di Dashboard interaktif untuk menganalisis data COVID-19 di Indonesia")
    st.markdown("by Sabrina Agnia Rachma")
    st.markdown("NPM = 184230023")

st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Home", "Halaman Data"])

if menu == "Home": 
    judul() 
    df = load_data()
    # Pilih tahun 
    year = select_year() 
    Location = select_Location(df)
    # Load & filter data 
    df_filtered = filter_data(df, year, Location) 
    kolom(df_filtered)
    pie_chart1(df_filtered)
    bar_chart(df_filtered)
    bar_chart2(df_filtered)
    map_chart(df_filtered)

elif menu == "Halaman Data": 
    judul() 
    year = select_year() 
    # Load & filter data 
    df = load_data() 
    df_filtered = filter_data(df, year) 
    show_data(df_filtered) 
