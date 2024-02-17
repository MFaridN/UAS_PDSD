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

def cleaning_data (df_Data):
    # Copy DataFrame to avoid modifying original data
    data = df_Data.copy()
    
    # Fill missing values with forward fill method
    data.fillna(method='ffill', inplace=True)
    
    # Drop non-numeric columns
    non_numeric_columns = data.select_dtypes(exclude=['number']).columns
    data = data.drop(columns=non_numeric_columns)
    
    return data

def cleaning_data_wd (df_Data):
    # Copy DataFrame to avoid modifying original data
    data_wd = df_Data.copy()
    
    # Fill missing values with forward fill method
    data_wd.fillna(method='ffill', inplace=True)
    
    data_wd['tanggal_jam'] = pd.to_datetime(df_Data[['year', 'month', 'day','hour']], format='%Y-%m-%d %H:%M:%S')
    
    return data_wd

# def Air_Pollution_hour_some(data):
# Sepanjang tahun / hari
def Air_Pollution_Hourly_Umum(data, pollutant):
    # Convert date columns to datetime
    data['tanggal_jam'] = pd.to_datetime(data[['year', 'month', 'day']], format='%Y-%m-%d %H:%M:%S')
    # Group by date and calculate hourly mean based on the selected pollutant
    hourly_comparison = data.groupby('tanggal_jam')[pollutant].mean()
    
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
def Air_Pollution_One_Year(data, pollutant):
    tanggal_terakhir = data['tanggal_jam'].max()
    tanggal_sebelumnya = tanggal_terakhir - pd.DateOffset(years=1)

    # Filter data untuk satu tahun terakhir
    data_one_year = data[(data['tanggal_jam'] >= tanggal_sebelumnya) & (data['tanggal_jam'] <= tanggal_terakhir)]
    
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
def Air_Pollution_Last_Month(data, pollutant):
    bulan_terakhir = data['tanggal_jam'].max()
    start_date = bulan_terakhir - pd.DateOffset(months=1)

    data_one_month = data[(data['tanggal_jam'] >= start_date) & (data['tanggal_jam'] <= bulan_terakhir)]
    
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
def air_quality_regression(data):
    X = data[['TEMP']]
    y = data['PM2.5']
    X = sm.add_constant(X)
    model = sm.OLS(y, X)
    results = model.fit()
    return results.summary()

def perform_clustering(data):
    X = data[['TEMP', 'PRES', 'WSPM']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=3, random_state=0)
    data['cluster'] = kmeans.fit_predict(X_scaled)
    return data
# 
def visualisasi_clustering(data):
    st.header("Hasil Clustering terhadap data yang digunakan")
    data_with_cluster = perform_clustering(data)
    st.write(data_with_cluster.tail(100))
    # Buat objek plot untuk scatter plot
    fig, ax = plt.subplots()

    ax.set_xlabel('TEMP')
    ax.set_ylabel('PRES')
    ax.set_title('Hasil Clustering')

    scatter = plt.scatter(data_with_cluster['TEMP'], data_with_cluster['PRES'], c=data_with_cluster['cluster'], cmap='viridis')

    # legend
    # legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")

    legend_elements = scatter.legend_elements()[0]

    # Mendefinisikan label klaster
    cluster_labels = [f'Cluster {i}' for i in range(1, len(legend_elements) + 1)]

    # Membuat legenda dengan label klaster yang baru dibuat
    legend1 = ax.legend(handles=legend_elements, labels=cluster_labels, title="Clusters")

    st.pyplot(fig)
    with st.expander("Penjelasaan Grafik Clusteringg"):
        st.write('Analisis clustering membantu mengelompokkan data kualitas udara berdasarkan atribut-atribut tertentu seperti suhu, tekanan udara, dan kecepatan angin. Melalui algoritma clustering, data dapat dikelompokkan menjadi beberapa klaster yang memiliki karakteristik yang serupa. Hal ini membantu dalam mengidentifikasi pola atau tren tersembunyi dalam data kualitas udara. Dengan melihat hasil clustering, kita dapat menemukan pola-pola baru yang mungkin tidak terlihat sebelumnya, dan hal ini membantu dalam pemahaman tentang faktor-faktor yang mempengaruhi kualitas udara. Selain itu, penerapan analisis regresi pada setiap klaster yang dihasilkan dapat memberikan wawasan tambahan tentang hubungan antara variabel-variabel tertentu dalam setiap kelompok.')

