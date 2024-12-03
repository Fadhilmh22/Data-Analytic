import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import json
import folium
from streamlit_folium import st_folium
from babel.numbers import format_currency
from datetime import date


def display_map(df):
    # Menambahkan dropdown untuk memilih jenjang pendidikan
    jenjang_options = ['SD', 'SMP', 'SMA', 'SMK']
    selected_jenjang = st.selectbox("Pilih Jenjang Pendidikan:", jenjang_options)
    
    # Kolom yang relevan berdasarkan jenjang yang dipilih
    jumlah_sekolah_column = f"Jumlah Sekolah {selected_jenjang}"
    
    if jumlah_sekolah_column not in df.columns:
        st.error(f"Data untuk jenjang {selected_jenjang} tidak tersedia.")
        return ""
    
    # Membuat peta dengan pusat Indonesia
    map = folium.Map(location=[-6.1751, 106.8650], zoom_start=5, scrollWheelZoom=False, tiles='CartoDB positron')
    
    # Membaca GeoJSON dari file lokal
    geojson_url = 'indonesia-edit.geojson'
    df['PROVINSI'] = df['PROVINSI'].str.upper()

    # Membuat Choropleth Map untuk peta Indonesia
    choropleth = folium.Choropleth(
        geo_data=geojson_url,
        data=df,
        columns=['PROVINSI', jumlah_sekolah_column],
        key_on='feature.properties.state',
        fill_color='YlOrRd',  # Ganti dengan palet warna lain
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"Jumlah Sekolah {selected_jenjang}"
    )
    choropleth.geojson.add_to(map)

    # Menambahkan informasi tambahan pada setiap provinsi di GeoJSON
    df_indexed = df.set_index('PROVINSI')  # Indeks menggunakan 'PROVINSI' untuk pencocokan
    
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['state'].upper()  # Nama provinsi di GeoJSON
        if state_name in df_indexed.index:
            jumlah_sekolah = df_indexed.loc[state_name, jumlah_sekolah_column]
            feature['properties']['population'] = f"Jumlah Sekolah {selected_jenjang}: {jumlah_sekolah}"

    # Menambahkan tooltip pada GeoJSON untuk menampilkan informasi yang relevan
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['state', 'population'], labels=False)  # Menggunakan 'state' dan 'population' sebagai tooltip
    )

    # Menampilkan peta di Streamlit
    st_map = st_folium(map, width=700, height=450)

    # Menangani interaksi dengan peta, seperti klik pada provinsi
    state_name = ''
    if st_map.get('last_active_drawing'):
        state_name = st_map['last_active_drawing']['properties']['state']
    
    return state_name


# Load data
data = pd.read_csv('Dataset_APBN_2023.csv')




# Slide awal
st.markdown("""
<div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-botton: 100px;">
    <h1 style="color: #3333cc; text-align: center;">Dashboard Analisis Pengaruh Anggaran APBN Di Sektor Pendidikan Terhadap Angka Putus Sekolah Di Setiap Provinsi</h1>
    <h2 style="text-align: center; color: #444;">Kelompok 3</h2>
    <ul style="list-style: none; text-align: center; padding: 0; color: #333;">
        <li><b>Amelda Nur Azzuhra</b> (210414013)</li>
        <li><b>Haykal Hudiya Abiyyu</b> (210414020)</li>
        <li><b>Fadhiil Mursyid Habibi</b> (210414021)</li>
        <li><b>Bella Syifa Anandita Suherlan</b> (210414024)</li>
    </ul>
</div>
""", unsafe_allow_html=True)



state_name = display_map(data)
st.write(f'Provinsi yang dipilih: {state_name}')

# Sidebar
st.sidebar.image("school.png", width=250)  # Menampilkan logo dengan lebar 100px
st.sidebar.title("Filter Data")
selected_provinces = st.sidebar.multiselect("Pilih Provinsi", data['PROVINSI'].unique(), default=data['PROVINSI'].unique()[:5])
analysis_date = date.today()

