import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

@st.cache_data
#Load Data CSV
def load_data(url) :
    df = pd.read_csv(url)
    return df

#pembersihn data
def cleaning_data (df_Data):
    data = df_Data.copy()
    
    data.fillna(method='ffill', inplace=True)
    
    non_numeric_columns = data.select_dtypes(exclude=['number']).columns
    data = data.drop(columns=non_numeric_columns)
    
    return data

def cleaning_data_wd (df_Data):
    data_wd = df_Data.copy()
    
    data_wd.fillna(method='ffill', inplace=True)
    return data_wd

def cleaning_data_hourly (df_Data):
    data_hourly = df_Data.copy()
    
    data_hourly.fillna(method='ffill', inplace=True)
    data_hourly['tanggal_jam'] = pd.to_datetime(df_Data[['year', 'month', 'day','hour']], format='%Y-%m-%d %H:%M:%S')
    return data_hourly
#end pembersihn data

#Proses
#Proses Tab 1
#pertanyaan 1
def daily_air_pollution_comparison(data):
    data['tanggal'] = pd.to_datetime(data[['year', 'month', 'day']], format='%Y-%m-%d')

    # Grafik Perbandingan Tingkat PM2.5 per Hari di Aotizhongxin
    st.subheader('Grafik Perbandingan Tingkat PM2.5 per Hari')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=data, x='tanggal', y='PM2.5', ax=ax, label='PM2.5')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Rata-rata Tingkat PM2.5')
    ax.set_title('Perbandingan Tingkat PM2.5 per Hari di Aotizhongxin')
    st.pyplot(fig)

def monthly_air_pollution_comparison(data):
    # Grafik Distribusi Tingkat PM2.5 per Bulan
    st.subheader('Distribusi Tingkat PM2.5 per Bulan')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=data, x='month', y='PM2.5', ax=ax)
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Tingkat PM2.5')
    ax.set_title('Distribusi Tingkat PM2.5 per Bulan')
    st.pyplot(fig)
    
def yearly_air_pollution_comparison(data):
    data['tanggal'] = pd.to_datetime(data[['year', 'month', 'day']], format='%Y-%m-%d')
    
    # Grafik Perbandingan Rata-rata PM2.5 per Tahun
    st.subheader('Grafik Perbandingan Rata-rata PM2.5 per Tahun')
    yearly_pm25_avg = data.groupby(data['tanggal'].dt.year)['PM2.5'].mean().reset_index()
    yearly_pm25_avg.columns = ['Tahun', 'Rata-rata PM2.5']
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=yearly_pm25_avg, x='Tahun', y='Rata-rata PM2.5', palette='coolwarm', ax=ax)
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Rata-rata PM2.5')
    ax.set_title('Grafik Perbandingan Rata-rata PM2.5 per Tahun')
    st.pyplot(fig)

