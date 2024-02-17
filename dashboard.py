import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

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
    
    data_wd['tanggal'] = pd.to_datetime(data_wd[['year', 'month', 'day']], format='%Y-%m-%d')
    
    return data_wd
    
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
    st.subheader('10122510 - Fikkry Ihza Fachrezi')
    # st.subheader('Grafik Tingkat Polusi Udara')
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

df_Data = load_data("https://raw.githubusercontent.com/MFaridN/UAS_PDSD/main/PRSA_Data_Aotizhongxin_20130301-20170228.csv")
data_clean = cleaning_data (df_Data)
data_clean_wd = cleaning_data_wd (df_Data)

with st.sidebar:
    selected = option_menu('Menu', ['Dashboard'],
                           icons=["easel2", "graph-up"],
                           menu_icon="cast",
                           default_index=0)
if (selected == 'Dashboard') :
    st.header(f"Analisis Polusi Udara Aotizhongxin")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5","Pertanyaan 6"])

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

        perbedaan_polusi(data_clean)

    with tab5:
        st.subheader('10122273 - Win Termulo Nova')
        st.subheader('Pola Musiman Curah Hujan')
        pola_curah_hujan (data_clean)
    with tab6:
        st.header("Tab 3")
        st.image("https://static.streamlit.io/examples/owl.jpg")