import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
import datetime
import plotly.graph_objects as go
from scipy import stats

st.set_page_config(
    page_title="Dashboard Olah Sampah",
    page_icon="🚛"
)
df = pd.read_csv("dashboard/main_data.csv")
sc_df = pd.read_excel("dashboard/second_data.xlsx")
df['Date'] = pd.to_datetime(df.assign(day=1, month=df['No'], year=df['Tahun'])[['year', 'month', 'day']])
min_date = df['Date'].min()
max_date = df['Date'].max()

def perhitungan_total_tonase(data_sampah):
    ttl_sampah_tahunan = data_sampah.groupby("Tahun")["Tonase (Ton)"].sum()
    ttl_sampah_tahunan = ttl_sampah_tahunan.reset_index()
    ttl_sampah_tahunan.columns = ["Tahun", "Total Tonase (Ton)"]
    return ttl_sampah_tahunan

sns.set(style='dark')
plt.style.use('dark_background')

with st.sidebar:
    st.image("dashboard/garbage_collector.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu Data',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    with st.expander('Data Sources'):
        st.write(
            '''
            1. [Portal Data Kota Bandung](http://data.bandung.go.id/index.php/portal/detail_dataset/a344cc7c-96a0-4eb2-b3f4-a0b438535677)
            2. [Badan Pusat Statistik](https://bandungkota.bps.go.id/indicator/5/2042/2/rata-rata-pengeluaran-perkapita-sebulan-menurut-kelompok-makanan-dan-non-makanan-di-kota-bandung.html) | [Additional Link](https://jabar.bps.go.id/statictable/2022/07/08/645/rata-rata-pengeluaran-per-kapita-sebulan-makanan-dan-bukan-makanan-menurut-kabupaten-kota-di-provinsi-jawa-barat-rupiah-2020-dan-2021.html)
            3. [Kompas](https://regional.kompas.com/read/2022/09/12/183604178/upah-minimum-kota-bandung-dari-tahun-2012-hingga-2022)
            4. [OKEZONE](https://economy.okezone.com/read/2022/05/16/622/2594875/intip-gaji-petugas-kebersihan-di-bandung-dan-jakarta)
            5. [DETIK](https://www.detik.com/jabar/berita/d-6724978/produksi-sampah-di-bandung-meningkat-tiap-tahun)
            6. [Skripsi](https://elibrary.unikom.ac.id/id/eprint/7744/7/UNIKOM_LUKAS%20ALBERTO%20NDOA_BAB%201.pdf)
            '''
        )
    st.write(
            '''
            Contact:\\
            [tirtaagungjati18@gmail.com](mailto:tirtaagungjati18@gmail.com)\\
            [LinkedIn](https://www.linkedin.com/in/tirta-agung-jati)
            '''
        )

main_df = df[(df['Date'] >= str(start_date)) & (df['Date'] <= str(end_date))]
ttl_sampah_tahunan = perhitungan_total_tonase(main_df)
font_size = "20px"
st.header('Darurat Penanganan Sampah di Kota Bandung ♻️')
st.markdown(f"<p style='font-size: {font_size};'>Kota Bandung mulai tanggal 26 Oktober 2023 sampai 26 Desember 2023 menyatakan darurat sampah. Hal ini ditetapkan dalam Keputusan Wali Kota Bandung nomor 658.1/Kep.2523-DLH/2023 tentang Penetapan Situasi Darurat Pengelolaan Sampah.</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size: {font_size};'>Achmad Nugraha, Wakil Ketua II DPRD Kota Bandung, menyoroti lambannya langkah Pemkot Bandung dalam menangani situasi ini, khususnya terkait rencana Pembangkit Listrik Tenaga Sampah (PLTSa) yang belum terealisasi.</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size: {font_size};'>Ia berpendapat bahwa keberhasilan menyelesaikan permasalahan sampah di kota ini memerlukan tindakan serius dari pemerintah, terutama dalam menjalankan kebijakan yang telah ada, seperti Peraturan Daerah tentang Tata Ruang Wilayah.</p>", unsafe_allow_html=True)
with st.expander('Sumber Berita'):
    st.write("[Berita 1](https://www.detik.com/jabar/berita/d-7019155/kritik-pedas-wakil-ketua-dprd-ke-pemkot-bandung-soal-penanganan-sampah)")
    st.write("[Berita 2](https://www.detik.com/jabar/berita/d-7013615/kota-bandung-masih-darurat-sampah)")

st.subheader("Perbandingan Produksi dan Penanganan Sampah")
persentase_penanganan = [round((ps / ps_total) * 100, 2) for ps, ps_total in zip(sc_df["Capaian Penanganan Sampah (Ton)"], sc_df["Produksi Sampah (Ton)"])]
fig = go.Figure()
fig.add_trace(go.Bar(
    x=sc_df["Tahun"],
    y=sc_df["Produksi Sampah (Ton)"],
    name='Produksi Sampah (Ton)',
))
fig.add_trace(go.Bar(
    x=sc_df["Tahun"],
    y=sc_df["Capaian Penanganan Sampah (Ton)"],
    name='Capaian Penanganan Sampah (Ton)',
))
for i, txt in enumerate(persentase_penanganan):
    fig.add_annotation(
        x=sc_df["Tahun"][i],
        y=sc_df["Capaian Penanganan Sampah (Ton)"][i],
        text=f'{txt}%',
        showarrow=True,
        arrowhead=5,
        arrowwidth=2,
        arrowcolor='red',
        font=dict(size=15, color='yellow')
    )
fig.update_layout(
    xaxis_title='Tahun',
    yaxis_title='Jumlah (Ton)',
    barmode='group',
)
st.plotly_chart(fig)
st.markdown(f"<p style='font-size: {font_size};'>Tiap tahun terlihat terjadi peningkatan persentase capaian penanganan sampah yang dikelola. Hal ini terjadi karena produksi sampah yang dihasilkan oleh masyarakat setiap tahunnya menurun. Namun, jumlah sampah yang dapat dikelola tiap tahun bisa dikatakan stagnan, berkisar antara 470-485 ribu ton sampah.</p>", unsafe_allow_html=True)

st.subheader("Total Kompensasi Jasa Pelayanan (Rp) Per Tahun")
fig_kompensasi = go.Figure()
fig_kompensasi.add_trace(go.Bar(
    x=sc_df["Tahun"],
    y=sc_df["Total Kompensasi Jasa Pelayanan (Rp)"],
    name='Total Kompensasi Jasa Pelayanan (Rp)',
    marker=dict(color='green')
))
fig_kompensasi.update_layout(
    xaxis_title='Tahun',
    yaxis_title='Jumlah (Rp)',
)
st.plotly_chart(fig_kompensasi)
st.markdown(f"<p style='font-size: {font_size};'>Tampaknya hal ini bisa terjadi dikarenakan anggaran pengeluaran Kompensasi Jasa Pelayanan (Rp) per tahun di Kota Bandung stagnan atau tidak adanya kenaikan yang signifikan untuk mengatasi permasalahan sampah di kota ini.</p>", unsafe_allow_html=True)

st.subheader("Pengeluaran Kompensasi Jasa Pelayanan Per Ton Sampah (Rp) Per Tahun")
fig_kompensasi = go.Figure()
fig_kompensasi.add_trace(go.Bar(
    x=sc_df["Tahun"],
    y=sc_df["Kompensasi Per Ton Sampah (Rp)"],
    name='Kompensasi Per Ton Sampah (Rp)',
    marker=dict(color='orange')
))
fig_kompensasi.update_layout(
    xaxis_title='Tahun',
    yaxis_title='Jumlah (Rp)',
)
st.plotly_chart(fig_kompensasi)

st.subheader("Plot Pola Tonase Sampah Berdasarkan Bulan")
fig = go.Figure()
for tahun, data_tahun in main_df.groupby('Tahun'):
    fig.add_trace(go.Scatter(x=data_tahun['Bulan'], y=data_tahun['Tonase (Ton)'], mode='lines+markers', name=str(tahun)))
fig.update_layout(xaxis_title='Bulan',
                  yaxis_title='Tonase (Ton)')
st.plotly_chart(fig)
with st.expander('Keterangan'):
    st.write("Tahun 2017: Tertinggi Bulan Oktober Terendah Bulan Februari")
    st.write("Tahun 2018: Tertinggi Bulan November Terendah Bulan Februari")
    st.write("Tahun 2019: Tertinggi Bulan Oktober Terendah Bulan Februari")
    st.write("Tahun 2020: Tertinggi Bulan Januari Terendah Bulan Mei")
    st.write("Tahun 2021: Tertinggi Bulan Januari Terendah Bulan November")
    
st.subheader("Pola Ritasi (Rit) Berdasarkan Bulan untuk Setiap Tahun")
fig = go.Figure()
for tahun, data_tahun in main_df.groupby('Tahun'):
    fig.add_trace(go.Scatter(x=data_tahun['Bulan'], y=data_tahun['Ritasi (Rit)'], mode='lines+markers', name=str(tahun)))
fig.update_layout(xaxis_title='Bulan',
                  yaxis_title='Ritasi (Rit)')
st.plotly_chart(fig)
with st.expander('Keterangan'):
    st.write("Tahun 2017: Tertinggi Bulan Oktober Terendah Bulan Februari")
    st.write("Tahun 2018: Tertinggi Bulan Oktober Terendah Bulan Februari")
    st.write("Tahun 2019: Tertinggi Bulan Oktober Terendah Bulan Februari")
    st.write("Tahun 2020: Tertinggi Bulan Januari Terendah Bulan Mei")
    st.write("Tahun 2021: Tertinggi Bulan Januari Terendah Bulan November")
    
st.subheader("Pola Kompensasi Jasa Pelayanan (Rp) Sampah Berdasarkan Bulan untuk Setiap Tahun")
fig = go.Figure()
for tahun, data_tahun in main_df.groupby('Tahun'):
    fig.add_trace(go.Scatter(x=data_tahun['Bulan'], y=data_tahun['Kompensasi Jasa Pelayanan (Rp)'], mode='lines+markers', name=str(tahun)))
fig.update_layout(xaxis_title='Bulan',
                  yaxis_title='Kompensasi Jasa Pelayanan (Rp)')
st.plotly_chart(fig)
with st.expander('Keterangan'):
    st.write("Tahun 2017: Tertinggi Bulan Oktober Terendah Bulan Februari")
    st.write("Tahun 2018: Tertinggi Bulan November Terendah Bulan Februari")
    st.write("Tahun 2019: Tertinggi Bulan Oktober Terendah Bulan Februari")
    st.write("Tahun 2020: Tertinggi Bulan Januari Terendah Bulan Mei")
    st.write("Tahun 2021: Tertinggi Bulan Januari Terendah Bulan November")
    
st.subheader("Pola Kompensasi Dampak Negatif Sampah Berdasarkan Bulan untuk Setiap Tahun")
fig = go.Figure()
for tahun, data_tahun in main_df.groupby('Tahun'):
    fig.add_trace(go.Scatter(x=data_tahun['Bulan'], y=data_tahun['Kompensasi Dampak Negatif (Rp)'], mode='lines+markers', name=str(tahun)))
fig.update_layout(xaxis_title='Bulan',
                  yaxis_title='Kompensasi Dampak Negatif (Rp)')
st.plotly_chart(fig)
with st.expander('Keterangan'):
    st.write("Tahun 2017: Tertinggi Bulan Oktober Terendah Bulan Februari")
    st.write("Tahun 2018: Tertinggi Bulan Desember Terendah Bulan Februari")
    st.write("Tahun 2019: Tertinggi Bulan Oktober Terendah Bulan Februari")
    st.write("Tahun 2020: Tertinggi Bulan Desember Terendah Bulan Februari")
    st.write("Tahun 2021: Tertinggi Bulan Januari Terendah Bulan November")

puncak_tonase = df.loc[df.groupby('Tahun')['Tonase (Ton)'].idxmax()]
puncak = puncak_tonase[['Bulan', 'Tahun', 'Tonase (Ton)']]
st.subheader("Puncak Tonase Sampah Tiap Tahun")
st.table(puncak)

kenaikan_tonase = df.loc[df.groupby('Tahun')['KenaikanPenurunanTonase (Ton)'].idxmax()]
kenaikan = kenaikan_tonase[['Bulan', 'Tahun', 'KenaikanPenurunanTonase (Ton)', 'KenaikanPenurunanTonase (%)']]
kenaikan = kenaikan.rename(columns={
    'Bulan': 'Bulan',
    'Tahun': 'Tahun',
    'KenaikanPenurunanTonase (Ton)': 'Kenaikan Tonase Sampah (Ton)',
    'KenaikanPenurunanTonase (%)': 'Persentase Kenaikan Sampah (%)'
})
st.subheader("Puncak Kenaikan Tonase Sampah Tiap Tahun")
st.table(kenaikan)

penurunan_tonase = df.loc[df.groupby('Tahun')['KenaikanPenurunanTonase (Ton)'].idxmin()]
penurunan = penurunan_tonase[['Bulan', 'Tahun', 'KenaikanPenurunanTonase (Ton)', 'KenaikanPenurunanTonase (%)']]
penurunan = penurunan.rename(columns={
    'Bulan': 'Bulan',
    'Tahun': 'Tahun',
    'KenaikanPenurunanTonase (Ton)': 'Penurunan Tonase Sampah (Ton)',
    'KenaikanPenurunanTonase (%)': 'Persentase Penurunan Sampah (%)'
})
st.subheader("Lembah Penurunan Tonase Sampah Tiap Tahun")
st.table(penurunan)

Dampak_Negatif = df.loc[df.groupby('Tahun')['Kompensasi Dampak Negatif (Rp)'].idxmax()]
kompensasi = Dampak_Negatif[['Bulan', 'Tahun', 'Tonase (Ton)', 'Kompensasi Dampak Negatif (Rp)']]
st.subheader("Puncak Kompensasi Dampak Negatif (Rp) Sampah Tiap Tahun")
st.table(kompensasi)

st.subheader("Faktor yang mempengaruhi Jumlah Kompensasi Jasa Pelayanan")
# Analisis Regresi Linier antara Kompensasi Jasa Pelayanan (Rp) dan Tonase (Ton)
z_scores = np.abs(stats.zscore(main_df["Kompensasi Jasa Pelayanan (Rp)"]))
outliers = z_scores > 3
fig = go.Figure()
fig.add_trace(go.Scatter(x=main_df["Tonase (Ton)"], y=main_df["Kompensasi Jasa Pelayanan (Rp)"], mode='markers', name='Data'))
fig.add_trace(go.Scatter(x=main_df["Tonase (Ton)"][outliers], y=main_df["Kompensasi Jasa Pelayanan (Rp)"][outliers], mode='markers', marker=dict(color='red', symbol='x'), name='Outlier'))
fig.update_layout(
    title='Analisis Regresi Linier antara Kompensasi Jasa Pelayanan (Rp) dan Tonase (Ton)',
    xaxis=dict(title='Tonase (Ton)'),
    yaxis=dict(title='Kompensasi Jasa Pelayanan (Rp)')
)
st.plotly_chart(fig)

outliers_tk = pd.DataFrame({
    'Tonase (Ton)': main_df["Tonase (Ton)"][outliers],
    'Kompensasi Jasa Pelayanan (Rp)': main_df["Kompensasi Jasa Pelayanan (Rp)"][outliers]
})
with st.expander('Outliers Data'):
    st.write(outliers_tk)
    
# Analisis Regresi Linier antara Kompensasi Jasa Pelayanan (Rp) dan Ritasi (Rit)
z_scores = np.abs(stats.zscore(df["Kompensasi Jasa Pelayanan (Rp)"]))
outliers = z_scores > 3
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Ritasi (Rit)"], y=df["Kompensasi Jasa Pelayanan (Rp)"], mode='markers', name='Data'))
fig.add_trace(go.Scatter(x=df["Ritasi (Rit)"][outliers], y=df["Kompensasi Jasa Pelayanan (Rp)"][outliers], mode='markers', marker=dict(color='red', symbol='x'), name='Outlier'))
fig.update_layout(
    title='Analisis Regresi Linier antara Kompensasi Jasa Pelayanan (Rp) dan Ritasi (Rit)',
    xaxis=dict(title='Ritasi (Rit)'),
    yaxis=dict(title='Kompensasi Jasa Pelayanan (Rp)')
)
st.plotly_chart(fig)
outliers_rk = pd.DataFrame({
    'Ritasi (Rit)': df["Ritasi (Rit)"][outliers],
    'Kompensasi Jasa Pelayanan (Rp)': df["Kompensasi Jasa Pelayanan (Rp)"][outliers]
})
with st.expander('Outliers Data'):
    st.write(outliers_rk)

st.subheader("Hubungan Tonase Sampah dan Ritasi dan apakah ada outliers")
# Analisis Regresi Linier antara Tonase (Ton) dan Ritasi (Rit)
z_scores = np.abs(stats.zscore(df["Tonase (Ton)"]))
outliers = z_scores > 3
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Ritasi (Rit)"], y=df["Tonase (Ton)"], mode='markers', name='Data'))
fig.add_trace(go.Scatter(x=df["Ritasi (Rit)"][outliers], y=df["Tonase (Ton)"][outliers], mode='markers', marker=dict(color='red', symbol='x'), name='Outlier'))
fig.update_layout(
    title='Analisis Regresi Linier antara Tonase (Ton) dan Ritasi (Rit)',
    xaxis=dict(title='Ritasi (Rit)'),
    yaxis=dict(title='Tonase (Ton)')
)
st.plotly_chart(fig)
outliers_rt = pd.DataFrame({
    'Ritasi (Rit)': df["Ritasi (Rit)"][outliers],
    'Tonase (Ton)': df["Tonase (Ton)"][outliers]
})
with st.expander('Outliers Data'):
    st.write(outliers_rt)

st.header("Kesimpulan:")
st.markdown("1. Terdapat dua bulan kemungkinan yang memiliki tonase sampah pada titik puncak atau sangat banyak sampah, yaitu Oktober atau Januari. Selain itu, anomali terjadi pada Tahun 2018 dimana Bulan November memiliki pemuncakan paling tinggi untuk jumlah tonase sampah di Bandung, dan pada tahun-tahun berikutnya, jumlah tonase sampah akan menurun setelah bulan Oktober.")
st.markdown("2. Kenaikan tonase sampah tertinggi terjadi pada Bulan Mei pada Tahun 2017 dengan kenaikan 16.76% dari bulan sebelumnya, yaitu 4972.357 Ton sampah.")
st.markdown("3. Penanganan sampah di Kota Bandung berhasil pada tahun 2021 dengan mengoptimalkan pengeluaran sampah. Pada Bulan November terdapat penurunan tonase sampah sebanyak 17.46% dengan pengurangan sampah sebesar 6970.544 Ton Sampah. Selain itu, kenaikan terbesar pada Desember 2021 hanya sebesar 9.89% atau naik sebesar 3258.696 Ton sampah.")
st.markdown("4. Terdapat perbedaan pada Puncak Kompensasi Dampak Negatif (Rp) dengan Puncak Tonase sampah pada Tahun 2018 dan 2020. Puncak Tonase sampah di tahun 2018 terdapat pada bulan November, sedangkan pada tahun 2020 pada Bulan Januari. Namun, Kompensasi yang didapatkan tidak lebih besar daripada Kompensasi Dampak Negatif akan Sampah yang ada pada tahun 2018 bulan Desember dan tahun 2020 bulan Desember.")
st.markdown("5. Feature Kompensasi Jasa Pelayanan (Rp) memiliki korelasi positif yang kuat dengan Tonase (Ton) dan Ritasi (Rit). Walaupun terdapat 2 outlier negatif, yang berarti kedua data tersebut memiliki nilai Tonase (Ton) atau Ritasi (Rit) yang lebih rendah dari nilai yang diharapkan berdasarkan hubungan linier dengan Kompensasi Jasa Pelayanan (Rp). Faktor ritasi memiliki pengaruh pada rentang rit sebesar 7000-8500 berdasarkan dengan Kompensasi Jasa Pelayanan (Rp), dan faktor Tonase (Ton) sampah memiliki pengaruh pada rentang sebesar 35000-45000.")
st.markdown("6. Feature Tonase (Ton) memiliki korelasi positif yang kuat dengan Ritasi (Rit). Terdapat 1 outlier negatif, yang berarti data tersebut memiliki nilai Ritasi (Rit) yang lebih rendah dari nilai yang diharapkan berdasarkan hubungan linier dengan Tonase (Ton). Faktor ritasi memiliki pengaruh pada rentang rit sebesar 7000-8500 berdasarkan dengan Feature Tonase (Ton).")
st.caption("Copyright "+ str(datetime.date.today().year) + " " + "[Tirta Agung Jati](https://www.linkedin.com/in/tirta-agung-jati 'Tirta Agung Jati | LinkedIn')")