def air_pollution_daily_comparison(data):
    # Perbandingan Tingkat Polusi Udara Harian
    st.subheader('Perbandingan Tingkat Polusi Udara Harian Berdasarkan PM2.5, PM10, SO2, NO2, CO, O3')
    
    # Memilih kolom yang akan ditampilkan
    selected_columns = st.multiselect('Pilih kolom', ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
    st.caption("""
                - PM2.5: Particulate Matter 2.5 (Partikel Udara 2.5)
                - PM10: Particulate Matter 10 (Partikel Udara 10)
                - SO2: Sulfur Dioxide (Diosida Belerang)
                - NO2: Nitrogen Dioxide (Diosida Nitrogen)
                - CO: Carbon Monoxide (Karbon Monoksida)
                - O3: Ozone (Ozon)
                   """)
    
    # Menampilkan plot perbandingan per hari
    if selected_columns:
        daily_average = data.groupby(data['tanggal'].dt.date).mean()
        st.line_chart(daily_average[selected_columns])
         # Penjelasan
        with st.expander("Lihat Penjelasan"):
            st.write("""
                        PM2.5: Particulate Matter 2.5 (Partikel Udara 2.5): Partikel-partikel kecil dengan diameter kurang dari atau sama dengan 2.5 mikrometer, yang dapat masuk ke dalam saluran pernapasan dan menyebabkan gangguan kesehatan.
                        
                        PM10: Particulate Matter 10 (Partikel Udara 10): Partikel-partikel dengan diameter kurang dari atau sama dengan 10 mikrometer, yang juga dapat mempengaruhi kesehatan manusia terutama pada sistem pernapasan.
                        
                        SO2: Sulfur Dioxide (Diosida Belerang): Gas yang dihasilkan dari pembakaran bahan bakar fosil yang mengandung belerang, yang dapat menyebabkan iritasi saluran pernapasan dan masalah kesehatan lainnya.
                        
                        NO2: Nitrogen Dioxide (Diosida Nitrogen): Gas beracun yang dihasilkan dari pembakaran bahan bakar, yang dapat menyebabkan masalah pernapasan dan memperburuk kondisi seperti asma.
                        
                        CO: Carbon Monoxide (Karbon Monoksida): Gas tidak berwarna dan tidak berbau yang dihasilkan dari pembakaran tidak sempurna bahan bakar, yang dapat menyebabkan keracunan CO pada paparan tinggi.
                        
                        O3: Ozone (Ozon): Gas yang dihasilkan dari reaksi kimia antara oksida nitrogen dan senyawa organik volatil di bawah sinar matahari, yang dapat menyebabkan iritasi saluran pernapasan dan memperburuk kondisi kesehatan.
                                """
                        )
        
def main_visualization(data):
    st.subheader("Perbandingan tingkat pulusi udara berdasarkan PM2.5 ")
    pilih_perbandingan_waktu = st.radio(
          "Pilih berdasarkan waktu",
          ("Per Hari","Per Bulan","Per Tahun")
      )
    if (pilih_perbandingan_waktu == "Per Hari"):
        daily_air_pollution_comparison(data)
    elif (pilih_perbandingan_waktu == "Per Bulan"):
        monthly_air_pollution_comparison(data)
    else:
        yearly_air_pollution_comparison(data)
     # Penjelasan
    with st.expander("Lihat Penjelasan"):
        st.write(
            """Untuk menentukan tingkat polusi udara, digunakan PM2.5. PM2.5 adalah partikel halus di udara dengan diameter kurang dari atau sama dengan 2.5 mikrometer. Partikel ini berasal dari berbagai sumber, termasuk emisi kendaraan bermotor, industri, pembakaran biomassa, dan debu.
            """
        )
    st.write('<hr>', unsafe_allow_html=True)
    air_pollution_daily_comparison(data)

#pertanyaan 2        
def air_pollutant_temperature_comparison(data):
    # Perbandingan Tingkat SO2, NO2, dan O3 pada Hari dengan Suhu Tinggi dan Rendah
    st.subheader('Perbandingan Tingkat SO2, NO2, dan O3 pada Hari dengan Suhu Tinggi dan Rendah')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=data, x='TEMP', y='SO2', hue='TEMP', palette='coolwarm', ax=ax)
    sns.boxplot(data=data, x='TEMP', y='NO2', hue='TEMP', palette='coolwarm', ax=ax)
    sns.boxplot(data=data, x='TEMP', y='O3', hue='TEMP', palette='coolwarm', ax=ax)
    ax.set_xlabel('Suhu (Binned)')
    ax.set_ylabel('Tingkat Polutan')
    ax.set_title('Perbandingan Tingkat SO2, NO2, dan O3 pada Hari dengan Suhu Tinggi dan Rendah')
    ax.legend(title='TEMP')
    st.pyplot(fig)

    # Grafik Tingkat Polutan Udara vs Suhu
    st.title('Tingkat Polutan Udara vs Suhu')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=data, x='TEMP', y='PM2.5', hue='TEMP', palette='coolwarm', ax=ax)
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel('Tingkat PM2.5')
    ax.set_title('Tingkat Polutan Udara vs Suhu')
    st.pyplot(fig)
    
# Filter data berdasarkan suhu
def filter_data_by_temperature(data, temperature_threshold):
    data_rendah = data[data['TEMP'] <= temperature_threshold]
    data_tinggi = data[data['TEMP'] > temperature_threshold]
    return data_rendah, data_tinggi

