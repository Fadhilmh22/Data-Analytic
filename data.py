import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import date
import matplotlib.pyplot as plt
import altair as alt


def display_map(df):
    jenjang_options = ['SD', 'SMP', 'SMA', 'SMK']
    selected_jenjang = st.selectbox(
        "Pilih Jenjang Pendidikan:", jenjang_options)

    jumlah_sekolah_column = f"Jumlah Sekolah {selected_jenjang}"

    if jumlah_sekolah_column not in df.columns:
        st.error(f"Data untuk jenjang {selected_jenjang} tidak tersedia.")
        return ""

    map = folium.Map(location=[-6.1751, 106.8650], zoom_start=5,
                     scrollWheelZoom=False, tiles='CartoDB positron')

    geojson_url = 'indonesia-edit.geojson'
    df['PROVINSI'] = df['PROVINSI'].str.upper()

    choropleth = folium.Choropleth(
        geo_data=geojson_url,
        data=df,
        columns=['PROVINSI', jumlah_sekolah_column],
        key_on='feature.properties.state',
        fill_color='YlOrRd',  
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"Jumlah Sekolah {selected_jenjang}"
    )
    choropleth.geojson.add_to(map)

    df_indexed = df.set_index('PROVINSI')

    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['state'].upper()
        if state_name in df_indexed.index:
            jumlah_sekolah = df_indexed.loc[state_name, jumlah_sekolah_column]
            feature['properties']['population'] = f"Jumlah Sekolah {selected_jenjang}: {jumlah_sekolah}"

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['state', 'population'], labels=False)
    )

    st_map = st_folium(map, width=700, height=450)

    state_name = ''
    if st_map.get('last_active_drawing'):
        state_name = st_map['last_active_drawing']['properties']['state']

    return state_name

# Load data
data = pd.read_csv('Dataset_APBN_2023.csv')

# Slide awal
st.markdown("""
<div style="
    background-color: #e6f7ff; 
    padding: 30px; 
    border-radius: 15px; 
    margin-bottom: 50px; 
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);">    
    <h1 style="color: #00509e; text-align: center; font-size: 2.5rem; font-family: 'Comic Sans ms', sans-serif; margin-bottom: 10px;">
        Dashboard Analisis Pengaruh Anggaran APBN <br> Di Sektor Pendidikan Terhadap Angka Putus Sekolah
    </h1>
    <h2 style="text-align: center; color: #007acc; font-family: 'Comic Sans ms', sans-serif; margin-bottom: 30px;">
        Kelompok 2
    </h2>
    <ul style="list-style: none; padding: 0; margin: 0; font-size: 1.2rem; color: #003f7d; font-family: 'Comic Sans ms', sans-serif; line-height: 2;">
        <li><b>Amelda Nur Azzuhra</b> (210414013)</li>
        <li><b>Haykal Hudiya Abiyyu</b> (210414020)</li>
        <li><b>Fadhiil Mursyid Habibi</b> (210414021)</li>
        <li><b>Bella Syifa Anandita Suherlan</b> (210414024)</li>
    </ul>
</div>
""", unsafe_allow_html=True)

state_name = display_map(data)
st.write(f'Provinsi yang dipilih: {state_name}')

from datetime import date
import streamlit as st

# Sidebar
st.sidebar.image("school.png", width=250)
st.sidebar.title("Filter Data")

# Menambahkan instruksi di sidebar
st.sidebar.markdown(
    "Pilih provinsi yang ingin Anda analisis dari dropdown list di bawah ini. Anda dapat memilih satu atau beberapa provinsi untuk melihat data yang relevan."
)

# Multiselect untuk memilih provinsi
selected_provinces = st.sidebar.multiselect(
    "Pilih Provinsi", data['PROVINSI'].unique(), default=data['PROVINSI'].unique()[:1])

# Menampilkan tanggal analisis
analysis_date = date.today()
st.sidebar.write(f"**Tanggal Analisis:** {analysis_date.strftime('%d-%m-%Y')}")

if selected_provinces:
    st.write(
        f"Analisis data untuk provinsi: **{', '.join(selected_provinces)}** pada tanggal **{analysis_date.strftime('%d-%m-%Y')}**")

# Filter data berdasarkan provinsi yang dipilih
filtered_data = data[data['PROVINSI'].isin(selected_provinces)]


tab1, tab2, tab3 = st.tabs(["Ringkasan", "Analisis Pendidikan", "Input Data"])

# Tab 1: Ringkasan
with tab1:
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
    total_schools = int(filtered_data.iloc[:, 3:19:4].sum().sum())
    total_students = int(filtered_data.iloc[:, 4:19:4].sum().sum())
    total_budget = int(filtered_data['PAGU'].sum()) 

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
        school_data = pd.DataFrame(
            {"Jenjang": school_levels, "Jumlah Sekolah": school_counts})
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
        student_data = pd.DataFrame(
            {"Jenjang": school_levels, "Jumlah Murid": student_counts})
        st.bar_chart(student_data.set_index("Jenjang"))

        st.empty()

#         # Original Data (Semua Data Tanpa Filter)
#         original_data = data.copy()

#        # Memisahkan grafik Pagu ke bagian lain, di luar kolom
# st.subheader("Pagu APBN 2023 per Provinsi")

