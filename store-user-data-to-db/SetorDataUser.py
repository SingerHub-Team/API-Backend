import pandas as pd
import requests

# Fungsi untuk melakukan request ke API register-data-without-auth
def register_data_without_auth(data):
    url = "http://localhost:8000/register-data-without-auth"
    response = requests.post(url, json=data)
    return response.json()

# Baca file Excel
df = pd.read_excel("store-user-data-to-db/UserSingerHub.xlsx")
total_success_store = 1
# Iterasi setiap baris data
for index, row in df.iterrows():
    # Buat payload data untuk dikirim ke API
    payload = {
        "id": row["ID"],
        "nama_lengkap": row["Nama_Lengkap"],
        "umur": row["Umur"],
        "jenis_kelamin": row["Jenis_Kelamin"],
        "daerah_asal": row["Daerah_Asal"],
        "pengalaman_bernyanyi": row["Pengalaman_Bernyanyi"],
        "genre_musik": row["Genre_Musik"],
        "keterampilan_alat_musik": row["Keterampilan_Alat_Musik"],
        "alamat_tempat_tinggal": row["Alamat_Tempat_Tinggal"],
        "latitude": row["Latitude"],
        "longitude": row["Longitude"]
    }
    
    # Kirim request ke API
    response = register_data_without_auth(payload)
    
    # Cetak hasil respons
    print(f'{total_success_store} {row["Nama_Lengkap"]} {response}')
    total_success_store += 1