# Hitung rata-rata tingkat SO2, NO2, dan O3
def calculate_average_pollutants(data):
    rata_rata_so2 = data['SO2'].mean()
    rata_rata_no2 = data['NO2'].mean()
    rata_rata_o3 = data['O3'].mean()
    return rata_rata_so2, rata_rata_no2, rata_rata_o3

def visualization_temp_air(data):
    st.subheader('Tingkat SO2, NO2, dan O3 Sesuai Tinggi dan Rendah Suhu')
    # Slider untuk memilih suhu batas
    temperature_threshold = st.slider('Pilih Suhu Batas', min_value=0, max_value=40, value=25, step=1)
    
    # Filter data berdasarkan suhu
    data_rendah, data_tinggi = filter_data_by_temperature(data, temperature_threshold)
    
    # Hitung rata-rata tingkat polutan
    rata_rata_so2_rendah, rata_rata_no2_rendah, rata_rata_o3_rendah = calculate_average_pollutants(data_rendah)
    rata_rata_so2_tinggi, rata_rata_no2_tinggi, rata_rata_o3_tinggi = calculate_average_pollutants(data_tinggi)
    
    # Buat grafik
    fig, ax = plt.subplots()
    ax.plot([0, 1], [rata_rata_so2_rendah, rata_rata_so2_tinggi], label='SO2')
    ax.plot([0, 1], [rata_rata_no2_rendah, rata_rata_no2_tinggi], label='NO2')
    ax.plot([0, 1], [rata_rata_o3_rendah, rata_rata_o3_tinggi], label='O3')

    # Atur label
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel('Tingkat Polutan Udara (μg/m³)')
    ax.set_title('Tingkat Polutan Udara vs Suhu')
    ax.legend()
    st.pyplot(fig)
    with st.expander("Lihat Penjelasan"):
            st.write("""
                        SO2: Sulfur Dioxide (Diosida Belerang): Gas yang dihasilkan dari pembakaran bahan bakar fosil yang mengandung belerang, yang dapat menyebabkan iritasi saluran pernapasan dan masalah kesehatan lainnya.
                        
                        NO2: Nitrogen Dioxide (Diosida Nitrogen): Gas beracun yang dihasilkan dari pembakaran bahan bakar, yang dapat menyebabkan masalah pernapasan dan memperburuk kondisi seperti asma.
                        
                        O3: Ozone (Ozon): Gas yang dihasilkan dari reaksi kimia antara oksida nitrogen dan senyawa organik volatil di bawah sinar matahari, yang dapat menyebabkan iritasi saluran pernapasan dan memperburuk kondisi kesehatan.
                                """
                        )
    st.caption("""
                - PM2.5: Particulate Matter 2.5 (Partikel Udara 2.5)
                - PM10: Particulate Matter 10 (Partikel Udara 10)
                - SO2: Sulfur Dioxide (Diosida Belerang)
                - NO2: Nitrogen Dioxide (Diosida Nitrogen)
                - CO: Carbon Monoxide (Karbon Monoksida)
                - O3: Ozone (Ozon)
                   """)

#Proses Tab 2
# Sepanjang tahun / hari
def Air_Pollution_Hourly_Umum(data, pollutant):
    data['tanggal_jam'] = pd.to_datetime(data[['year', 'month', 'day']], format='%Y-%m-%d %H:%M:%S')
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

#Proses Tab 3
def korelasiSO(data):

    quest3 = data[['TEMP','PRES','WSPM','CO']]

    plt.figure(figsize=(8, 5))
    sns.heatmap(quest3.corr(), cmap='Blues', annot=True, fmt='.2f')
    plt.suptitle("Korelasi kandungan CO", y=1.02)
    plt.show()
    st.pyplot(plt)

def korelasiSO2(data):
    quest4 = data[['TEMP','PRES','WSPM','SO2']]

    plt.figure(figsize=(8, 5))
    sns.heatmap(quest4.corr(), cmap='Blues', annot=True, fmt='.2f')
    plt.suptitle("Korelasi kandungan SO2", y=1.02)
    plt.show()
    st.pyplot(plt)

