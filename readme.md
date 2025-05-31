# Laporan Proyek Machine Learning - Rizky Maulana Saputra

## Project Overview

Dalam era digital, industri game mengalami pertumbuhan pesat dengan ribuan judul yang tersedia di berbagai platform. Tantangan utama bagi pengguna adalah menemukan game yang sesuai dengan preferensi mereka di tengah lautan pilihan tersebut. Sistem rekomendasi dapat menjadi solusi yang efektif untuk menyaring informasi dan memberikan rekomendasi personalisasi kepada pengguna.

Masalah ini penting untuk diselesaikan karena dapat meningkatkan pengalaman pengguna dan meningkatkan loyalitas terhadap platform distribusi game

## Business Understanding

### Problem Statements

Menjelaskan pernyataan masalah:
- Bagaimana memberikan rekomendasi game yang relevan berdasarkan deskripsi konten game?
- Bagaimana meningkatkan akurasi rekomendasi menggunakan pendekatan content-based filtering?

### Goals

Menjelaskan tujuan proyek yang menjawab pernyataan masalah:
- Membangun sistem rekomendasi berbasis content-based filtering menggunakan TF-IDF dan cosine similarity.
- Memberikan 10 rekomendasi game paling relevan berdasarkan input judul game.

### Solution statements
- Menggunakan metode TF-IDF untuk ekstraksi fitur dari deskripsi teks.
- Menggunakan cosine similarity untuk mengukur kemiripan antar game berdasarkan vektor TF-IDF.
- Menyimpan hasil perhitungan similarity untuk menghasilkan top-N recommendation.

## Data Understanding
Dataset yang digunakan merupakan dataset dari Steam Video Game Dataset yang tersedia secara publik melalui Kaggle: https://www.kaggle.com/datasets/nikdavis/steam-store-games.

Dataset ini terdiri dari 27.075 entri game dengan beberapa fitur utama:
- appid: ID unik dari setiap game
- name: Nama dari game
- release_date: Tanggal rilis
- english : Menandakan apakah game tersebut support bahasa inggris
- developer: Developer game
- publisher: Publisher game
- platforms : Platform yang support untuk memainkan game
- required_age : Batas umur untuk memainkan game
- categories: Kategori fitur seperti Multiplayer, Singleplayer, VR, dll
- genres: Genre game (Action, Indie, RPG, dll)
- steamspy_tags: Tag yang diberikan pengguna
- rating: Rating rata-rata (jika tersedia)
- achievements : 
- positive_ratings : Jumlah rating positive dari game
- negative_ratings : Jumlah rating negative dari game
- average_playtime : Rata rata playtime dari game
- median_playtime : Nilai tengah atau Median dari game
- owners : User yang memilki game
- price : Harga dari game dalam bentuk USD



## Data Preparation
Pada bagian ini Anda menerapkan dan menyebutkan teknik data preparation yang dilakukan. Teknik yang digunakan pada notebook dan laporan harus berurutan.


## Modeling
Tahapan ini membahas mengenai model sisten rekomendasi yang Anda buat untuk menyelesaikan permasalahan. Sajikan top-N recommendation sebagai output.


## Evaluation
Pada bagian ini Anda perlu menyebutkan metrik evaluasi yang digunakan. Kemudian, jelaskan hasil proyek berdasarkan metrik evaluasi tersebut.

Ingatlah, metrik evaluasi yang digunakan harus sesuai dengan konteks data, problem statement, dan solusi yang diinginkan.


**---Ini adalah bagian akhir laporan---**
