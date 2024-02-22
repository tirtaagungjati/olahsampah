import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import plotly.graph_objects as go

data_sampah = pd.read_csv("dashboard/pages/data_sampah.csv")
Kompensasi_Jasa_pred = pd.read_csv("dashboard/pages/kjp_with_mlr.csv")
Kompensasi_Jasa_pred_with_randomforest = pd.read_csv("dashboard/pages/kjp_with_randomforest.csv")
Kompensasi_Jasa_pred_with_xgb = pd.read_csv("dashboard/pages/kjp_with_xgb.csv")
data_eval_train = pd.read_csv("dashboard/pages/data_eval_train.csv",index_col=0)
data_eval_test = pd.read_csv("dashboard/pages/data_eval_test.csv",index_col=0)
sns.set(style='dark')
plt.style.use('dark_background')

st.header('Regression pada Kompensasi Jasa Pelayanan (Rp) 📈')
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
fig.add_trace(go.Scatter(x=data_sampah['Date'],y=data_sampah['Kompensasi Jasa Pelayanan (Rp)'], mode='lines', name='Kompensasi Jasa Pelayanan (Rp)'))
fig.add_trace(go.Scatter(x=Kompensasi_Jasa_pred['Date'],y=Kompensasi_Jasa_pred['0'], mode='lines', name='KJP Pred With MLR'))
fig.add_trace(go.Scatter(x=Kompensasi_Jasa_pred_with_randomforest['Date'],y=Kompensasi_Jasa_pred_with_randomforest['0'], mode='lines', name='KJP Pred With RF'))
fig.add_trace(go.Scatter(x=Kompensasi_Jasa_pred_with_xgb['Date'],y=Kompensasi_Jasa_pred_with_xgb['0'], mode='lines', name='KJP Pred With XGB'))
fig.update_layout(
    title='Time Plot Kompensasi Jasa Pelayanan (Rp) 2017-2021',
    xaxis=dict(title='Time'),
    yaxis=dict(title='Kompensasi Jasa Pelayanan (Rp)'),
    autosize=False,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    )
)
st.plotly_chart(fig)

fig = go.Figure(data=[
    go.Bar(x=data_eval_test.index, y=data_eval_test['MAE'], marker_color='blue')
])
fig.update_layout(
    title='Plot MAE for Different Models',
    xaxis=dict(title='Model'),
    yaxis=dict(title='MAE'),
)
st.plotly_chart(fig)
with st.expander('Keterangan'):
    st.write("MAE (Mean Absolute Error):")
    st.write("- Semakin kecil nilainya, semakin baik. MAE mengukur rata-rata dari selisih absolut antara prediksi dan nilai sebenarnya.")
    st.write("- Nilai yang lebih kecil menunjukkan bahwa model memiliki kesalahan prediksi yang lebih rendah.")
    
fig = go.Figure(data=[
    go.Bar(x=data_eval_test.index, y=data_eval_test['MSE'], marker_color='blue')
])
fig.update_layout(
    title='Plot MSE for Different Models',
    xaxis=dict(title='Model'),
    yaxis=dict(title='MSE'),
)
st.plotly_chart(fig)
with st.expander('Keterangan'):
    st.write("MSE (Mean Squared Error):")
    st.write("- Semakin kecil nilainya, semakin baik. MSE mengukur rata-rata dari kuadrat dari selisih antara prediksi dan nilai sebenarnya.")
    st.write("- Seperti MAE, nilai yang lebih kecil menunjukkan bahwa model memiliki kesalahan prediksi yang lebih rendah.")
    
