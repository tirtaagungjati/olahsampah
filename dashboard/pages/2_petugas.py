import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import plotly.graph_objects as go

df = pd.read_excel("Data/data_gaji_pengeluaran.xlsx")
df['Uang Bersih'] = df['UMK Kota Bandung (Rp)'] - df['Rata-rata Pengeluaran Perkapita Sebulan (Rp)']
list_tahun = df['Tahun'].tolist()
list_tahun = tuple(list_tahun)
sns.set(style='dark')
plt.style.use('dark_background')

st.header('Perbandingan Gaji dengan Pengeluaran Petugas Kebersihan 💸')
with st.sidebar:
    st.image("dashboard/garbage_collector.jpg")
    with st.expander('Data Sources'):
        st.write(
            '''
            1. [Portal Data Kota Bandung](http://data.bandung.go.id/index.php/portal/detail_dataset/a344cc7c-96a0-4eb2-b3f4-a0b438535677)
            2. [Badan Pusat Statistik](https://bandungkota.bps.go.id/indicator/5/2042/2/rata-rata-pengeluaran-perkapita-sebulan-menurut-kelompok-makanan-dan-non-makanan-di-kota-bandung.html) | [Additional Link](https://jabar.bps.go.id/statictable/2022/07/08/645/rata-rata-pengeluaran-per-kapita-sebulan-makanan-dan-bukan-makanan-menurut-kabupaten-kota-di-provinsi-jawa-barat-rupiah-2020-dan-2021.html)
            3. [Kompas](https://regional.kompas.com/read/2022/09/12/183604178/upah-minimum-kota-bandung-dari-tahun-2012-hingga-2022)
            4. [OKEZONE](https://economy.okezone.com/read/2022/05/16/622/2594875/intip-gaji-petugas-kebersihan-di-bandung-dan-jakarta)
            '''
        )
    st.write(
            '''
            Contact:\\
            [tirtaagungjati18@gmail.com](mailto:tirtaagungjati18@gmail.com)\\
            [LinkedIn](https://www.linkedin.com/in/tirta-agung-jati)
            '''
        )
    
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Tahun'], y=df['UMK Kota Bandung (Rp)'], mode='lines+markers', name='UMK Kota Bandung (Rp)'))
fig.add_trace(go.Scatter(x=df['Tahun'], y=df['Rata-rata Pengeluaran Perkapita Sebulan (Rp)'], mode='lines+markers', name='Rata-rata Pengeluaran Perkapita Sebulan (Rp)'))
fig.add_trace(go.Scatter(x=df['Tahun'], y=df['Uang Bersih'], mode='lines+markers', name='Uang Bersih'))
fig.update_layout(
    title='Plot UMK Kota Bandung, Rata-rata Pengeluaran Perkapita Sebulan, dan Uang Bersih',
    xaxis=dict(title='Tahun'),
    yaxis=dict(title='Jumlah (Rp)'),
)
st.plotly_chart(fig)

option = st.selectbox(
    'Pilih Tahun yang ingin dibandingkan datanya',
    list_tahun)

st.write('You selected:', option)

data = df[df['Tahun'] == option]
values = [data['UMK Kota Bandung (Rp)'].values[0],
          data['Rata-rata Pengeluaran Perkapita Sebulan (Rp)'].values[0],
          data['Uang Bersih'].values[0]]
labels = ['UMK Kota Bandung', 'Rata-rata Pengeluaran Perkapita', 'Uang Bersih']
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.update_layout(
    title=f'Persentase UMK Kota Bandung, Rata-rata Pengeluaran Perkapita, dan Uang Bersih ({option})',
)
st.plotly_chart(fig)

st.header("Disclaimer ")
st.markdown("Data UMK Kota Bandung didapatkan dari berita Kompas yang dilansir dari laman resmi Dinas Tenaga Kerja dan Transmigrasi (Disnakertrans) Jawa Barat")
st.markdown("Data tersebut dijadikan sebuah patokan Gaji Petugas Kebersihan Berdasarkan catatan Okezone dimana Berdasarkan data dari Dinas Lingkungan Hidup dan Kebersihan (DLHK) Gaji yang diterima sesuai dengan UMR Kota Bandung")
st.markdown("Data Rata-rata Pengeluaran Perkapita Sebulan Kota Bandung didapatkan dari laman Badan Pusat Statisik")
st.markdown("Data tersebut sudah termasuk Rata-rata Pengeluaran Perkapita Sebulan Menurut Kelompok Makanan dan non Makanan di Kota Bandung (Rupiah)")
st.caption("Copyright "+ str(datetime.date.today().year) + " " + "[Tirta Agung Jati](https://www.linkedin.com/in/tirta-agung-jati 'Tirta Agung Jati | LinkedIn')")