import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, auth, firestore
from fastapi import FastAPI, Request
import requests
import os

# pip install python-dotenv
# Load environment variables from the .env file
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

        # Create request payload
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        # Send request to Firebase Authentication REST API
        response = requests.post(
            "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword",
            params={"key": API_KEY},
            json=payload
        )

        # Check response status and retrieve user ID
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

@app.post("/logout")
async def logout_user(request: Request):
    try:
        data = await request.json()
        uid = data.get("uid")

        # Revoke user session and invalidate valid ID token
        auth.revoke_refresh_tokens(uid)
        return {"message": "Logout berhasil"}
    except Exception as e:
        return {"message": "Logout gagal", "error": str(e)}

@app.post("/register-account")
async def register_account(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        nama_lengkap = data.get("nama_lengkap")

        user = auth.create_user(email=email, password=password)

        # Save full name to Firestore
        user_data = {
            "Nama_Lengkap": nama_lengkap
        }
        db.collection("UserSingerHub").document(user.uid).set(user_data)
        
        return {"message": "Pengguna berhasil didaftarkan", "uid": user.uid}
    except Exception as e:
        return {"message": "Gagal mendaftarkan pengguna", "error": str(e)}

@app.post("/register-data-without-auth")
async def register_data_without_auth(request: Request):
    try:
        data = await request.json()
        id = data.get("id")
        nama_lengkap = data.get("nama_lengkap")
        umur = data.get("umur")
        jenis_kelamin = data.get("jenis_kelamin")
        daerah_asal = data.get("daerah_asal")
        pengalaman_bernyanyi = data.get("pengalaman_bernyanyi")
        genre_musik = data.get("genre_musik")
        keterampilan_alat_musik = data.get("keterampilan_alat_musik")
        alamat_tempat_tinggal = data.get("alamat_tempat_tinggal")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        user_data = {
            "Nama_Lengkap": nama_lengkap,
            "Umur": umur,
            "Jenis_Kelamin": jenis_kelamin,
            "Daerah_Asal": daerah_asal,
            "Pengalaman_Bernyanyi": pengalaman_bernyanyi,
            "Genre_Musik": genre_musik,
            "Keterampilan_Alat_Musik": keterampilan_alat_musik,
            "Alamat_Tempat_Tinggal": alamat_tempat_tinggal,
            "Latitude": latitude,
            "Longitude": longitude
        }
        db.collection("UserSingerHub").document(id).set(user_data)
        
        return {"message": "Data pengguna berhasil disimpan"}
    except Exception as e:
        return {"message": "Gagal menyimpan data pengguna", "error": str(e)}

@app.post("/register-data/{uid}")
async def register_data(uid: str, request: Request):
    try:
        # Validate UID
        try:
            auth.get_user(uid)
        except ValueError as e:
            if str(e) == "Cannot find user.":
                return {"message": "Invalid UID"}

        data = await request.json()
        nama_lengkap = data.get("nama_lengkap")
        umur = data.get("umur")
        jenis_kelamin = data.get("jenis_kelamin")
        daerah_asal = data.get("daerah_asal")
        pengalaman_bernyanyi = data.get("pengalaman_bernyanyi")
        genre_musik = data.get("genre_musik")
        keterampilan_alat_musik = data.get("keterampilan_alat_musik")
        alamat_tempat_tinggal = data.get("alamat_tempat_tinggal")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        user_data = {
            "Nama_Lengkap": nama_lengkap,
            "Umur": umur,
            "Jenis_Kelamin": jenis_kelamin,
            "Daerah_Asal": daerah_asal,
            "Pengalaman_Bernyanyi": pengalaman_bernyanyi,
            "Genre_Musik": genre_musik,
            "Keterampilan_Alat_Musik": keterampilan_alat_musik,
            "Alamat_Tempat_Tinggal": alamat_tempat_tinggal,
            "Latitude": latitude,
            "Longitude": longitude
        }
        db.collection("UserSingerHub").document(uid).set(user_data)

        return {"message": "Data pengguna berhasil disimpan"}
    except Exception as e:
        return {"message": "Gagal menyimpan data pengguna", "error": str(e)}

@app.put("/update-profile/{uid}")
async def update_profile(uid: str, request: Request):
    try:
        # Validate UID
        try:
            auth.get_user(uid)
        except ValueError as e:
            if str(e) == "Cannot find user.":
                return {"message": "Invalid UID"}

        data = await request.json()
        nama_lengkap = data.get("nama_lengkap")
        umur = data.get("umur")
        jenis_kelamin = data.get("jenis_kelamin")
        daerah_asal = data.get("daerah_asal")
        pengalaman_bernyanyi = data.get("pengalaman_bernyanyi")
        genre_musik = data.get("genre_musik")
        keterampilan_alat_musik = data.get("keterampilan_alat_musik")
        alamat_tempat_tinggal = data.get("alamat_tempat_tinggal")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Update user profile in Firestore
        updated_data = {
            "Nama_Lengkap": nama_lengkap,
            "Umur": umur,
            "Jenis_Kelamin": jenis_kelamin,
            "Daerah_Asal": daerah_asal,
            "Pengalaman_Bernyanyi": pengalaman_bernyanyi,
            "Genre_Musik": genre_musik,
            "Keterampilan_Alat_Musik": keterampilan_alat_musik,
            "Alamat_Tempat_Tinggal": alamat_tempat_tinggal,
            "Latitude": latitude,
            "Longitude": longitude
        }
        db.collection("UserSingerHub").document(uid).update(updated_data)

        return {"message": "Profil berhasil diperbarui"}
    except Exception as e:
        return {"message": "Gagal memperbarui profil", "error": str(e)}

@app.put("/update-profile-by-id/{id}")
async def update_profile_by_id(id: str, request: Request):
    try:
        data = await request.json()
        nama_lengkap = data.get("nama_lengkap")
        umur = data.get("umur")
        jenis_kelamin = data.get("jenis_kelamin")
        daerah_asal = data.get("daerah_asal")
        pengalaman_bernyanyi = data.get("pengalaman_bernyanyi")
        genre_musik = data.get("genre_musik")
        keterampilan_alat_musik = data.get("keterampilan_alat_musik")
        alamat_tempat_tinggal = data.get("alamat_tempat_tinggal")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Update user profile in Firestore
        updated_data = {
            "Nama_Lengkap": nama_lengkap,
            "Umur": umur,
            "Jenis_Kelamin": jenis_kelamin,
            "Daerah_Asal": daerah_asal,
            "Pengalaman_Bernyanyi": pengalaman_bernyanyi,
            "Genre_Musik": genre_musik,
            "Keterampilan_Alat_Musik": keterampilan_alat_musik,
            "Alamat_Tempat_Tinggal": alamat_tempat_tinggal,
            "Latitude": latitude,
            "Longitude": longitude
        }
        db.collection("UserSingerHub").document(id).update(updated_data)
        return {"message": "Profil berhasil diperbarui"}
    except Exception as e:
        return {"message": "Gagal memperbarui profil", "error": str(e)}

@app.get("/get-user-data")
async def get_user_data(uid: str = None, id: str = None):
    try:
        if uid:
            doc_ref = db.collection("UserSingerHub").document(uid)
            doc = doc_ref.get()
            if doc.exists:
                user_data = doc.to_dict()
                return {"message": "Data pengguna ditemukan", "user_data": user_data}
            else:
                return {"message": "Data pengguna tidak ditemukan"}
        elif id:
            users_ref = db.collection("UserSingerHub")
            query = users_ref.document(id)
            data = query.get().to_dict()
            if data is None:
                return {"message": "User data not found"}
            return {"message": "Data pengguna ditemukan", "user_data": data}
        else:
            return {"message": "Parameter UID atau ID harus diberikan"}
    except Exception as e:
        return {"message": "Gagal mendapatkan data pengguna", "error": str(e)}

if __name__ == "__main__":
    # Run using: uvicorn main:app --host 0.0.0.0 --port 8000
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
