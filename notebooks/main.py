# %% [markdown]
# # **Recommendation System**

# %% [markdown]
# ## Business Understanding

# %% [markdown]
# ### Problem Statements

# %% [markdown]
# Menjelaskan pernyataan masalah:
# - Bagaimana memberikan rekomendasi game yang relevan berdasarkan deskripsi konten game?
# - Bagaimana meningkatkan akurasi rekomendasi menggunakan pendekatan content-based filtering?

# %% [markdown]
# ### Goals

# %% [markdown]
# Menjelaskan tujuan proyek yang menjawab pernyataan masalah:
# - Membangun sistem rekomendasi berbasis content-based filtering menggunakan TF-IDF dan cosine similarity.
# - Memberikan 10 rekomendasi game paling relevan berdasarkan input judul game.

# %% [markdown]
# ### Solution Statements

# %% [markdown]
# - Menggunakan metode TF-IDF untuk ekstraksi fitur dari deskripsi teks.
# - Menggunakan cosine similarity untuk mengukur kemiripan antar game berdasarkan vektor TF-IDF.
# - Menyimpan hasil perhitungan similarity untuk menghasilkan top-N recommendation.

# %% [markdown]
# - Import Library

# %%
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import  WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import  cosine_similarity


# %% [markdown]
# ## Data Understanding

# %% [markdown]
# Dataset yang digunakan diambil dari Kaggle - Steam Store Games
# Tautan Dataset:<br>
# Steam Store Games : https://www.kaggle.com/datasets/nikdavis/steam-store-games <br>
# 
# Dataset ini memiliki 27.075 baris dan 18 kolom data yang mempresentasikan
# 
# - appid : Id unik dari game
# - name : Nama dari game
# - release_date : Tanggal liris dari game
# - english : Menandakan apakah game tersebut support bahasa inggris
# - developer : Developer game
# - publisher : Publisher game
# - platforms : Platform yang support untuk memainkan game
# - required_age : Batas umur untuk memainkan game
# - categories : Kategore dari game seperti Multiplayer, Singleplayer, VR, dll
# - genres : Genre dari game (Action, Indie, RPG, dll)
# - steamspy_tags : Tag yang diberikan pengguna
# - achievements : 
# - positive_ratings : Rating Positive dari game
# - negative_ratings : Rating Negative dari game
# - average_playtime : Rata rata playtime dari game
# - median_playtime : Nilai tengah atau Median dari playtime game
# - owners : User yang memilki game
# - price : Harga dari game dalam bentuk USD
# 
# Kondisi Data :<br>
# - Missing Values : Dilakukan pada Exploration Data Analytics yakni terdapat missing values kolom developer (1) dan publisher (14)
# - Duplicate Data : Dilakukan pada Exploration Data Analytics yakni tidak terdapat duplikat data
# - Outlier : Dilakukan pada Exploration Data Analytics terlihat terdapat outlier di kolom :
#     - Kolom price : 1975 Outlier
#     - Kolom positive_ratings : 4286 Outlier
#     - Kolom negative_ratings : 3957 Outlier
#     - Kolom required_age : 596 Outlier
#     - Kolom achievements : 1695 Outlier 

# %% [markdown]
# - Load Data

# %%
df = pd.read_csv('../data/steam.csv')

# %% [markdown]
# ## Exploration Data Analysis

# %% [markdown]
# 1. Pemeriksaan Struktur Data, Missing Values dan Duplicate Data : <br>
# Dataset terdiri dari 27.075 baris dengan berbagai variabel seperti appid, name, release_date, english, developer, publisher, platforms, required_age, categories, genres, steamspy_tags, achievements, positive ratings, negtive ratings, average playtime, median playtime, owners, price. Hasil pengecekan menunjukkan bahwa terdapat missing values pada dataset tepatnya di kolom developer dan publisher

# %%
df.head()

# %%
df.dtypes

# %%
df.isna().sum()

# %%
df.duplicated().sum()

# %% [markdown]
# 2. Statistik Deskriptif : <br>
# 

# %%
df.describe()

# %% [markdown]
# 3. Cek Outlier

# %%
numeric = df[['price', 'positive_ratings', 
              'negative_ratings','required_age', 'achievements']]
def check_outlier(data):
    Q1 = df[data].quantile(0.25)
    Q3 = df[data].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outlier = df[(df[data] < lower) | (df[data]>upper)]
    print(f"Kolom {data} : {len(outlier)} Outlier")
for i in numeric:
    check_outlier(i)

# %% [markdown]
# 4. Visual

