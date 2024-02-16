import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from streamlit_option_menu import option_menu

# testing
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

@st.cache_data
#Load Data CSV
def load_data(url) :
    df = pd.read_csv(url)
    return df

def cleaning_data (data1):
    # Copy DataFrame to avoid modifying original data
    data = data1.copy()
    
    # Fill missing values with forward fill method
    data.fillna(method='ffill', inplace=True)
    
    # Drop non-numeric columns
    non_numeric_columns = data.select_dtypes(exclude=['number']).columns
    data = data.drop(columns=non_numeric_columns)
    
    return data

def cleaning_data_wd (data1):
    # Copy DataFrame to avoid modifying original data
    data_wd = data1.copy()
    
    # Fill missing values with forward fill method
    data_wd.fillna(method='ffill', inplace=True)
    
    data_wd['tanggal_jam'] = pd.to_datetime(data1[['year', 'month', 'day','hour']], format='%Y-%m-%d %H:%M:%S')
    
    return data_wd

# def Air_Pollution_hour_some(data1):
# Sepanjang tahun / hari
def Air_Pollution_Hourly_Umum(data1, pollutant):
    # Convert date columns to datetime
    data1['tanggal_jam'] = pd.to_datetime(data1[['year', 'month', 'day']], format='%Y-%m-%d %H:%M:%S')
    # Group by date and calculate hourly mean based on the selected pollutant
    hourly_comparison = data1.groupby('tanggal_jam')[pollutant].mean()
    
    # Visualisasi per jam
    plt.figure(figsize=(20, 6))
    plt.plot(hourly_comparison.index, hourly_comparison, label=pollutant)
    plt.xlabel('Jam dalam Sehari')
    plt.ylabel(f'Rata-rata Tingkat {pollutant}')
    plt.title(f'Perbandingan Tingkat {pollutant} per Jam dalam Sehari')
    plt.legend()
    st.pyplot(plt)

# satu tahun terakhir 

    # 
def Air_Pollution_One_Year(data1, pollutant):
    tanggal_terakhir = data1['tanggal_jam'].max()
    tanggal_sebelumnya = tanggal_terakhir - pd.DateOffset(years=1)

    # Filter data untuk satu tahun terakhir
    data_one_year = data1[(data1['tanggal_jam'] >= tanggal_sebelumnya) & (data1['tanggal_jam'] <= tanggal_terakhir)]
    
    # Perhitungan rata-rata tingkat polutan per jam dalam sehari
    hourly_comparison_one_year = data_one_year.groupby(data_one_year['tanggal_jam']).mean()
    
    # Visualisasi per jam
    plt.figure(figsize=(15, 6))
    plt.plot(hourly_comparison_one_year.index, hourly_comparison_one_year[pollutant], marker="o", markersize=5, label=pollutant)

    plt.xlabel('Waktu')
    plt.ylabel(f'Rata-rata Tingkat {pollutant}')
    plt.title(f'Perbandingan Tingkat {pollutant} per jam dalam sehari selama satu tahun terakhir')
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.xticks(rotation=45, ha="right")
    plt.xlim(hourly_comparison_one_year.index.min(), hourly_comparison_one_year.index.max())
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gca().set_ylim(bottom=0)  # Mengatur batas bawah sumbu y ke 0 agar tidak negatif
    plt.tight_layout()
    st.pyplot(plt)

# Satu tahun terakhir end

# Satu bulan terakhir
def Air_Pollution_Last_Month(data1, pollutant):
    bulan_terakhir = data1['tanggal_jam'].max()
    start_date = bulan_terakhir - pd.DateOffset(months=1)

    data_one_month = data1[(data1['tanggal_jam'] >= start_date) & (data1['tanggal_jam'] <= bulan_terakhir)]
    
    hourly_comparison_one_month = data_one_month.groupby(data_one_month['tanggal_jam']).mean()

    # Visualisasi per jam
    plt.figure(figsize=(15, 6))
    plt.plot(hourly_comparison_one_month.index, hourly_comparison_one_month[pollutant], marker="o", markersize=5, label=pollutant)

    plt.xlabel('Waktu')
    plt.ylabel(f'Rata-rata Tingkat {pollutant}')
    plt.title(f'Perbandingan Tingkat {pollutant} per jam dalam sehari selama satu bulan terakhir')
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.xticks(rotation=45, ha="right")
    plt.xlim(hourly_comparison_one_month.index.min(), hourly_comparison_one_month.index.max())
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gca().set_ylim(bottom=0)  # Mengatur batas bawah sumbu y ke 0 agar tidak negatif
    plt.tight_layout()
    st.pyplot(plt)
# Satu bulan terakhir end
    
# testing
def air_quality_regression(data2):
    X = data2[['TEMP']]
    y = data2['PM2.5']
    X = sm.add_constant(X)
    model = sm.OLS(y, X)
    results = model.fit()
    return results.summary()

def perform_clustering(data3):
    X = data3[['TEMP', 'PRES', 'WSPM']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=3, random_state=0)
    data3['cluster'] = kmeans.fit_predict(X_scaled)
    return data3
# testing end