fig = go.Figure(data=[
    go.Bar(x=data_eval_test.index, y=data_eval_test['MAPE'], marker_color='blue')
])
fig.update_layout(
    title='Plot MAPE for Different Models',
    xaxis=dict(title='Model'),
    yaxis=dict(title='MAPE'),
)
st.plotly_chart(fig)
with st.expander('Keterangan'):
    st.write("MAPE (Mean Absolute Percentage Error):")
    st.write("- Semakin kecil nilainya, semakin baik. MAPE mengukur persentase rata-rata dari selisih absolut antara prediksi dan nilai sebenarnya.")
    st.write("- Nilai yang lebih kecil menunjukkan bahwa model memberikan prediksi dalam batas persentase kesalahan yang lebih rendah.")
    
fig = go.Figure(data=[
    go.Bar(x=data_eval_test.index, y=data_eval_test['R squared'], marker_color='blue')
])
fig.update_layout(
    title='Plot R squared for Different Models',
    xaxis=dict(title='Model'),
    yaxis=dict(title='R squared'),
)
st.plotly_chart(fig)
with st.expander('Keterangan'):
    st.write("R squared (R^2)")
    st.write("- Semakin besar nilainya, semakin baik. R^2 mengukur seberapa baik variabilitas dalam variabel dependen dapat dijelaskan oleh model.")
    st.write("- Nilai yang lebih besar, mendekati 1, menunjukkan bahwa model dapat menjelaskan variasi yang lebih besar dalam data.")

fig = go.Figure(data=[
    go.Bar(x=data_eval_test.index, y=data_eval_test['RMSE'], marker_color='blue')
])
fig.update_layout(
    title='Plot RMSE for Different Models',
    xaxis=dict(title='Model'),
    yaxis=dict(title='RMSE'),
)
st.plotly_chart(fig)
with st.expander('Keterangan'):
    st.write("RMSE (Root Mean Squared Error):")
    st.write("- Semakin kecil nilainya, semakin baik. RMSE adalah akar kuadrat dari MSE dan memberikan bobot lebih pada kesalahan yang besar.")
    st.write("- Nilai yang lebih kecil menunjukkan bahwa model memiliki kesalahan prediksi yang lebih rendah.")

st.header("Kesimpulan:")
st.markdown("Berdasarkan nilai-nilai metrics, model regresi linear berganda atau Multiple Linear Regression (MLR) memiliki kinerja terbaik dengan MAE, MSE, MAPE, R^2, RMSE yang lebih baik daripada model Random Forest dan XGBoost, dilihat dari data evaluasi prediksinya.")

mlr_test_results = """
- MAE: 7.27e+06
- MSE: 1.22e+14
- MAPE: 0.004024
- R^2: 0.990513
- RMSE: 1.11e+07
"""

st.markdown("Test MLR:" + mlr_test_results)

st.header("Penjelasan model MLR dalam memprediksi Kompensasi Jasa Pelayanan (Rp) menggunakan SHAP")
shap_train = "dashboard/pages/shap_train_mlr.png"
shap_test = "dashboard/pages/shap_test_mlr.png"
st.image(shap_train, caption='Ringkasan Nilai SHAP untuk Interpretasi model MLR pada Data Train', use_column_width=True)
st.image(shap_test, caption='Ringkasan Nilai SHAP untuk Interpretasi model MLR pada Data Test', use_column_width=True)
st.markdown("Fitur penting yang memiliki nilai rata-rata SHAP terbesar pada metode Regresi Linier Berganda (MLR) Baik pada Data Train dan Data Test pada variabel Kompensasi Jasa Pelayanan (Rp) adalah **Tonase (Ton) Sampah**.")
st.markdown("Semakin tinggi nilai pada variabel Tonase (Ton), memiliki kontribusi positif yang tinggi terhadap prediksi, sementara nilai yang rendah memiliki kontribusi negatif yang tinggi.")
st.markdown("Untuk Notebook bisa dilihat disini [KLIK DISINI](https://github.com/tirtaagungjati/olahsampah/blob/main/model_ml.ipynb)")
st.caption("Copyright "+ str(datetime.date.today().year) + " " + "[Tirta Agung Jati](https://www.linkedin.com/in/tirta-agung-jati 'Tirta Agung Jati | LinkedIn')")