# # DataFrame Total Pagu
# total_pagu_chart = pd.DataFrame({
#     'Provinsi': original_data['PROVINSI'],
#     'PAGU (Triliun)': original_data['PAGU'] / 1e12  # Konversi ke triliun
# })

# # Sort berdasarkan PAGU
# total_pagu_chart = total_pagu_chart.sort_values(
#     by="PAGU (Triliun)", ascending=True)

# # Bar Chart menggunakan Altair
# chart = alt.Chart(total_pagu_chart).mark_bar(color='#78B3CE').encode(
#     x=alt.X('PAGU (Triliun):Q', title='PAGU (Triliun)',
#             axis=alt.Axis(tickMinStep=5)),  # Sumbu X
#     y=alt.Y('Provinsi:N', sort='-x', title='Provinsi'),  # Sumbu Y
#     tooltip=['Provinsi', 'PAGU (Triliun)']  # Tooltip interaktif
# ).properties(
#     width=800,  # Lebar chart
#     height=600  # Tinggi chart
# ).configure_axis(
#     grid=True,
#     labelFontSize=12,
#     titleFontSize=14
# ).configure_title(
#     fontSize=16,
#     anchor='start',
#     fontWeight='bold'
# )

# # Tampilkan Chart
# st.altair_chart(chart, use_container_width=True)


# Tab 2: Analisis Per Jenjang Pendidikan
with tab2:
    st.header("Analisis Pendidikan Per Jenjang")
    jenjang = st.selectbox("Pilih Jenjang", ["SD", "SMP", "SMA", "SMK"])
    st.write(f"Statistik untuk {jenjang}:")

    jenjang_columns = {
        "SD": ["Jumlah Sekolah SD", "Jumlah Kuota Murid SD", "Jumlah Murid SD", "Dropout SD"],
        "SMP": ["Jumlah Sekolah SMP", "Jumlah Kuota Murid SMP", "Jumlah Murid SMP", "Dropout SMP"],
        "SMA": ["Jumlah Sekolah SMA", "Jumlah Kuota Murid SMA", "Jumlah Murid SMA", "Dropout SMA"],
        "SMK": ["Jumlah Sekolah SMK", "Jumlah Kuota Murid SMK", "Jumlah Murid SMK", "Dropout SMK"],
    }
    jenjang_data = filtered_data[jenjang_columns[jenjang]]

    st.bar_chart(jenjang_data.drop(columns=[
                 "Dropout SD", "Dropout SMP", "Dropout SMA", "Dropout SMK"], errors='ignore').sum())

    st.write("Statistik Dropout")
    dropout_column = f"Dropout {jenjang}"
    if dropout_column in jenjang_data.columns:
        dropout_data = jenjang_data[dropout_column]
        st.bar_chart(dropout_data, height=300)
    else:
        st.warning("Data dropout tidak ditemukan untuk jenjang ini.")

    st.write("Rasio Dropout terhadap Total Murid")
    if dropout_column in jenjang_data.columns:
        total_students_jenjang = jenjang_data[f"Jumlah Murid {jenjang}"].sum()
        total_dropout_jenjang = jenjang_data[dropout_column].sum()

        dropout_percentage = (total_dropout_jenjang / total_students_jenjang) * \
            100 if total_students_jenjang > 0 else 0

        labels = ["Dropout"]
        values = [total_dropout_jenjang]

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.7,  
            marker=dict(colors=["red"]),  
            textinfo='none'  
        )])

        fig.update_layout(
            annotations=[dict(
                text=f"{dropout_percentage:.2f}%",
                x=0.5,
                y=0.5,
                font_size=20,
                showarrow=False,
                font=dict(
                    family="Comic Sans MS",  
                    size=20,  
                    color="red",  
                    style="italic" 
                )
            )],
            showlegend=False 
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Data dropout tidak tersedia untuk jenjang ini.")


# Tab 3: Input Data
with tab3:
    st.header("Input Data Baru")

    school_level = st.radio("Pilih Tingkatan Sekolah", [
                            "SD", "SMP", "SMA", "SMK"])

    additional_students = st.number_input(
        "Tambahkan Jumlah Murid", min_value=0, step=1)
    additional_dropout = st.number_input(
        "Tambahkan Tingkat Dropout", min_value=0, step=1)

    if st.button("Simpan Data"):
        level_columns = {
            "SD": ("Jumlah Murid SD", "Dropout SD"),
            "SMP": ("Jumlah Murid SMP", "Dropout SMP"),
            "SMA": ("Jumlah Murid SMA", "Dropout SMA"),
            "SMK": ("Jumlah Murid SMK", "Dropout SMK"),
        }
        student_col, dropout_col = level_columns[school_level]
        for province in selected_provinces:
            data.loc[data['PROVINSI'] == province,
                     student_col] += additional_students
            data.loc[data['PROVINSI'] == province,
                     dropout_col] += additional_dropout

        data.to_csv('Dataset_APBN_2023.csv', index=False)
        st.success(
            f"Data berhasil diperbarui untuk jenjang {school_level}! Ditambahkan pada provinsi: {', '.join(selected_provinces)}")
        st.write(
            f"{student_col} +{additional_students}, {dropout_col} +{additional_dropout}")

# Expander for details
with st.expander("Detail Provinsi"):
    filtered_data.index.name = "Index"

    st.write(filtered_data)
