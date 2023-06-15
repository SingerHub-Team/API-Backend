# Dokumentasi API - Rachman Ridwan (C23-PC608) | SingerHub Team
URL Postman: https://crimson-meteor-286265.postman.co/workspace/My-Workspace~fa951aa7-7621-4290-8e9e-56ea28be3b3a/collection/20240322-ed86dd2a-8118-4eed-8142-32428b11c430?action=share&creator=20240322
## Deskripsi
API yang telah dibuat adalah sebuah RESTful API yang digunakan untuk melakukan operasi otentikasi pengguna (Register, Login, Logout) dan operasi pembaruan profil pengguna.

Dokumentasi ini memberikan gambaran tentang API, protokol yang digunakan, endpoint-endpointnya, dan instruksi untuk menguji endpoint-endpoint tersebut menggunakan `curl` atau `POSTMAN`.

### Prasyarat
Sebelum menjalankan aplikasi, pastikan Anda memiliki prasyarat berikut:
- Python 3.7 atau yang lebih baru
- `pip` package manager
- Proyek Firebase dengan Firestore diaktifkan
- Kredensial SDK Admin Firebase (file JSON)

Serta, pastikan dependensi berikut sudah terinstal:
- `firebase_admin`
- `python-dotenv`
- `fastapi`
- `pydantic`
- `requests`
- `uvicorn`

Jika belum, install dependensi dengan menggunakan perintah berikut:

```shell
pip install firebase_admin python-dotenv fastapi pydantic requests uvicorn
```

Lalu, untuk mengeksekusi API, tinggal run `uvicorn main:app --host 0.0.0.0 --port 8000` pada terminal direktori `main.py`.

### Konfigurasi
1. Clone repositori ini:
```bash
git clone https://github.com/SingerHub-Team/API-Backend.git
```

2. Clone repositori ini:
```bash
cd API-Backend
```

3. Instal dependensi yang diperlukan:
```bash
pip install -r requirements.txt
```

4. Atur variabel lingkungan:
Buat file .env di direktori proyek dan tambahkan variabel lingkungan berikut:
```makefile
API_KEY=<kunci-api-firebase-anda>
DIR_FIREBASE_CONFIG=<lokasi-file-json-sdk-admin-firebase-anda>
```
API ini memerlukan beberapa variabel lingkungan yang harus diatur:
- API_KEY: Kunci API Firebase.
- DIR_FIREBASE_CONFIG: Path ke file konfigurasi Firebase.

5. Jalankan aplikasi:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
Aplikasi akan dapat diakses di http://localhost:8000.

## Protokol
API ini menggunakan protokol HTTP.

## Endpoint

### Login User
Menggunakan metode HTTP POST untuk melakukan login pengguna.

Endpoint: `/login`

#### Permintaan
| Parameter | Tipe   | Deskripsi           |
| --------- | ------ | --------------------|
| email     | string | Email pengguna      |
| password  | string | Kata sandi pengguna |

#### Respon
```json
{
    "message": "Login berhasil",
    "uid": "USER_UID",
    "id_token": "ID_TOKEN_AUTH_NYA"
}
```
### Pengujian menggunakan CURL
```json
curl -X POST -d '{"email": "ridwan@singerhub.com", "password": "password123"}' -H "Content-Type: application/json" http://localhost:8000/login
```

### Logout User
Menggunakan metode HTTP POST untuk melakukan logout pengguna.

Endpoint: `/logout`

#### Permintaan
| Parameter  | Tipe   | Deskripsi           |
| ---------- | ------ | --------------------|
| uid        | string | ID pengguna         |

#### Respon
```json
{
    "message": "Logout berhasil"
}
```

### Pengujian menggunakan CURL
```json
curl -X POST -d '{"id_token": "ID_TOKEN_AUTH_NYA"}' -H "Content-Type: application/json" http://localhost:8000/logout
```

### Register Account
Menggunakan metode HTTP POST untuk mendaftarkan akun pengguna.

Endpoint: `/register-account`

#### Permintaan
| Parameter     | Tipe   | Deskripsi           |
| ------------- | ------ | --------------------|
| email         | string | Email pengguna      |
| password      | string | Kata sandi pengguna |
| nama_lengkap  | string | Nama lengkap        |