# %% [markdown]
# - Top 10 Genre Terpopuler<br>
# Insight: Genre seperti Action, Indie, dan Casual menjadi yang paling dominan dalam dataset game ini.

# %%
df['genres'].str.split(';').explode().value_counts().head(10).plot(kind='barh', color='lightblue')
plt.title("Top 10 Most Common Genres")
plt.xlabel("Jumlah")
plt.ylabel("Genre")
plt.gca().invert_yaxis()
plt.show()

# %% [markdown]
# - Distribusi Average Playtime<br>
# Insight: Sebagian besar game memiliki waktu main yang sangat rendah, dengan beberapa game yang sangat lama dimainkan (outlier).
# 
# 

# %%
sns.histplot(df['average_playtime'], bins=50, kde=True, color='orange')
plt.title("Distribusi Rata-rata Waktu Main")
plt.xlabel("Average Playtime (menit)")
plt.ylabel("Frekuensi")
plt.show()

# %% [markdown]
# - Boxplot Average Playtime<br>
# Insight: Outlier cukup ekstrem di sebelah kanan, mengindikasikan beberapa game dimainkan hingga ratusan ribu menit.

# %%
sns.boxplot(x=df['average_playtime'], color='lightgreen')
plt.title("Boxplot Rata-rata Waktu Main")
plt.xlabel("Average Playtime (menit)")
plt.show()

# %% [markdown]
# - WordCloud Genre<br>
#     Insight: Genre populer seperti Action, Adventure, dan Indie muncul dominan secara visual, memperkuat hasil pada analisis bar chart sebelumnya.

# %%
text = ' '.join(df['genres'].dropna().str.replace(';', ' '))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("WordCloud Genre")
plt.show()


# %% [markdown]
# - Jumlah Game Dirilis per Tahun<br>
# Insight: Terlihat adanya tren peningkatan jumlah game dari tahun ke tahun, terutama mulai tahun 2014-an. Namun, ada penurunan signifikan di beberapa tahun terakhir yang kemungkinan karena data belum lengkap.

# %%
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['release_year'] = df['release_date'].dt.year

df['release_year'].value_counts().sort_index().plot(kind='line', marker='o')
plt.title("Jumlah Game Dirilis per Tahun")
plt.xlabel("Tahun")
plt.ylabel("Jumlah Game")
plt.grid(True)
plt.show()


# %% [markdown]
# ## Data Preparation

# %% [markdown]
# 1. Handling Missing Values :<br>
# Seluruh baris yang memiliki data kosong dihapus menggunakan df.dropna() untuk menjaga konsistensi data

# %%
df = df.dropna()

# %% [markdown]
# 2. Menghapus kolom yang tidak relevan dan konversi tipe data :
#    - Kolom appid dihapus karena tidak memiliki kontribusi terhadap proses pemodelan
#    - Kolom numerik seperti achievements, positive_ratings, negative_ratings, average_playtime, median_playtime, price dikonversi ke tipe float agar dapat digunakan untuk analisis dan transformasi numerik

# %%
df = df.drop(columns=['appid'], axis=1)
df['achievements'] = df['achievements'].astype(float)
df['positive_ratings'] = df['positive_ratings'].astype(float)
df['negative_ratings'] = df['negative_ratings'].astype(float)
df['average_playtime'] = df['average_playtime'].astype(float)
df['median_playtime'] = df['median_playtime'].astype(float)
df['price'] = df['price'].astype(float)
df['combined'] = df['genres'].fillna('') + ' ' + df['developer'].fillna('')

# %% [markdown]
# 3. Handling Outlier<br>
# Untuk fitur numerik (price, positive_ratings, negative_ratings, required_age, achievements), dilakukan penanganan outlier menggunakan metode IQR. Nilai yang berada diluar rentang Q1-1.5xIQR dan Q3+1.5xIQR di cap ke batas tersebut.

# %%
numeric = df[['price', 'positive_ratings', 
              'negative_ratings', 'required_age', 'achievements']]
def outlier_handling(data):
    Q1 = df[data].quantile(0.25)
    Q3 = df[data].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df.loc[df[data] > upper, data] = upper
    df.loc[df[data] < lower, data] = lower

for i in numeric:
    outlier_handling(i)
    check_outlier(i)

# %% [markdown]
# 4. Vectorization dan Perhitungan Cosine Similarity :<br>
#    Data pada kolom combined di transformasi menjadi bentuk vektor menggunakan TF-IDF agar dapat dihitung kemiripan. Hasil dari TF-IDF digunakan untuk menghitung cosine similarity, yang menjadi dasar penilaian kemiripan antar game.

