import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor



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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5","Pertanyaan 6","Prediksi Tingkat PM2.5"])

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
        st.header("Tab 3")
        st.image("https://static.streamlit.io/examples/owl.jpg")
    with tab5:
        st.header("Tab 3")
        pola_curah_hujan (data_clean)
    with tab6:
        st.header("Tab 3")
        st.image("https://static.streamlit.io/examples/owl.jpg")
    with tab7:
        st.header("10122265 - Muhammad Pradipta Waskitha")
        st.markdown('**Bisakah Memprediksi tingkat PM2.5 Dengan Parameter TEMP,DEWP, dan WSPM?**')
        Prediksi_PM25(data_clean)
        
        