# Data-Analytic

Aplikasi ini memungkinkan pengguna untuk melakukan Analisis Pengaruh Anggaran APBN Di Sektor Pendidikan Terhadap Angka Putus Sekolah. Aplikasi ini dibuat menggunakan **Streamlit** dan **Plotly** untuk visualisasi data.

## Fitur Utama
- **Filter Provinsi**: Pengguna dapat memilih provinsi yang ingin dianalisis melalui sidebar.
- **Analisis Dropout**: Menampilkan statistik dropout untuk jenjang pendidikan tertentu dan rasio dropout terhadap jumlah murid.
- **Visualisasi**: Menyediakan visualisasi data menggunakan grafik batang dan donut chart untuk memberikan gambaran yang jelas mengenai rasio dropout.

## Cara Penggunaan

### 1. Instalasi
Pastikan Python sudah terinstal di perangkat Anda. Jika belum, Anda bisa mengunduhnya di [python.org](https://www.python.org/downloads/).

1. Clone repository ini atau unduh file kode.
2. Install semua dependensi yang dibutuhkan dengan perintah berikut di terminal atau command prompt:

    ```bash
    pip install -r requirements.txt
    ```

3. Jalankan aplikasi menggunakan perintah:

    ```bash
    streamlit run data.py
    ```

    Setelah itu, aplikasi akan berjalan di browser Anda.

### 2. Menggunakan Filter Provinsi
Pada sidebar, Anda akan menemukan opsi untuk memilih provinsi yang ingin dianalisis.

1. **Pilih Provinsi**: Anda bisa memilih satu atau lebih provinsi yang diinginkan untuk analisis. Gunakan fitur **multiselect** untuk memilih provinsi yang sesuai.
2. **Tanggal Analisis**: Tanggal analisis akan otomatis ditampilkan sesuai dengan hari Anda membuka aplikasi.

Setelah memilih provinsi, aplikasi akan menampilkan data terkait provinsi yang dipilih beserta statistik terkait.

### 3. Analisis Data Dropout
Pada bagian utama aplikasi, Anda akan melihat statistik dropout yang terkait dengan jenjang pendidikan. Aplikasi ini menghitung dan menampilkan:

- **Grafik Bar** yang menunjukkan jumlah dropout berdasarkan jenjang.
- **Donut Chart** yang menampilkan rasio dropout terhadap total jumlah murid dalam bentuk grafik donat, dengan persentase yang dihitung secara otomatis.

### 4. Tampilan Visualisasi
Di bagian visualisasi, Anda dapat melihat grafik yang interaktif. Pengguna dapat memanfaatkan grafik ini untuk memahami sebaran data dropout dan rasio dropout dengan lebih mudah.

## Teknologi yang Digunakan
- **Streamlit**: Untuk membangun aplikasi web interaktif.
- **Plotly**: Untuk visualisasi grafik donut chart.
- **Pandas**: Untuk manipulasi data.
- **Altair**: Untuk grafik tambahan (misalnya donut chart alternatif).
  
## Kontribusi
Jika Anda ingin berkontribusi pada proyek ini, silakan lakukan langkah-langkah berikut:

1. Fork repository ini.
2. Buat branch baru untuk fitur atau perbaikan yang Anda kerjakan.
3. Setelah selesai, kirimkan pull request untuk diskusi lebih lanjut.

## Lisensi
Proyek ini dilisensikan di bawah lisensi MIT. Lihat file [LICENSE](LICENSE) untuk informasi lebih lanjut.