# %%
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# %% [markdown]
# ## Modelling

# %% [markdown]
# Pendekatan utama dalam proyek ini adalah Content-Based Filtering menggunakan teknik TF-IDF dan Cosine Similarity. Pendekatan ini fokus pada konten deskriptif dari game, seperti genre dan developer, untuk memberikan rekomendasi yang relevan.
# 
# Algoritma: TF-IDF + Cosine Similarity
# 1. TF-IDF (Term Frequency-Inverse Document Frequency) digunakan untuk mengubah teks dalam kolom combined (gabungan genres dan developer) menjadi representasi numerik.
# 
# 2. Cosine Similarity digunakan untuk mengukur kemiripan antar game berdasarkan vektor TF-IDF tersebut.

# %%
def get_recommendations(name, cosine_sim=cosine_sim):
    idx = df[df['name'].str.lower() == name.lower()].index
    if len(idx) == 0:
        return f"Game '{name}' tidak ditemukan di dataset."
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    game_indices = [i[0] for i in sim_scores]
    return df[['name', 'genres', 'developer']].iloc[game_indices]

# %% [markdown]
# Kelebihan :<br>
# - Tidak memerlukan interaksi atau data pengguna
# - Mengandalkan deskripsi konten yang tersedia
# 
# Kekurangan :<br>
# - Tidak memperhitungkan popularitas atau rating pengguna
# - Hanya fokus pada kemiripan konten, bukan perilaku pengguna

# %% [markdown]
# ## Evaluation

# %% [markdown]
# Karena sistem ini menggunakan pendekatan content-based filtering tanpa data interaksi pengguna (seperti klik, rating, atau waktu bermain), maka evaluasi dilakukan secara **kualitatif/manual**.
# 
# Metode evaluasi yang dilakukan:
# 1. **Manual Inspection**: Menguji beberapa judul game populer, lalu mengecek apakah hasil rekomendasinya relevan berdasarkan genre, developer, atau kontennya.
# 2. **Top-N Relevance Check**: Mengamati apakah daftar 10 teratas memiliki kemiripan konten dengan judul input.

# %%
get_recommendations("Grand Theft Auto V")

# %% [markdown]
# Contoh:
# Untuk input "Grand Theft Auto V", sistem merekomendasikan:
# - Manhunt
# - Grand Theft Auto
# - Grand Theft Auto 2
# - Grand Theft Auto IV
# - Grand Theft Auto : Episodes from Liberty City
# - Grand Theft Auto III
# - Grand Theft Auto : Vice City
# - Grand Theft Auto : San Andreas
# - Max Payne 3
# - L.A. Noire : the VR Case Files
# 
# Hasil ini dianggap **relevan**, karena game-game tersebut memiliki genre aksi dunia terbuka (open-world action) yang serupa.
# 
# > Karena tidak ada data relevansi eksplisit atau preferensi pengguna, maka metrik kuantitatif seperti Precision@K atau NDCG tidak dapat digunakan pada proyek ini.
# 

# %% [markdown]
# ✅ Apakah Sudah Menjawab Problem Statements?<br>
# Yes.<br>
# Problem statement menyatakan bahwa pengguna kesulitan menemukan game yang sesuai dengan preferensi mereka di tengah banyaknya pilihan game di pasar.
# Model ini berhasil memberikan rekomendasi yang relevan dan personalized berdasarkan genre dan developer, sehingga menjawab permasalahan utama tersebut.
# 
# 
# ✅ Apakah Berhasil Mencapai Goals?:<br>
# Yes.<br>
# Tujuan proyek adalah membangun sistem rekomendasi sederhana yang mampu:
# - Menganalisis data game berdasarkan metadata.
# - Memberikan rekomendasi game yang mirip dengan input user.
# Model telah mencapai kedua tujuan tersebut dengan pendekatan yang cukup ringan namun efektif (tanpa memerlukan user-item rating atau deep learning).
# 
# ✅ Apakah Solution Statements Berdampak?<br>
# Yes, to some extent.<br>
# Pendekatan content-based recommendation menggunakan TF-IDF berhasil memberikan:
# - Rekomendasi game yang mirip dari segi konten.
# - Hasil yang bisa ditafsir secara eksplisit oleh pengguna (karena berbasis genre/developer).
# 
# Dampaknya: sistem ini dapat diintegrasikan ke dalam platform pencarian game untuk membantu user dalam eksplorasi konten yang sesuai minatnya. Meski belum sepenuhnya personalized (karena belum menggunakan feedback pengguna), sistem ini tetap berdampak positif pada user experience.
# 