def korelasiNO2(data):
    quest6 = data[['TEMP','PRES','WSPM','O3']]

    plt.figure(figsize=(8, 5))
    sns.heatmap(quest6.corr(), cmap='Blues', annot=True, fmt='.2f')
    plt.suptitle("Korelasi kandungan O3", y=1.02)
    plt.show()
    st.pyplot(plt)
    with st.expander("See explanation"):
        st.write(
        """ 
        1. Terdapat korelasi yang signifikan pada kandungan CO dan O3, dengan nilai korelasi yang lebih besar dari 0.1. Hal ini menunjukkan adanya hubungan positif antara kandungan CO2 dan O3.
        2. Korelasi yang signifikan juga ditemukan antara kandungan SO2 dan NO2, dengan nilai korelasi yang lebih besar dari 0.1. Ini mungkin menunjukkan adanya polusi udara yang berasal dari sumber yang sama atau proses yang serupa yang menghasilkan kedua zat tersebut.
        3. Namun, tidak ada korelasi yang signifikan yang ditemukan antara kandungan CO2 dan SO2, serta antara kandungan CO2 dan NO2. Hal ini menunjukkan bahwa meskipun kedua pasangan tersebut memiliki nilai korelasi di atas 0.1, hubungan antara kandungan CO2 dan SO2 atau NO2 tidak cukup kuat untuk dianggap signifikan.
        """
    )
    with st.expander("Conclution"):
        st.write(
        """ 
            Semua Kandungan terhadap CO, SO2, dan O3 memiliki korelasi tinggi dikarenakan nilai nya > 0.1
        """
    )

#Proses Tab 4
def pola_curah_hujan (data):
    # Buat kolom 'bulan'
    data['bulan'] = data['tanggal'].dt.strftime('%Y-%m')
    # Perbandingan Per Bulan
    monthly_comparison = data.groupby('bulan').mean()
    # Ekstrak bulan dari kolom tanggal
    data['bulan'] = data['tanggal'].dt.month
    
    # Perbandingan rata-rata curah hujan per bulan
    monthly_rain_comparison = data.groupby('bulan')['RAIN'].mean()
    
    # Visualisasi pola musiman curah hujan
    plt.figure(figsize=(10, 6))
    sns.barplot(x=monthly_rain_comparison.index, y=monthly_rain_comparison)
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata Curah Hujan')
    plt.title('Pola Musiman Curah Hujan')
    st.pyplot(plt)
    with st.expander("See explanation"):
        st.write(
    """Untuk menentukan tingkat polusi udara saya mengambil berdasarkan PM2.5. PM2.5 sebuah istilah yang digunakan untuk mengukur partikel halus di udara, yang memiliki diameter kurang dari atau sama dengan 2.5 mikrometer. Partikel ini dapat berasal dari berbagai sumber, termasuk emisi kendaraan bermotor, industri, pembakaran biomassa, dan debu.
    Seperti ya dilihat berdasarkan grafik bahwa tingkat polusi tertinggi di station Aotizhongxin biasa terjadi di bulan pergantian tahun atau bulan awal awal tahun.
    """
        )

