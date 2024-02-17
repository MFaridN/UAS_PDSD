import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
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

def cleaning_data_hourly (df_Data):
    # Copy DataFrame to avoid modifying original data
    data_hourly = df_Data.copy()
    
    # Fill missing values with forward fill method
    data_hourly.fillna(method='ffill', inplace=True)
    data_hourly['tanggal_jam'] = pd.to_datetime(df_Data[['year', 'month', 'day','hour']], format='%Y-%m-%d %H:%M:%S')
    return data_hourly
    
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
    st.subheader('Perbandingan Data Kualitas Udara di Aotizhongxin')
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

def perbedaan_polusi(data):
    # Table tingkat polusi udara
    data['tanggal'] = pd.to_datetime(data[['year', 'month', 'day']], format='%Y-%m-%d')
    st.subheader('Tabel Tahun dan Rata-rata Tingkat Polusi Udara Pertahun')
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
    st.title(f"Analisis Polusi Udara Aotizhongxin")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["TAB 1", "TAB 2", "TAB 3", "TAB 4", "TAB 5","TAB 6"])

    with tab1:
        st.write("Nama : Muhammad Farid Nurrahman")
        st.write("Nim : 10122256")
        st.header("Informasi yang ingin disampaikan")
        st.write("1. Bagaimana perbandingan tingkat polusi udara perharinya?")
        st.write("2. Penerapan Clustering & Analisis Regresi terhadap informasi no-1 dan tren yang tercipta")
        Air_Pollution_Day(data_clean)
    with tab2:
        st.write("Nama : Erwin Hafiz Triadi")
        st.write("Nim : 10122269")
        st.header("Informasi yang ingin disampaikan")
        st.write("1. Bagaimana tren kualitas udara berdasarkan PM2.5, PM10, SO2, NO2, CO, dan O3 selama periode waktu tertentu?")
        st.write("2. Penerapan Clustering & Analisis Regresi terhadap informasi no-1 dan tren yang tercipta")
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
        st.write("Nama : Mochammad Syahrul Almugni Yusup")
        st.write("Nim : 10122244")
        korelasiSO(data_clean)
        korelasiSO2(data_clean)
        korelasiNO2(data_clean)
    with tab4:
        st.write("Nama : Fikkry Ihza Fachrezi")
        st.write("Nim : 10122510")
        st.subheader('Perbedaan Tingkat Polusi')
        perbedaan_polusi(data_clean)

    with tab5:
        st.write("Nama : Win Termulo Nova")
        st.write("Nim : 10122273")
        st.subheader('Pola Musiman Curah Hujan')
        pola_curah_hujan (data_clean)
    with tab6:
        st.write("Nama : Muhammad Pradipta Waskitha")
        st.write("Nim : 10122265")
        st.image("https://static.streamlit.io/examples/owl.jpg")
        
elif (selected == 'Profile') :
    st.header('Proyek Analisis Data: Air Quality Dataset')
    st.subheader('Kelompok : IF7- Numpy')
    st.subheader('Anggota :')
    st.write('10122244 - MOCHAMMAD SYAHRUL ALMUGNI YUSUP')
    st.write('10122256 - MUHAMMAD FARID NURRAHMAN')
    st.write('10122265 - MUHAMMAD PRADIPTA WASKITHA')
    st.write('10122269 - ERWIN HAFIZ TRIADI')
    st.write('10122273 - WIN TERMULO NOVA')
    st.write('10122510 - FIKKRY IHZA FACHREZI')
    st.write('Isi data yang digunakan')
    st.write(data_clean_wd.tail(50))
    
        