# Menampilkan tanggal sebagai teks di sidebar
st.sidebar.write(f"**Tanggal Analisis:** {analysis_date.strftime('%d-%m-%Y')}")

if selected_provinces:
    st.write(f"Analisis data untuk provinsi: **{', '.join(selected_provinces)}** pada tanggal **{analysis_date.strftime('%d-%m-%Y')}**")

# Filter data berdasarkan provinsi yang dipilih
filtered_data = data[data['PROVINSI'].isin(selected_provinces)]

# Tabs
tab1, tab2, tab3 = st.tabs(["Ringkasan", "Analisis Pendidikan", "Input Data"])

# Tab 1: Ringkasan
with tab1:
    # Gaya CSS untuk membuat layout horizontal
    st.markdown("""
    <style>
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
    }
    .metric-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 30%;
    }
    .metric-title {
        font-size: 18px;
        color: #333;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #3333cc;
    }
    </style>
    """, unsafe_allow_html=True)

    

    # Data Ringkasan
    total_schools = int(filtered_data.iloc[:, 3:19:4].sum().sum())  # Jumlah total sekolah
    total_students = int(filtered_data.iloc[:, 4:19:4].sum().sum())  # Jumlah total murid
    total_budget = int(filtered_data['PAGU'].sum())  # Total anggaran

    # Layout Ringkasan
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-box">
            <div class="metric-title">Total Sekolah</div>
            <div class="metric-value" style="font-size: 15px; color: #3333cc;">{total_schools}</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">Total Murid</div>
            <div class="metric-value" style="font-size: 15px; color: #3333cc;">{total_students}</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">Total Anggaran</div>
            <div class="metric-value" style="font-size: 15px; color: #3333cc;">Rp {total_budget:,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Diagram Tambahan
    col1, col2 = st.columns(2)

    # Diagram 1: Sekolah per Jenjang
    with col1:
        st.subheader("Jumlah Sekolah setiap Jenjang")
        school_levels = ["SD", "SMP", "SMA", "SMK"]
        school_counts = [
            filtered_data["Jumlah Sekolah SD"].sum(),
            filtered_data["Jumlah Sekolah SMP"].sum(),
            filtered_data["Jumlah Sekolah SMA"].sum(),
            filtered_data["Jumlah Sekolah SMK"].sum(),
        ]
        school_data = pd.DataFrame({"Jenjang": school_levels, "Jumlah Sekolah": school_counts})
        st.bar_chart(school_data.set_index("Jenjang"))

        st.empty()


    # Diagram 2: Murid per Jenjang
    with col2:
        st.subheader("Jumlah Murid setiap Jenjang")
        student_counts = [
            filtered_data["Jumlah Murid SD"].sum(),
            filtered_data["Jumlah Murid SMP"].sum(),
            filtered_data["Jumlah Murid SMA"].sum(),
            filtered_data["Jumlah Murid SMK"].sum(),
        ]
        student_data = pd.DataFrame({"Jenjang": school_levels, "Jumlah Murid": student_counts})
        st.bar_chart(student_data.set_index("Jenjang"))

        st.empty()



# Tab 2: Analisis Per Jenjang Pendidikan
with tab2:
    st.header("Analisis Pendidikan Per Jenjang")
    jenjang = st.selectbox("Pilih Jenjang", ["SD", "SMP", "SMA", "SMK"])
    st.write(f"Statistik untuk {jenjang}:")
    
    # Menampilkan data jenjang yang dipilih
    jenjang_columns = {
        "SD": ["Jumlah Sekolah SD", "Jumlah Kuota Murid SD", "Jumlah Murid SD", "Dropout SD"],
        "SMP": ["Jumlah Sekolah SMP", "Jumlah Kuota Murid SMP", "Jumlah Murid SMP", "Dropout SMP"],
        "SMA": ["Jumlah Sekolah SMA", "Jumlah Kuota Murid SMA", "Jumlah Murid SMA", "Dropout SMA"],
        "SMK": ["Jumlah Sekolah SMK", "Jumlah Kuota Murid SMK", "Jumlah Murid SMK", "Dropout SMK"],
    }
    jenjang_data = filtered_data[jenjang_columns[jenjang]]
    
    # Grafik gabungan untuk semua data kecuali dropout
    st.bar_chart(jenjang_data.drop(columns=["Dropout SD", "Dropout SMP", "Dropout SMA", "Dropout SMK"], errors='ignore').sum())
    
    # Tambahkan visualisasi terpisah untuk Dropout
    st.write("Statistik Dropout")
    dropout_column = f"Dropout {jenjang}"
    if dropout_column in jenjang_data.columns:
        dropout_data = jenjang_data[dropout_column]
        st.bar_chart(dropout_data, height=300)
        st.caption(f"Grafik dropout untuk jenjang {jenjang}. (Data terlihat lebih jelas di diagram ini)")
    else:
        st.warning("Data dropout tidak ditemukan untuk jenjang ini.")

    # Menampilkan Donut Chart untuk Dropout
    st.write("Rasio Dropout terhadap Total Murid")
    if dropout_column in jenjang_data.columns:
        total_students_jenjang = jenjang_data[f"Jumlah Murid {jenjang}"].sum()
        total_dropout_jenjang = jenjang_data[dropout_column].sum()
        
        # Hitung persentase dropout
        dropout_percentage = (total_dropout_jenjang / total_students_jenjang) * 100 if total_students_jenjang > 0 else 0

        # Data untuk Donut Chart hanya menunjukkan Dropout
        labels = ["Dropout"]
        values = [total_dropout_jenjang]

        # Membuat Donut Chart dengan Plotly
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.7,  # Untuk menciptakan efek Donut
            marker=dict(colors=["red"]),  # Warna Dropout merah
            textinfo='none'  # Menghilangkan teks default (100%) pada chart
        )])

        # Tambahkan teks di tengah donut
        fig.update_layout(
            annotations=[dict(
                text=f"{dropout_percentage:.2f}%",  # Menampilkan persen dropout
                x=0.5, 
                y=0.5, 
                font_size=20, 
                showarrow=False, 
                font=dict(
                    family="Comic Sans MS",  # Mengubah font menjadi Comic Sans
                    size=20,  # Ukuran font
                    color="red",  # Warna font merah
                    style="italic"  # Membuat font miring
                )
            )],
            showlegend=False  # Sembunyikan legenda
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Data dropout tidak tersedia untuk jenjang ini.")


# Tab 3: Input Data
with tab3:
    st.header("Input Data Baru")
    
    # Radio button untuk memilih jenjang pendidikan
    school_level = st.radio("Pilih Tingkatan Sekolah", ["SD", "SMP", "SMA", "SMK"])
    
    # Input untuk jumlah murid, tingkat dropout
    additional_students = st.number_input("Tambahkan Jumlah Murid", min_value=0, step=1)
    additional_dropout = st.number_input("Tambahkan Tingkat Dropout", min_value=0, step=1)
    
    if st.button("Simpan Data"):
        level_columns = {
            "SD": ("Jumlah Murid SD", "Dropout SD"),
            "SMP": ("Jumlah Murid SMP", "Dropout SMP"),
            "SMA": ("Jumlah Murid SMA", "Dropout SMA"),
            "SMK": ("Jumlah Murid SMK", "Dropout SMK"),
        }
        student_col, dropout_col = level_columns[school_level]
        for province in selected_provinces:
            data.loc[data['PROVINSI'] == province, student_col] += additional_students
            data.loc[data['PROVINSI'] == province, dropout_col] += additional_dropout
        
        data.to_csv('Dataset_APBN_2023.csv', index=False)
        st.success(f"Data berhasil diperbarui untuk jenjang {school_level}! Ditambahkan pada provinsi: {', '.join(selected_provinces)}")
        st.write(f"{student_col} +{additional_students}, {dropout_col} +{additional_dropout}")

# Expander for details
with st.expander("Detail Provinsi"):
    # Mengganti nama index yang lama menjadi "Index"
    filtered_data.index.name = "Index"
    
    st.write(filtered_data)


