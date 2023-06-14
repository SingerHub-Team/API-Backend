import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, auth, firestore
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os

# pip install python-dotenv
# Load variabel environment dari file .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
DIR_FIREBASE_CONFIG = os.getenv("DIR_FIREBASE_CONFIG")
app = FastAPI()
cred = credentials.Certificate(DIR_FIREBASE_CONFIG)
firebase_admin.initialize_app(cred)

db = firestore.client()

## API Autentikasi (Register dan Login)
@app.post("/login")
async def login_user(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")

        # Membuat payload permintaan
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        # Mengirim permintaan ke API REST Firebase Authentication
        response = requests.post(
            "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword",
            params={"key": API_KEY},
            json=payload
        )

        # Memeriksa status respons dan mengambil ID pengguna
        if response.status_code == 200:
            user_data = response.json()
            uid = user_data["localId"]
            id_token = user_data["idToken"]
            return {"message": "Login berhasil", "uid": uid, "id_token": id_token}
        else:
            error_message = response.json()["error"]["message"]
            return {"message": "Login gagal", "error": error_message}

    except Exception as e:
        return {"message": "Login gagal", "error": str(e)}
# Pengujian: curl -X POST -d '{"email": "ridwan@singerhub.com", "password": "password123"}' -H "Content-Type: application/json" http://localhost:8000/login

@app.post("/logout")
async def logout_user(request: Request):
    try:
        data = await request.json()
        uid = data.get("uid")

        # Mencabut sesi pengguna dan membatalkan token ID yang valid
        auth.revoke_refresh_tokens(uid)
        return {"message": "Logout berhasil"}
    except Exception as e:
        return {"message": "Logout gagal", "error": str(e)}
# Pengujian: curl -X POST -d '{"id_token": "ID_TOKEN_AUTH_NYA"}' -H "Content-Type: application/json" http://localhost:8000/logout

class RegisterData(BaseModel):
    id: str
    nama_lengkap: str
    umur: int
    jenis_kelamin: str
    daerah_asal: str
    pengalaman_bernyanyi: int
    genre_musik: str
    keterampilan_alat_musik: str
    alamat_tempat_tinggal: str
    latitude: float
    longitude: float

@app.post("/register")
async def register_user(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        register_data = RegisterData(**data.get("register_data"))

        user = auth.create_user(email=email, password=password)
        
        # Menyimpan informasi pengguna tambahan ke database Firestore
        user_data = {
            "ID": register_data.id,
            "Nama_Lengkap": register_data.nama_lengkap,
            "Umur": register_data.umur,
            "Jenis_Kelamin": register_data.jenis_kelamin,
            "Daerah_Asal": register_data.daerah_asal,
            "Pengalaman_Bernyanyi": register_data.pengalaman_bernyanyi,
            "Genre_Musik": register_data.genre_musik,
            "Keterampilan_Alat_Musik": register_data.keterampilan_alat_musik,
            "Alamat_Tempat_Tinggal": register_data.alamat_tempat_tinggal,
            "Latitude": register_data.latitude,
            "Longitude": register_data.longitude
        }
        db.collection("UserSingerHub").document(user.uid).set(user_data)
        
        return {"message": "Pengguna berhasil dibuat", "uid": user.uid}
    except Exception as e:
        return {"message": "Gagal membuat pengguna", "error": str(e)}
# Pengujian: 
# curl -X POST -d '{
#   "email": "ridwan@singerhub.com",
#   "password": "password123",
#   "register_data": {
#     "id": "8G9K6S",
#     "nama_lengkap": "Rachman Ridwan",
#     "umur": 25,
#     "jenis_kelamin": "Laki-laki",
#     "daerah_asal": "Jakarta",
#     "pengalaman_bernyanyi": 5,
#     "genre_musik": "Pop",
#     "keterampilan_alat_musik": "Gitar",
#     "alamat_tempat_tinggal": "Jl. Cendrawasih No. 12, Jakarta Pusat",
#     "latitude": -6.18819,
#     "longitude": 106.82497
#   }
# }' -H "Content-Type: application/json" http://localhost:8000/register

## Perbarui Profil
class UpdateProfile(BaseModel):
    id: str
    nama_lengkap: str
    umur: int
    jenis_kelamin: str
    daerah_asal: str
    pengalaman_bernyanyi: int
    genre_musik: str
    keterampilan_alat_musik: str
    alamat_tempat_tinggal: str
    latitude: float
    longitude: float

@app.put("/update-profile/{uid}")
async def update_profile(uid: str, profile_update: UpdateProfile):
    try:
        data = profile_update.dict()
        # Memperbarui profil pengguna di database Firestore
        updated_data = {
            "ID": data.get("id"),
            "Nama_Lengkap": data.get("nama_lengkap"),
            "Umur": data.get("umur"),
            "Jenis_Kelamin": data.get("jenis_kelamin"),
            "Daerah_Asal": data.get("daerah_asal"),
            "Pengalaman_Bernyanyi": data.get("pengalaman_bernyanyi"),
            "Genre_Musik": data.get("genre_musik"),
            "Keterampilan_Alat_Musik": data.get("keterampilan_alat_musik"),
            "Alamat_Tempat_Tinggal": data.get("alamat_tempat_tinggal"),
            "Latitude": data.get("latitude"),
            "Longitude": data.get("longitude")
        }
        db.collection("UserSingerHub").document(uid).update(updated_data)
        return {"message": "Profil berhasil diperbarui"}
    except Exception as e:
        return {"message": "Gagal memperbarui profil", "error": str(e)}
# Pengujian:
# curl -X PUT -d '{
#   "id": "8G9K6S",
#   "nama_lengkap": "Budi Santoso",
#   "umur": 25,
#   "jenis_kelamin": "Laki-laki",
#   "daerah_asal": "Jakarta",
#   "pengalaman_bernyanyi": 5,
#   "genre_musik": "Pop",
#   "keterampilan_alat_musik": "Gitar",
#   "alamat_tempat_tinggal": "Jl. Cendrawasih No. 12, Jakarta Pusat",
#   "latitude": -6.18819,
#   "longitude": 106.82497
# }' -H "Content-Type: application/json" http://localhost:8000/update-profile/USER_UID

if __name__ == "__main__":
    # jalankan: uvicorn main:app --host 0.0.0.0 --port 8000
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