def visualisasi_regresi(data):
    st.header("Regresi Linier")
    st.write("Analisis regresi linier antara suhu (TEMP) dan PM2.5")
    X = data[['TEMP']]
    y = data['PM2.5']
    X = sm.add_constant(X)
    model = sm.OLS(y, X)
    results = model.fit()

    # Visualisasi regresi linier
    plt.figure(figsize=(10, 6))
    plt.scatter(data['TEMP'], data['PM2.5'], alpha=0.5, label ="Data Observasi")
    plt.plot(data['TEMP'], results.predict(), color='red', label='Regresi Linier')
    plt.xlabel('Suhu (TEMP)')
    plt.ylabel('PM2.5')
    plt.title('Regresi Linier antara Suhu dan PM2.5')
    plt.legend()
    st.pyplot(plt)
    with st.expander("Penjelasaan Grafik Regresi Linear"):
        st.write('Grafik regresi linear menampilkan hubungan antara variabel suhu (TEMP) dan PM2.5. Dalam grafik ini, titik-titik merepresentasikan data pengamatan yang diamati. Garis merah menunjukkan pola atau tren umum dari data tersebut. Dengan melihat grafik, kita dapat mengidentifikasi arah dan kekuatan hubungan antara suhu dan tingkat PM2.5. Titik-titik yang berdekatan atau berkelompok menunjukkan kecenderungan di mana data cenderung berkumpul. Ini membantu kita memahami sebaran data serta pola umum dari hubungan antara suhu dan tingkat PM2.5.') 

    st.header("Summary Regresi Linier")
    st.write("Summary regresi linier menunjukkan ringkasan statistik dari model regresi linier yang telah dibuat.")
    st.text(results.summary())
# testing end