data1 = load_data("https://raw.githubusercontent.com/MFaridN/UAS_PDSD/main/PRSA_Data_Aotizhongxin_20130301-20170228.csv")
data_bersih = cleaning_data(data1)
data_bersih_hourly = cleaning_data_wd(data_bersih)

# Sidebar
with st.sidebar :
  
  st.header("Klentit")
  menu = option_menu('Menu',["Dashboard","Profile"],
    icons = ["ease12", "graph-up"],
    menu_icon = "cast",
    default_index = 0)

# Side bar END


# main view
if (menu == "Dashboard"):
    # airPolutionTesting(data_bersih)
    # Air_Pollution_one_year_PM10(data_bersih_hourly)
    # st.write("qq")
    # Air_Pollution_Last_Month(data_bersih_hourly,"PM10")

    # Air_Pollution_one_year_PM10(data_bersih)
    # st.write(data_bersih.columns)
    
      

    tab1, tab2 = st.tabs(["Klentit 1","Klentit2" ]) 
    with tab1 :
      # testing
      st.header("Hasil Clustering")
      data_with_cluster = perform_clustering(data_bersih)
      st.write(data_with_cluster.tail())
      # Misalnya, Anda bisa menampilkan scatter plot untuk melihat pemetaan klaster
      plt.scatter(data_with_cluster['TEMP'], data_with_cluster['PRES'], c=data_with_cluster['cluster'], cmap='viridis')
      plt.xlabel('TEMP')
      plt.ylabel('PRES')
      plt.title('Hasil Clustering')
      st.pyplot(plt)


    # testing end
      # Display data tail dari data main atau data bersih dulu
      st.write("Bagaimana tren kualitas udara berdasarkan PM2.5, PM10, SO2, NO2, CO, dan O3 selama periode waktu tertentu?")
      st.write("Nama : Erwin Hafiz Triadi")
      st.write("Nim : 10122269")
      st.title("Data yang Digunakan di Atongxinzin")
      st.write(data_bersih.tail())
      st.header("Overview tren sepanjang waktu")
      Air_Pollution_Hourly_Umum(data_bersih,"PM10")
      with st.expander("Penjelasan Tingkat PM10 per jam dalam sehari") :
        st.write('Dilihat dari grafik diatas dapat dilihat dan diketahui tren sepanjang waktu dimana terjadi kenaikan dan penurunan') 
      st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah
      Air_Pollution_Hourly_Umum(data_bersih,"PM2.5")
      with st.expander("Penjelasan Tingkat PM2.5 per jam dalam sehari") :
        st.write('Dilihat dari grafik diatas, terlihat dari proses pengiriman sudah sangat baik, terdapat 96.478 paket terkirim, dan perbandingannya sangat signifikan dibanding dengan proses yang lain. namun perlu dianalisa kembali untuk pengirimannya apakah sudah tepat waktu atau tidak')
      st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah
      Air_Pollution_Hourly_Umum(data_bersih,"SO2")
      with st.expander("Penjelasan Tingkat PM2.5 per jam dalam sehari") :
        st.write('Dilihat dari grafik diatas, terlihat dari proses pengiriman sudah sangat baik, terdapat 96.478 paket terkirim')
      st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah
      Air_Pollution_Hourly_Umum(data_bersih,"O3")
      with st.expander("Penjelasan Tingkat PM2.5 per jam dalam sehari") :
        st.write('Dilihat dari grafik diatas, terlihat dari proses pengiriman sudah sangat baik, terdapat 96.478 paket terkirim')
      st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah
      Air_Pollution_Hourly_Umum(data_bersih,"NO2")
      with st.expander("Penjelasan Tingkat PM2.5 per jam dalam sehari") :
        st.write('Dilihat dari grafik diatas, terlihat dari proses pengiriman sudah sangat baik, terdapat 96.478 paket terkirim')
      st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah
      pilih_perbandingan2 = st.radio(
            "Pilihan perbandingan",
            ("Satu Tahun Terakhir","Satu Bulan Terakhir" , "semua konsentrasi ")
        )
      
    if pilih_perbandingan2 == "Satu Tahun Terakhir":
            st.write("Satu Tahun Terakhir")
            # Air_Pollution_Hour_PM25(data_bersih)

            st.write("qq")
            Air_Pollution_One_Year(data_bersih_hourly,"PM10")
            Air_Pollution_One_Year(data_bersih_hourly,"PM2.5")
            Air_Pollution_One_Year(data_bersih_hourly,"SO2")
            Air_Pollution_One_Year(data_bersih_hourly,"O3")
            Air_Pollution_One_Year(data_bersih_hourly,"NO2")


            

    elif pilih_perbandingan2 == "Satu Bulan Terakhir":
            st.write("Perbandingan hanya selama satu bulan terakhir")
            Air_Pollution_Last_Month(data_bersih_hourly,"PM10")
            Air_Pollution_Last_Month(data_bersih_hourly,"PM2.5")
            Air_Pollution_Last_Month(data_bersih_hourly,"SO2")
            Air_Pollution_Last_Month(data_bersih_hourly,"O3")
            Air_Pollution_Last_Month(data_bersih_hourly,"NO2")
         


    with tab2 :
      st.header("Klentit tab 2")
    #   Air_Pollution_one_last_month(data_bersih)


#Main view end
