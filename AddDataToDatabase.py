import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendance-database-84fca-default-rtdb.asia-southeast1.firebasedatabase.app/"

})

ref = db.reference('Students')

data = {
    "21310730037":
        {
            "nama": "Mohammad Rangga Nur Faizin",
            "jurusan": "Teknik Elektro",
            "angkatan": "2024",
            "total_absensi": 7,
            "kelas": "A2",
            "gender": "Laki-laki",
            "last_attendance_time": "2024-1-31 00:54:34"
        },
    "0838":
        {
            "nama": "Jokowi",
            "jurusan": "Teknik Elektro",
            "angkatan": "2022",
            "total_absensi": 7,
            "kelas": "A2",
            "gender": "Laki-laki",
            "last_attendance_time": "2024-1-31 00:54:34"
        },
    "5234":
        {
            "nama": "Prabowo",
            "jurusan": "Teknik Elektro",
            "angkatan": "2022",
            "total_absensi": 7,
            "kelas": "A2",
            "gender": "Laki-laki",
            "last_attendance_time": "2024-1-31 00:54:34"
        },
    "7479":
        {
            "nama": "Gibran",
            "jurusan": "Teknik Elektro",
            "angkatan": "2022",
            "total_absensi": 7,
            "kelas": "A2",
            "gender": "Laki-laki",
            "last_attendance_time": "2024-1-31 00:54:34"
        },
    "21310730040":
        {
            "nama": "Ubeid Brimbi S.",
            "jurusan": "Teknik Elektro",
            "angkatan": "2022",
            "total_absensi": 1,
            "kelas": "A2",
            "gender": "Laki-Laki",
            "last_attendance_time": "2024-1-31 00:54:34"
        },
    "20230620046":
        {
            "nama": "Putri Prasmardiana Fitri.",
            "jurusan": "Pertanian",
            "angkatan": "2020",
            "total_absensi": 0,
            "kelas": "A2",
            "gender": "Perempuan",
            "last_attendance_time": "2024-1-31 00:54:34"
        },
}

for key,value in data.items():
    ref.child(key).set(value)