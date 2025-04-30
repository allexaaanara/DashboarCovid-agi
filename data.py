import streamlit as st
import pandas as pd
import plotly.express as px 

def load_data():
    df = pd.read_csv("covid_19.csv")
    df = df[df["Location"] != "Indonesia"]
    return df

def filter_data(df, year=None, Location=None):
    if year: 
        df = df[df['Date'].astype(str).str.contains(str(year))] 
    if Location:
        df = df[df['Location'].isin(Location)]
    return df 

def select_year(): 
    return st.sidebar.selectbox( 
        "Pilih Tahun 📅", 
        options=[None, 2020, 2021, 2022], 
        format_func=lambda x: "Semua Tahun" if x is None else x 
    )

def select_Location(df):
    Location = ["Semua Provinsi"] + sorted(df['Location'].unique())
    return st.sidebar.multiselect( 
        "Pilih Provinsi 🌍", 
        options= Location,
        default= Location
    )

def show_data(df): 
    selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns) 
    df_selected = df[selected_columns] 
    st.subheader("Data Covid-19 Indonesia 🔴⚪") 
    st.dataframe(df_selected.head(10)) 

    st.subheader("Statistik Deskriptif Dataset")
    st.write(df.describe())

# Fungsi untuk total kasus 
def total_case(df):     
    total_kasus = df.sort_values("Date").groupby("Location", as_index=False).last() 
    return total_kasus["Total Cases"].sum()

# Fungsi untuk total kematian 
def total_death(df): 
    total_mati = df['Total Deaths'].sum() 
    return total_mati 

# Fungsi untuk total sembuh 
def total_recovery(df): 
    total_sembuh = df['Total Recovered'].sum() 
    return total_sembuh 

def kolom(df):
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Kasus📈", value=kasus, border=True)
    col2.metric(label="Total Kematian💀", value=kematian, border=True)
    col3.metric(label="Total Sembuh😷", value=sembuh, border=True)

def pie_chart1(df):
    total_mati = total_death(df)
    total_sembuh = total_recovery(df)

    data = {
        'Status' : ['Meninggal', 'Sembuh'],
        'Jumlah' : [total_mati, total_sembuh]
    }

    fig = px.pie(
        data,
        names = 'Status',
        values = 'Jumlah',
        title = 'Perbandingan Total Kematian VS Total Kesembuhan', 
        hole = 0.5,
        color_discrete_sequence = ['#ff6459', '#4de89f']
    )

    st.plotly_chart(fig, use_container_width=True)

def bar_chart(df):
    df_last = df.sort_values("Date").groupby("Location", as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Deaths')

    fig = px.bar(
        top5,
        x = 'Location',
        y = 'Total Deaths',
        title = '5 Provinsi dengan Total Kematian Tertinggi',
        color = 'Total Deaths',
        color_continuous_scale="Reds",
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )

    fig.update_layout(
        xaxis_title='Provinsi',
        yaxis_title='Total Kematian',
        title_x=0.5,)
    
    st.plotly_chart(fig, use_container_width=True)

def bar_chart2(df):
    df_last = df.sort_values("Date").groupby("Location", as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Recovered')

    fig = px.bar(
        top5,
        x = 'Location',
        y = 'Total Recovered',
        color= 'Total Recovered',
        color_continuous_scale="Greens",
        title = '5 Provinsi dengan Total Kesembuhan Tertinggi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )

    fig.update_layout(
        xaxis_title='Provinsi',
        yaxis_title='Total Kesembuhan',
        title_x=0.5,)
    
    st.plotly_chart(fig, use_container_width=True)

def map_chart(df, year=None):
    df["Date"] = pd.to_datetime(df["Date"])
    if year:
        df["Year"] = df[df["Date"].dt.year == year]
    
    df_agg = df.groupby(["Location", "Latitude", "Longitude"], as_index=False)["New Cases"].sum()
    df_map = df_agg.dropna(subset=["Latitude", "Longitude" , "New Cases"])
    if df_map.empty:
        st.info("Tidak ada data untuk ditampilkan di peta.")
        return
    
    fig = px.scatter_geo(
        df_map,
        lat="Latitude",
        lon="Longitude",
        color="New Cases",
        size="New Cases",
        hover_name="Location",
        projection="mercator",
        color_continuous_scale="OrRd",
        template="plotly_dark",
        size_max=25,
        opacity=0.75,
        title="Peta Sebaran Kasus COVID-19 di Indonesia",
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
    )

    st.plotly_chart(fig, use_container_width=True)


        