df_Data = load_data("https://raw.githubusercontent.com/MFaridN/UAS_PDSD/main/PRSA_Data_Aotizhongxin_20130301-20170228.csv")
data_clean = cleaning_data(df_Data)
data_clean_wd = cleaning_data_wd (df_Data)
data_clean_hourly = cleaning_data_wd(data_clean)

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

    tab1, tab2 = st.tabs(["Klentit 1","Klentit2" ]) 
    with tab1 :

    # testing end
      # Display data tail dari data main atau data bersih dulu
      st.write("Nama : Erwin Hafiz Triadi")
      st.write("Nim : 10122269")
      st.title("Informasi yang ingin disampaikan")
      st.write("1. Bagaimana tren kualitas udara berdasarkan PM2.5, PM10, SO2, NO2, CO, dan O3 selama periode waktu tertentu?")
      st.write("2. Penerapan Clustering & Analisis Regresi terhadap informasi no-1 dan tren yang tercipta")
      st.title("Data yang Digunakan di Aotizhongxin")
      st.write(data_clean.tail(50))
      st.header("Overview tren sepanjang waktu")
      Air_Pollution_Hourly_Umum(data_clean,"PM10")
      with st.expander("Penjelasan Tingkat PM10 per Jam dalam Sehari Sepanjang waktu") :
        st.write('Grafik di atas menampilkan perubahan tingkat PM10 dalam udara selama periode waktu satu hari. Dari grafik tersebut, kita dapat melihat pola kenaikan dan penurunan tingkat PM10 dari jam ke jam sepanjang hari. Informasi ini membantu kita memahami bagaimana konsentrasi PM10 bervariasi selama periode waktu tertentu dalam satu hari. Perubahan ini dapat dipengaruhi oleh berbagai faktor, termasuk aktivitas manusia, kondisi cuaca, dan pola pergerakan udara. Memahami tren harian PM10 penting untuk mengambil tindakan yang diperlukan guna menjaga kualitas udara dan kesehatan masyarakat.') 
      st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah
      Air_Pollution_Hourly_Umum(data_clean,"PM2.5")
      with st.expander("Penjelasan Tingkat PM2.5 per Jam dalam Sehari Sepanjang waktu") :
        st.write('Grafik di atas memberikan gambaran tentang perubahan tingkat PM2.5 dalam udara sepanjang waktu dalam satu hari. Dari grafik tersebut, kita dapat mengidentifikasi pola tren, baik peningkatan maupun penurunan, dalam tingkat PM2.5 dari jam ke jam selama satu hari. Informasi ini membantu dalam pemahaman tentang fluktuasi harian tingkat PM2.5, yang dapat berkorelasi dengan aktivitas manusia, kondisi cuaca, dan faktor-faktor lingkungan lainnya. Dengan memahami tren harian ini, kita dapat mengambil langkah-langkah yang sesuai untuk mengelola kualitas udara dan menjaga kesehatan masyarakat.')
      st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah
      Air_Pollution_Hourly_Umum(data_clean,"SO2")
      with st.expander("Penjelasan Tingkat SO2(Sulfur dioksida) per Jam dalam Sehari Sepanjang waktu") :
        st.write('Grafik di atas menunjukkan perubahan tingkat sulfur dioksida (SO2) dalam udara selama periode satu hari. Dari grafik tersebut, kita dapat melihat pola naik turunnya tingkat SO2 dari jam ke jam sepanjang hari. Informasi ini membantu kita memahami bagaimana konsentrasi SO2 berubah selama periode tertentu dalam satu hari. Perubahan ini bisa dipengaruhi oleh aktivitas manusia seperti pembakaran bahan bakar fosil, industri, dan transportasi, serta faktor alam seperti aktivitas gunung berapi. Memahami tren harian SO2 penting untuk mengidentifikasi sumber polusi dan mengambil langkah-langkah untuk mengurangi dampaknya terhadap kualitas udara dan kesehatan manusia.')
      st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah
      Air_Pollution_Hourly_Umum(data_clean,"O3")
      with st.expander("Penjelasan Tingkat O3(Ozon) per Jam dalam Sehari Sepanjang waktu") :
        st.write('Grafik di atas menggambarkan perubahan tingkat ozon (O3) dalam udara selama periode waktu satu hari. Dari grafik tersebut, kita dapat melihat pola naik turunnya tingkat ozon dari jam ke jam sepanjang hari. Informasi ini membantu kita memahami bagaimana konsentrasi ozon berubah selama periode tertentu dalam satu hari. Perubahan ini dapat dipengaruhi oleh berbagai faktor, termasuk aktivitas manusia, kondisi cuaca, dan pola pergerakan udara. Memahami tren harian ozon penting untuk mengambil langkah-langkah yang diperlukan guna menjaga kualitas udara dan kesehatan masyarakat.')
      st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah
      Air_Pollution_Hourly_Umum(data_clean,"NO2")
      with st.expander("Penjelasan Tingkat NO2(Nitrogen Dioksida) per Jam dalam Sehari Sepanjang waktu") :
        st.write('Grafik di atas menggambarkan perubahan tingkat nitrogen dioksida (NO2) dalam udara selama periode waktu satu hari. Dari grafik tersebut, kita dapat melihat pola naik turunnya tingkat NO2 dari jam ke jam sepanjang hari. Informasi ini membantu kita memahami bagaimana konsentrasi NO2 berubah selama periode tertentu dalam satu hari. Perubahan ini dapat dipengaruhi oleh berbagai faktor, termasuk aktivitas manusia, kondisi cuaca, dan pola pergerakan udara. Memahami tren harian NO2 penting untuk mengambil langkah-langkah yang diperlukan guna menjaga kualitas udara dan kesehatan masyarakat.')
      st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah
      st.subheader("Pilih perbandingan")
      pilih_perbandingan2 = st.radio(
            "Pilihan perbandingan",
            ("Satu Tahun Terakhir","Satu Bulan Terakhir")
        )
      
    if pilih_perbandingan2 == "Satu Tahun Terakhir":
            st.header("Satu Tahun Terakhir")
            st.write("Pada grafik di bawah ini merupakan perbandingan tren antar jenis polutan dalam waktu 1 (satu) tahun terakhir dari data yang digunakan")
            Air_Pollution_One_Year(data_clean_hourly,"PM10")
            Air_Pollution_One_Year(data_clean_hourly,"PM2.5")
            Air_Pollution_One_Year(data_clean_hourly,"SO2")
            Air_Pollution_One_Year(data_clean_hourly,"O3")
            Air_Pollution_One_Year(data_clean_hourly,"NO2")


            

    elif pilih_perbandingan2 == "Satu Bulan Terakhir":
            st.header("Satu Bulan Terakhir")
            st.write("Pada grafik di bawah ini merupakan perbandingan tren antar jenis polutan dalam waktu 1 (satu) bulan terakhir dari data yang digunakan (sepanjang waktu)")
            Air_Pollution_Last_Month(data_clean_hourly,"PM10")
            Air_Pollution_Last_Month(data_clean_hourly,"PM2.5")
            Air_Pollution_Last_Month(data_clean_hourly,"SO2")
            Air_Pollution_Last_Month(data_clean_hourly,"O3")
            Air_Pollution_Last_Month(data_clean_hourly,"NO2")

    visualisasi_clustering(data_clean_hourly)

    visualisasi_regresi(data_clean_hourly)
    

    with tab2 :
      st.header("Klentit tab 2")
    #   Air_Pollution_one_last_month(data_clean)


#Main view end