#Proses Tab 5
def perbedaan_polusi(data):
    # Table tingkat polusi udara
    data['tanggal'] = pd.to_datetime(data[['year', 'month', 'day']], format='%Y-%m-%d')
    st.write('#### Tabel Tahun dan Rata-rata Tingkat Polusi Udara Pertahun')
    yearly_pm25_avg = data.groupby(data['tanggal'].dt.year)['PM2.5'].mean().reset_index()
    yearly_pm10_avg = data.groupby(data['tanggal'].dt.year)['PM10'].mean().reset_index()
    yearly_co_avg = data.groupby(data['tanggal'].dt.year)['CO'].mean().reset_index()
    yearly_no2_avg = data.groupby(data['tanggal'].dt.year)['NO2'].mean().reset_index()
    yearly_so2_avg = data.groupby(data['tanggal'].dt.year)['SO2'].mean().reset_index()
    yearly_o3_avg = data.groupby(data['tanggal'].dt.year)['O3'].mean().reset_index()
    yearly_pm_avg = pd.merge(yearly_pm25_avg, pd.merge(yearly_pm10_avg, pd.merge(yearly_co_avg, pd.merge(yearly_no2_avg, pd.merge(yearly_so2_avg, yearly_o3_avg, on='tanggal', how='outer'), on='tanggal', how='outer'), on='tanggal', how='outer'), on='tanggal', how='outer'), on='tanggal', how='outer')
    yearly_pm_avg.columns = ['Tahun', 'Rata-rata PM2.5', 'Rata-rata PM10', 'Rata-rata CO', 'Rata-rata NO2', 'Rata-rata SO2', 'Rata-rata O3']

    yearly_pm_avg = yearly_pm_avg.applymap(lambda x: '{:.0f}'.format(x) if isinstance(x, (int, float)) else x)
    st.write(yearly_pm_avg)


    with st.expander("Lihat Penjelasan"):
        st.write(
            """
            **Tingkat Polusi Udara di Aotizhongxin (2013-2017)**

            Tabel di atas menunjukkan rata-rata tingkat polusi udara di stasiun Aotizhongxin selama periode 2013 hingga 2017. Parameter yang diukur meliputi PM2.5, PM10, CO, NO2, SO2, dan O3.

            - **PM2.5 (Partikulat Matter 2.5):** Merupakan partikel halus dengan diameter kurang dari 2.5 mikrometer. Peningkatan nilai PM2.5 dapat memiliki dampak kesehatan yang signifikan.

            - **PM10 (Partikulat Matter 10):** Merupakan partikel dengan diameter kurang dari 10 mikrometer. Seperti PM2.5, PM10 dapat mempengaruhi kesehatan manusia.

            - **CO (Carbon Monoxide):** Gas beracun yang dapat dihasilkan oleh pembakaran bahan bakar fosil. Peningkatan CO dapat menjadi indikator emisi polusi udara dari kendaraan dan industri.

            - **NO2 (Nitrogen Dioxide):** Gas yang berasal dari pembakaran bahan bakar dan aktivitas industri. Tingkat NO2 dapat memberikan informasi tentang kualitas udara dan dampaknya pada kesehatan manusia.

            - **SO2 (Sulfur Dioxide):** Gas yang dihasilkan oleh pembakaran bahan bakar fosil yang mengandung belerang. SO2 dapat menyebabkan iritasi pada saluran pernapasan.

            - **O3 (Ozone):** Gas yang dapat memiliki dampak positif di atmosfera atas tetapi dapat menjadi polutan di permukaan bumi. Tingkat O3 dapat berkontribusi pada polusi udara dan masalah pernapasan.

            Dari tabel, dapat diamati bahwa tingkat PM2.5 tertinggi terjadi pada tahun 2017, sementara CO, NO2, dan O3 juga menunjukkan variasi selama periode tersebut. Pemahaman tentang pola ini dapat membantu dalam merencanakan langkah-langkah pengelolaan lingkungan untuk meningkatkan kualitas udara di wilayah tersebut.
            """
        )

    st.subheader('Grafik Perbedaan Tingkat Polusi')
    # Analisis korelasi
    correlation_matrix = data[['PM2.5', 'TEMP', 'PRES', 'WSPM']].corr()

    # Visualisasi matriks korelasi menggunakan heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5, ax=ax)
    plt.title('Matriks Korelasi antara Variabel Cuaca dan PM2.5')
    st.pyplot(plt)

    with st.expander("Lihat Penjelasan"):
        st.write(
            """
            Matriks korelasi di atas menggambarkan hubungan statistik antara variabel cuaca (TEMP, PRES, WSPM) dan tingkat polusi udara PM2.5.
            
            - **Korelasi Positif:** Nilai mendekati 1 menunjukkan hubungan positif, di mana kenaikan satu variabel berhubungan dengan kenaikan variabel lainnya.
            
            - **Korelasi Negatif:** Nilai mendekati -1 menunjukkan hubungan negatif, di mana kenaikan satu variabel berhubungan dengan penurunan variabel lainnya.
            
            - **Korelasi Nol:** Nilai mendekati 0 menunjukkan tidak adanya korelasi linier antara dua variabel.
            
            Dari grafik, kita dapat melihat seberapa kuat hubungan antara variabel-variabel tersebut. Misalnya, korelasi positif yang signifikan antara TEMP (suhu) dan PM2.5 mungkin menunjukkan bahwa peningkatan suhu berkaitan dengan peningkatan PM2.5.
            """
        )

