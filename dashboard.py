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
    data = df_Data.copy()
    
    # Fill missing values with forward fill method
    data.fillna(method='ffill', inplace=True)
    
    data['tanggal'] = pd.to_datetime(data[['year', 'month', 'day']], format='%Y-%m-%d')
    
    return data
    
def Air_Pollution_Day(data):
    # Convert date columns to datetime
    data['tanggal'] = pd.to_datetime(data[['year', 'month', 'day']], format='%Y-%m-%d')
    

    # Menampilkan tabel dengan tahun dan data rata-rata PM2.5 per tahun
    st.subheader('Tabel Tahun dan Rata-rata PM2.5 Pertahun')
    yearly_pm25_avg = data.groupby(data['tanggal'].dt.year)['PM2.5'].mean().reset_index()
    yearly_pm25_avg.columns = ['Tahun', 'Rata-rata PM2.5']
    
    # Menghilangkan koma dari angka dalam tabel
    yearly_pm25_avg = yearly_pm25_avg.applymap(lambda x: '{:.0f}'.format(x) if isinstance(x, (int, float)) else x)
    st.write(yearly_pm25_avg)
    
    # Plotting
    st.subheader('Grafik Perbandingan Tingkat PM2.5 per Hari di Aotizhongxin')
    plt.figure(figsize=(12, 6))
    sns.set_theme()
    plt.plot(data['tanggal'], data['PM2.5'], label='PM2.5')
    plt.xlabel('Tanggal')
    plt.ylabel('Rata-rata Tingkat PM2.5')
    plt.title('Perbandingan Tingkat PM2.5 per Hari di Aotizhongxin')
    plt.legend()
    st.pyplot(plt)
    
    # Penjelasan
    with st.expander("Lihat Penjelasan"):
        st.write(
    """Untuk menentukan tingkat polusi udara, digunakan PM2.5. PM2.5 adalah partikel halus di udara dengan diameter kurang dari atau sama dengan 2.5 mikrometer. Partikel ini berasal dari berbagai sumber, termasuk emisi kendaraan bermotor, industri, pembakaran biomassa, dan debu.
    Dari grafik, dapat dilihat bahwa tingkat polusi udara tertinggi di stasiun Aotizhongxin biasanya terjadi pada bulan-bulan pergantian tahun atau awal tahun.
    """
        )
    st.subheader('Perbandingan Data Kualitas Udara perhari di Aotizhongxin')
    # Memilih kolom yang akan ditampilkan
    selected_columns = st.multiselect('Pilih kolom', ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'wd', 'WSPM'])

    # Menampilkan plot perbandingan per hari
    if selected_columns:
        daily_average = data.groupby(data['tanggal'].dt.date).mean()
        st.line_chart(daily_average[selected_columns])

def pola_curah_hujan (data):
    # Perbandingan per bulan (atau sesuaikan dengan periode waktu yang diinginkan)
    # Buat kolom 'bulan'
    data['bulan'] = data['tanggal'].dt.strftime('%Y-%m')
    # Perbandingan Per Bulan
    monthly_comparison = data.groupby('bulan').mean()
    # Ekstrak bulan dari kolom tanggal
    data['bulan'] = data['tanggal'].dt.month
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
         

    with tab1:
        st.subheader('10122256 - Muhammad Farid Nurrahman')
        Air_Pollution_Day(data_clean)
    with tab2:
        st.header("Tab 2")
        
    with tab3:
        st.subheader('10122244 - Mochammad Syahrul Almugni Yusu')
        korelasiSO(data_clean)
        korelasiSO2(data_clean)
        korelasiNO2(data_clean)
    with tab4:
        st.subheader('10122510 - Fikkry Ihza Fachrezi')
        st.subheader('Perbedaan Tingkat Polusi')
        perbedaan_polusi(data_clean)

    with tab5:
        st.subheader('10122273 - Win Termulo Nova')
        st.subheader('Pola Musiman Curah Hujan')
        pola_curah_hujan (data_clean)
    with tab6:
        st.header("Tab 3")
        st.image("https://static.streamlit.io/examples/owl.jpg")

    with tab2 :
      st.header("Klentit tab 2")
    #   Air_Pollution_one_last_month(data_bersih)


#Main view end