#### Respon
```json
{
    "message": "Pengguna berhasil didaftarkan",
    "uid": "USER_UID"
}
```

### Pengujian menggunakan CURL
```json
curl -X POST -d '{"email": "ridwan@singerhub.com", "password": "password123", "nama_lengkap": "Ridwan Singer"}' -H "Content-Type: application/json" http://localhost:8000/register-account
```

### Register Data by UID
Menggunakan metode HTTP POST untuk mendaftarkan data pengguna berdasarkan UID.

Endpoint: `/register-data/{uid}`

#### Permintaan
| Parameter               | Tipe   | Deskripsi                            |
| ----------------------- | ------ | -------------------------------------|
| uid                     | string | UID pengguna                         |
| id                      | string | ID pengguna                          |
| nama_lengkap            | string | Nama lengkap pengguna                |
| umur                    | int    | Umur pengguna                        |
| jenis_kelamin           | string | Jenis kelamin pengguna               |
| daerah_asal             | string | Daerah asal pengguna                 |
| pengalaman_bernyanyi    | int    | Pengalaman bernyanyi (dalam tahun)   |
| genre_musik             | string | Genre musik pengguna                 |
| keterampilan_alat_musik | string | Keterampilan alat musik pengguna     |
| alamat_tempat_tinggal   | string | Alamat tempat tinggal pengguna       |
| latitude                | float  | Latitude koordinat pengguna          |
| longitude               | float  | Longitude koordinat pengguna         |

#### Respon
```json
{
    "message": "Data pengguna berhasil disimpan"
}
```

### Pengujian menggunakan CURL
```json
curl -X POST -d '{
    "id": "USER_ID",
    "nama_lengkap": "Ridwan Singer",
    "umur": 25,
    "jenis_kelamin": "Laki-laki",
    "daerah_asal": "Jakarta",
    "pengalaman_bernyanyi": 5,
    "genre_musik": "Pop",
    "keterampilan_alat_musik": "Gitar",
    "alamat_tempat_tinggal": "Jl. Bintaro Raya No. 123",
    "latitude": -6.123456,
    "longitude": 106.789012
}' -H "Content-Type: application/json" http://localhost:8000/register-data/{uid}
```


### Update Profile by UID
Menggunakan metode HTTP PUT untuk memperbarui profil pengguna berdasarkan UID.

Endpoint: `/update-profile/{uid}`

#### Permintaan
| Parameter           | Tipe   | Deskripsi                   |
| ------------------- | ------ | ----------------------------|
| uid                 | string | UID pengguna                |
| id                  | string | ID pengguna                 |
| nama_lengkap        | string | Nama lengkap pengguna       |
| umur                | int    | Umur pengguna               |
| jenis_kelamin       | string | Jenis kelamin pengguna      |
| daerah_asal         | string | Daerah asal pengguna        |
| pengalaman_bernyanyi| int    | Pengalaman bernyanyi (dalam tahun) |
| genre_musik         | string | Genre musik pengguna        |
| keterampilan_alat_musik | string | Keterampilan alat musik pengguna |
| alamat_tempat_tinggal | string | Alamat tempat tinggal pengguna |
| latitude            | float  | Latitude koordinat pengguna |
| longitude           | float  | Longitude koordinat pengguna|

#### Respon
```json
{
    "message": "Profil berhasil diperbarui"
}
```

### Pengujian menggunakan CURL
```json
curl -X PUT -d '{
    "nama_lengkap": "Ridwan Singer",
    "umur": 25,
    "jenis_kelamin": "Laki-laki",
    "daerah_asal": "Jakarta",
    "pengalaman_bernyanyi": 5,
    "genre_musik": "Pop",
    "keterampilan_alat_musik": "Gitar",
    "alamat_tempat_tinggal": "Jl. Bintaro Raya No. 123",
    "latitude": -6.123456,
    "longitude": 106.789012
}' -H "Content-Type: application/json" http://localhost:8000/update-profile/{uid}
```

### Update Profile by ID
Menggunakan metode HTTP PUT untuk memperbarui profil pengguna berdasarkan ID.

Endpoint: `/update-profile-by-id/{id}`

