import streamlit as st
import pandas as pd

# Load data
data = pd.read_csv('Dataset_APBN_2023.csv')

# Sidebar
st.sidebar.title("Filter Data")
selected_province = st.sidebar.selectbox("Pilih Provinsi", data['PROVINSI'].unique())
analysis_date = st.sidebar.date_input("Pilih Tanggal Analisis")

# Main Layout
st.title("Dashboard APBN 2023")
st.write(f"Analisis data untuk provinsi: **{selected_province}** pada tanggal **{analysis_date}**")

# Filter data berdasarkan provinsi
province_data = data[data['PROVINSI'] == selected_province]

# Tabs
tab1, tab2, tab3 = st.tabs(["Ringkasan", "Analisis Pendidikan", "Input Data"])

# Tab 1: Ringkasan
with tab1:
    st.header("Statistik Ringkasan")
    total_schools = province_data.iloc[:, 3:19:4].sum().sum()  # Jumlah total sekolah
    total_students = province_data.iloc[:, 4:19:4].sum().sum()  # Jumlah total murid
    total_budget = province_data['PAGU'].sum()

    st.metric("Total Sekolah", total_schools)
    st.metric("Total Murid", total_students)
    st.metric("Total Anggaran", f"Rp {total_budget:,}")

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
    jenjang_data = province_data[jenjang_columns[jenjang]]
    st.bar_chart(jenjang_data.sum())

# Tab 3: Input Data
with tab3:
    st.header("Input Data Baru")
    
    # Radio button untuk memilih jenjang pendidikan
    school_level = st.radio("Pilih Tingkatan Sekolah", ["SD", "SMP", "SMA", "SMK"])
    
    # Input untuk jumlah murid, tingkat dropout
    additional_students = st.number_input("Tambahkan Jumlah Murid", min_value=0, step=1)
    additional_dropout = st.number_input("Tambahkan Tingkat Dropout", min_value=0, step=1)
    
    if st.button("Simpan Data"):
        # Pilih kolom yang relevan berdasarkan jenjang pendidikan
        level_columns = {
            "SD": ("Jumlah Murid SD", "Dropout SD"),
            "SMP": ("Jumlah Murid SMP", "Dropout SMP"),
            "SMA": ("Jumlah Murid SMA", "Dropout SMA"),
            "SMK": ("Jumlah Murid SMK", "Dropout SMK"),
        }
        
        # Dapatkan nama kolom yang sesuai
        student_col, dropout_col = level_columns[school_level]
        
        # Update data untuk provinsi yang dipilih
        data.loc[data['PROVINSI'] == selected_province, student_col] += additional_students
        data.loc[data['PROVINSI'] == selected_province, dropout_col] += additional_dropout
        
        # Simpan kembali ke file CSV
        data.to_csv('Dataset_APBN_2023.csv', index=False)
        
        # Feedback ke pengguna
        st.success(f"Data berhasil diperbarui untuk jenjang {school_level}!")
        st.write(f"Provinsi: {selected_province}, {student_col} +{additional_students}, {dropout_col} +{additional_dropout}")



# Expander for details
with st.expander("Detail Provinsi"):
    st.write(province_data)