#Proses Tab 6   
def Prediksi_PM25(data, model_type='Linear Regression', dataset_size=0.8):
    st.subheader('Konfigurasi Model dan Dataset')

    #pilih variabel cuaca yang akan digunakan untuk prediksi
    features = st.multiselect('Pilih variabel cuaca', ['TEMP', 'DEWP', 'WSPM'])

    st.caption('Penggunaan jumlah variabel yang lebih banyak, meningkatkan keakuratan prediksi PM2.5')

    if not features:
        st.warning('Pilihlah setidaknya satu **variabel cuaca** untuk prediksi PM2.5')
        return
    
    #widget untuk memilih model regresi
    model_type = st.selectbox('Pilih Model Regresi', ['Linear Regression', 'Random Forest'])
    if model_type == 'Linear Regression':
        st.caption('Penggunaan regresi linear memberikan pemahaman yang lebih sederhana dan interpretatif')
    else:
        st.caption('Penggunaan Regresi Hutan Acak memberikan prediksi yang lebih akurat dalam hubungan yang lebih kompleks dalam data')

    #widget untuk mengatur ukuran dataset pengujian
    dataset_size = st.slider('Ukuran Dataset Pengujian', 0.1, 0.9, 0.8, step=0.05)
    st.caption('Ukuran dataset sangat mempengaruhi dari hasil prediksi')

    
    #pilih variabel target (misalnya, PM2.5)
    target = 'PM2.5'
    #pisahkan data menjadi dataset latihan dan pengujian
    X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=dataset_size, random_state=42)
    
    #inisialisasi model
    if model_type == 'Linear Regression':
        model = LinearRegression()
    else:
        model = RandomForestRegressor()
    
    #latih model pada dataset latihan
    model.fit(X_train, y_train)
    
    #lakukan prediksi pada dataset pengujian
    y_pred = model.predict(X_test)
    
    #hitung Mean Squared Error sebagai metrik evaluasi
    mse = mean_squared_error(y_test, y_pred)
    st.write(f'Mean Squared Error: {mse}')

    # Visualisasi hasil prediksi
    fig, ax = plt.subplots(figsize=(10, 6))
    #plot data aktual
    ax.scatter(X_test[features[0]], y_test, label='Actual', alpha=0.8, color='lightblue')
    # Plot data prediksi
    ax.scatter(X_test[features[0]], y_pred, label='Predicted', alpha=0.5, color='lightcoral')
    #atur label
    ax.set_xlabel('(' + ', '.join(features)+')')
    ax.set_ylabel('Tingkat PM2.5')
    ax.set_title('Prediksi Tingkat PM2.5 Berdasarkan ' + ', '.join(features))
    ax.legend()
    
    st.pyplot(fig)

    with st.expander('Penjelasan Tingkat Prediksi PM2.5'):
        st.write("Prediksi tingkat PM2.5 dapat dilakukan dengan parameter TEMP, DEWP, dan WSPM. Bukan hanya itu, untuk memprediksi tingkat PM2.5 dapat menggunakan"
                + "variabel lain juga. Penggunaan model regresi akan menentukan hasil dari prediksi. Jika menggunakan **Regresi Linear** maka dapat memberikan pemahaman"
                + "yang lebih sederhana dan interpretatif, sedangkan jika menggunakan **Regresi Hutan Acak** akan memberikan prediksi yang **lebih akurat**"
                + "dalam hubungan yang lebih kompleks dalam data. Semua itu bergantung dari kebutuhan pengguna dan juga dapat dilakukan eksperimen (uji coba) "
                + "dan evaluasi kinerja pada data model yang lebih spesifik")
        
    st.caption("TEMP : Temprature (Suhu)")
    st.caption("DEWP : Dew Point (Titik Embun)")
    st.caption("WSPM : Wetland Surface Water Model (Aliran & Tinggi Air)")


df_Data = load_data("https://raw.githubusercontent.com/MFaridN/UAS_PDSD/main/PRSA_Data_Aotizhongxin_20130301-20170228.csv")
data_clean = cleaning_data (df_Data)
data_clean_wd = cleaning_data_wd (df_Data)
data_clean_hourly = cleaning_data_hourly(data_clean)