#### Permintaan
| Parameter           | Tipe   | Deskripsi                   |
| ------------------- | ------ | ----------------------------|
| id                  | string | ID pengguna                 |
| nama_lengkap        | string | Nama lengkap pengguna       |
| umur                | int    | Umur pengguna               |
| jenis_kelamin       | string | Jenis kelamin pengguna      |
| daerah_asal         | string | Daerah asal pengguna        |
| pengalaman_bernyanyi| int    | Pengalaman bernyanyi (dalam tahun) |
| genre_musik         | string | Genre musik pengguna        |
| keterampilan_alat_musik | string | Keterampilan alat musik pengguna |
| alamat_tempat_tinggal | string | Alamat tempat tinggal pengguna |
| latitude            | float  | Latitude koordinat pengguna |
| longitude           | float  | Longitude koordinat pengguna|

#### Respon
```json
{
    "message": "Profil berhasil diperbarui"
}
```

### Pengujian menggunakan CURL
```json
curl -X PUT -d '{
    "nama_lengkap": "Ridwan Singer",
    "umur": 25,
    "jenis_kelamin": "Laki-laki",
    "daerah_asal": "Jakarta",
    "pengalaman_bernyanyi": 5,
    "genre_musik": "Pop",
    "keterampilan_alat_musik": "Gitar",
    "alamat_tempat_tinggal": "Jl. Bintaro Raya No. 123",
    "latitude": -6.123456,
    "longitude": 106.789012
}' -H "Content-Type: application/json" http://localhost:8000/update-profile-by-id/{id}
```

## Get User Data by UID

Menggunakan metode HTTP GET untuk mendapatkan data pengguna berdasarkan UID.

Endpoint: `/get-user-data?uid={uid}`

### Permintaan
| Parameter | Tipe   | Deskripsi        |
| --------- | ------ | -----------------|
| uid       | string | UID pengguna     |

### Respon
```
{
    "message": "Data pengguna ditemukan",
    "user_data": {
        "id": "USER_ID",
        "nama_lengkap": "Ridwan Singer",
        "umur": 25,
        "jenis_kelamin": "Laki-laki",
        "daerah_asal": "Jakarta",
        "pengalaman_bernyanyi": 5,
        "genre_musik": "Pop",
        "keterampilan_alat_musik": "Gitar",
        "alamat_tempat_tinggal": "Jl. Bintaro Raya No. 123",
        "latitude": -6.123456,
        "longitude": 106.789012
    }
}
```

### Pengujian menggunakan CURL
```json
curl -X GET http://localhost:8000/get-user-data?uid={uid}
```

## Get User Data by ID

Menggunakan metode HTTP GET untuk mendapatkan data pengguna berdasarkan ID.

Endpoint: `/get-user-data?id={id}`

### Permintaan
| Parameter | Tipe   | Deskripsi        |
| --------- | ------ | -----------------|
| id        | string | ID pengguna      |

### Respon
```
{
    "message": "Data pengguna ditemukan",
    "user_data": {
        "id": "USER_ID",
        "nama_lengkap": "Ridwan Singer",
        "umur": 25,
        "jenis_kelamin": "Laki-laki",
        "daerah_asal": "Jakarta",
        "pengalaman_bernyanyi": 5,
        "genre_musik": "Pop",
        "keterampilan_alat_musik": "Gitar",
        "alamat_tempat_tinggal": "Jl. Bintaro Raya No. 123",
        "latitude": -6.123456,
        "longitude": 106.789012
    }
}
```

### Pengujian menggunakan CURL
```json
curl -X GET http://localhost:8000/get-user-data?id={id}
```

## Testing menggunakan POSTMAN
Anda juga dapat menggunakan POSTMAN untuk menguji API ini. Berikut adalah langkah-langkah yang dapat Anda ikuti:

1. Buka aplikasi POSTMAN.
2. Pilih metode HTTP yang sesuai (POST atau PUT) dan masukkan URL endpoint yang diinginkan.
3. Atur header "Content-Type" menjadi "application/json".
4. Tambahkan body request dengan format JSON sesuai dengan contoh permintaan pada masing-masing endpoint.
5. Klik tombol "Send" untuk mengirim permintaan ke API.
6. Periksa respons yang diterima dari API untuk melihat hasilnya.

Pastikan API telah berjalan di `http://localhost:8000` sebelum melakukan pengujian menggunakan POSTMAN.
