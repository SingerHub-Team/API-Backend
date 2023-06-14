# Dokumentasi API - Rachman Ridwan (C23-PC608)
URL Postman: https://crimson-meteor-286265.postman.co/workspace/fa951aa7-7621-4290-8e9e-56ea28be3b3a/documentation/20240322-ed86dd2a-8118-4eed-8142-32428b11c430
## Deskripsi
API yang telah dibuat adalah sebuah RESTful API yang digunakan untuk melakukan operasi otentikasi pengguna (Register, Login, Logout) dan operasi pembaruan profil pengguna.

Dokumentasi ini memberikan gambaran tentang API, protokol yang digunakan, endpoint-endpointnya, dan instruksi untuk menguji endpoint-endpoint tersebut menggunakan `curl` atau `POSTMAN`.

### Prasyarat
Sebelum menjalankan aplikasi, pastikan Anda memiliki prasyarat berikut:
- Python 3.7 atau yang lebih baru
- `pip` package manager
- Proyek Firebase dengan Firestore diaktifkan
- Kredensial SDK Admin Firebase (file JSON)
- Paket `python-dotenv` (instal dengan `pip install python-dotenv`)

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

### Register User
Menggunakan metode HTTP POST untuk melakukan registrasi pengguna.

Endpoint: `/register`

#### Permintaan
| Parameter        | Tipe   | Deskripsi                     |
| ---------------- | ------ | ------------------------------|
| email            | string | Email pengguna                |
| password         | string | Kata sandi pengguna           |
| name             | string | Nama pengguna                 |
| phone_number     | string | Nomor telepon pengguna        |
| experience       | string | Pengalaman pengguna           |
| skills           | string | Keahlian pengguna             |
| country          | string | Negara pengguna               |
| date_of_birth    | string | Tanggal lahir pengguna (YYYY-MM-DD) |

#### Respon
```json
{
    "message": "Pengguna berhasil dibuat",
    "uid": "USER_UID"
}
```

### Pengujian menggunakan CURL
```json
curl -X POST -d '{"email": "ridwan@singerhub.com", "password": "password123", "name": "Rachman Ridwan", "phone_number": "21312312", "experience": "5 tahun", "skills": "Python, JavaScript", "country": "Malaysia", "date_of_birth": "1990-01-01"}' -H "Content-Type: application/json" http://localhost:8000/register
```

### Update Profile
Menggunakan metode HTTP PUT untuk memperbarui profil pengguna.

Endpoint: `/update-profile/{uid}`

#### Permintaan
| Parameter        | Tipe   | Deskripsi                     |
| ---------------- | ------ | ------------------------------|
| uid              | string | ID pengguna                   |
| name             | string | Nama pengguna                 |
| phone_number     | string | Nomor telepon pengguna        |
| experience       | string | Pengalaman karir pengguna     |
| skills           | string | Keahlian pengguna             |
| country          | string | Negara pengguna               |
| date_of_birth    | string | Tanggal lahir pengguna (YYYY-MM-DD) |

#### Respon
```json
{
    "message": "Profil berhasil diperbarui"
}
```

### Pengujian menggunakan CURL
```json
curl -X PUT -d '{"name": "R. Ridwan", "phone_number": "08210310231", "experience": "10 tahun", "skills": "C++, C#, Python", "country": "Indonesia", "date_of_birth": "2002-09-29"}' -H "Content-Type: application/json" http://localhost:8000/update-profile/USER_UID
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
