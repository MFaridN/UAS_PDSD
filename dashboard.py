import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu

@st.cache_data
#Load Data CSV
def load_data(url) :
    df = pd.read_csv(url)
    return df

def df_Air_Quality (df_Data):
    data = df_Data
    data.fillna(method='ffill', inplace=True)  # Menggunakan nilai sebelumnya (forward fill)
    return data

def df_Air_Quality_WD (df_Data):
    data = df_Data
    data.fillna(method='ffill', inplace=True)  # Menggunakan nilai sebelumnya (forward fill)

    # Cari kolom-kolom yang mengandung nilai non-numerik
    non_numeric_columns = data1.select_dtypes(exclude=['number']).columns

    # Drop kolom-kolom non-numerik dari DataFrame
    data = data.drop(columns=non_numeric_columns)
    data
    
df_Data = load_data("https://github.com/MFaridN/UAS_PDSD/blob/main/PRSA_Data_Aotizhongxin_20130301-20170228.csv")