with st.sidebar:
    selected = option_menu('Menu', ['Dashboard','Profile'],
                           icons=["easel2", "graph-up"],
                           menu_icon="cast",
                           default_index=0)
    
    
if (selected == 'Dashboard') :
    st.header(f"Analisis Kualitas Udara")
    st.write('Menggunakan Data Kota Aotizhongxin')
    st.write(data_clean_wd.drop(columns=['No']).head(100))
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["TAB 1", "TAB 2", "TAB 3", "TAB 4", "TAB 5","TAB 6"])

    with tab1:
        st.markdown("**Nama : Muhammad Farid Nurrahman**")
        st.markdown("**Nim : 10122256**")
        st.write('')
        st.markdown("""
                    ### Informasi yang ingin disampaikan
                    - **1. Bagaimana perbandingan tingkat polusi udara perhari,perbulan dan pertahun?**
                    - **2. Apakah tingkat SO2, NO2, dan O3 lebih tinggi pada hari dengan suhu tinggi atau rendah?**
                    """)
        st.write('')
        main_visualization(data_clean)
        st.write('<hr>', unsafe_allow_html=True)
        visualization_temp_air(data_clean)
        
    with tab2:
        st.markdown("**Nama : Erwin Hafiz Triadi**")
        st.markdown("**Nim : 10122269**")
        st.markdown("""
                    ### Informasi yang ingin disampaikan
                    - **1. Bagaimana tren kualitas udara berdasarkan PM2.5, PM10, SO2, NO2, CO, dan O3 selama periode waktu tertentu?**
                    - **2. Penerapan Clustering & Analisis Regresi terhadap informasi no-1 dan tren yang tercipta**
                    """)
        st.write('')
        st.write("Data yang Digunakan di Aotizhongxin")
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
        
    with tab3:
        st.markdown("**Nama :  Mochammad Syahrul Almugni Yusup**")
        st.markdown("**Nim : 10122244**")
        st.markdown("""
                    ### Informasi yang ingin disampaikan
                    - **1. Bagaimana perbandingan tingkat polusi udara perharinya?**
                    """)
        st.write('')
        korelasiSO(data_clean)
        korelasiSO2(data_clean)
        korelasiNO2(data_clean)
        
    with tab4:
        st.markdown("**Nama : Fikkry Ihza Fachrezi**")
        st.markdown("**Nim : 10122510**")
        st.markdown("""
                    ### Informasi yang ingin disampaikan
                    - **Apakah ada perbedaan dalam tingkat polusi udara antara bulan-bulan tertentu atau jam-jam tertentu dalam sehari?**
                    """)
        st.write('')
        st.subheader('Perbedaan Tingkat Polusi')
        perbedaan_polusi(data_clean)

    with tab5:
        st.markdown("**Nama : Win Termulo Nova**")
        st.markdown("**Nim : 10122273**")
        st.markdown("""
                    ### Informasi yang ingin disampaikan
                    - **Bagaimana pola musiman curah hujan memengaruhi kualitas udara**
                    """)
        st.write('')
        st.subheader('Pola Musiman Curah Hujan')
        pola_curah_hujan (data_clean)
    
    with tab6:
        st.markdown("**Nama : Muhammad Pradipta Waskitha**")
        st.markdown("**Nim : 10122265**")
        st.markdown("""
                    ### Informasi yang ingin disampaikan
                    - **Bisakah Memprediksi tingkat PM2.5 Dengan Parameter TEMP,DEWP, dan WSPM?**
                    """)
        st.write('')
        Prediksi_PM25(data_clean)
        
elif (selected == 'Profile') :
    st.header('Proyek Analisis Data: Air Quality Dataset')
    st.markdown("""
                ### Kelompok : IF7- Numpy
                **Anggota :**
                - **10122244 - MOCHAMMAD SYAHRUL ALMUGNI YUSUP**
                - **10122256 - MUHAMMAD FARID NURRAHMAN**
                - **10122265 - MUHAMMAD PRADIPTA WASKITHA**
                - **10122269 - ERWIN HAFIZ TRIADI**
                - **10122269 - ERWIN HAFIZ TRIADI**
                - **10122273 - WIN TERMULO NOVA**
                - **10122510 - FIKKRY IHZA FACHREZI**
                """)
   
    
        
