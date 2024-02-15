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
    # # Buat kolom 'bulan'
    # data['bulan'] = data['tanggal'].dt.strftime('%Y-%m')
    # # Perbandingan Per Bulan
    # monthly_comparison = data.groupby('bulan').mean()
    # # Ekstrak bulan dari kolom tanggal
    # data['bulan'] = data['tanggal'].dt.month
    # df_tabel = pd.DataFrame({data['bulan']})  
    # st.dataframe(tabel=df, width=500, height=150)
    
    # Convert date columns to datetime
    data['tanggal'] = pd.to_datetime(data[['year', 'month', 'day']], format='%Y-%m-%d')
    # Group by date and calculate daily mean
    daily_comparison = data.groupby('tanggal').mean()
    
    
    # Plotting
    plt.figure(figsize=(12, 6))
    sns.set_theme()
    plt.plot(data['tanggal'], data['PM2.5'], label='PM2.5')
    plt.xlabel('Tanggal')
    plt.ylabel('Rata-rata Tingkat PM2.5')
    plt.title('Perbandingan Tingkat PM2.5 per Hari di Aotizhongxin')
    plt.legend()
    st.pyplot(plt)
    with st.expander("See explanation"):
        st.write(
    """Untuk menentukan tingkat polusi udara saya mengambil berdasarkan PM2.5. PM2.5 sebuah istilah yang digunakan untuk mengukur partikel halus di udara, yang memiliki diameter kurang dari atau sama dengan 2.5 mikrometer. Partikel ini dapat berasal dari berbagai sumber, termasuk emisi kendaraan bermotor, industri, pembakaran biomassa, dan debu.
    Seperti ya dilihat berdasarkan grafik bahwa tingkat polusi tertinggi di station Aotizhongxin biasa terjadi di bulan pergantian tahun atau bulan awal awal tahun.
    """
        )


def pola_curah_hujan (data):
    # Perbandingan per bulan (atau sesuaikan dengan periode waktu yang diinginkan)
    # Buat kolom 'bulan'
    data['bulan'] = data['tanggal'].dt.strftime('%Y-%m')
    # Perbandingan Per Bulan
    monthly_comparison = data.groupby('bulan').mean()
    monthly_comparison
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
    plt.show()
    with st.expander("See explanation"):
        st.write(
    """Untuk menentukan tingkat polusi udara saya mengambil berdasarkan PM2.5. PM2.5 sebuah istilah yang digunakan untuk mengukur partikel halus di udara, yang memiliki diameter kurang dari atau sama dengan 2.5 mikrometer. Partikel ini dapat berasal dari berbagai sumber, termasuk emisi kendaraan bermotor, industri, pembakaran biomassa, dan debu.
    Seperti ya dilihat berdasarkan grafik bahwa tingkat polusi tertinggi di station Aotizhongxin biasa terjadi di bulan pergantian tahun atau bulan awal awal tahun.
    """
        )
        

def perbedaan_polusi(data):
    # Analisis korelasi
    correlation_matrix = data[['PM2.5', 'TEMP', 'PRES', 'WSPM']].corr()

    # Visualisasi matriks korelasi menggunakan heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
    plt.title('Matriks Korelasi antara Variabel Cuaca dan PM2.5')
    plt.show()

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
        st.subheader('Perbandingan Tingkat PM2.5 per Hari')
        Air_Pollution_Day(data_clean)
    with tab2:
        st.header("Tab 2")
        
    with tab3:
        st.header("Tab 3")
        st.image("https://static.streamlit.io/examples/owl.jpg")
    with tab4:
        st.subheader('10122510 - Fikkry Ihza Fachrezi')
        st.subheader('Perbedaan Tingkat Polusi')
        perbedaan_polusi(data_clean)

    with tab5:
        st.header("Tab 3")
        st.image("https://static.streamlit.io/examples/owl.jpg")
    with tab6:
        st.header("Tab 3")
        st.image("https://static.streamlit.io/examples/owl.jpg")