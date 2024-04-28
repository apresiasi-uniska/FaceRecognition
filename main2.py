import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

# Inisialisasi Firebase dengan menggunakan service account key
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-database-84fca-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "attendance-database-84fca.appspot.com"
})

# Menggunakan storage bucket untuk menyimpan data
bucket = storage.bucket()

# Inisialisasi video capture dari kamera ke-1
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# Resize frame input hanya satu kali
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

imgBackground = cv2.imread('Resources/background.png')

# Mengimport gambar mode ke dalam list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    img = cv2.imread(os.path.join(folderModePath, path))
    # Resize the image to match the region size
    img = cv2.resize(img, (414, 633))
    imgModeList.append(img)

# print(len(imgModeList))

# Load The encode file
print("Loading Encode Files.....")
file = open('EncodeFile.p', 'rb')
encodeListKnowWithIds = pickle.load(file)
file.close()
encodeListKnow, studentIds = encodeListKnowWithIds
print("Encode Loaded")

modeType = 0
counter = 0
id = -1

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[150:150 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    # Tampilkan tanggal secara realtime pada background utama
    current_date = datetime.now()
    formatted_date = current_date.strftime("%A, %d %B %Y %H:%M:%S")
    cv2.putText(imgBackground, formatted_date, (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    non_recognition_displayed = False  # Flag to track if "Non Recognition" is displayed

    if faceCurFrame:
        recognized_face = False
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                recognized_face = True
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0, colorC=(0, 255, 0))  # Green color
                id = studentIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
                    imgStudent = []

        if not recognized_face:
            non_recognition_displayed = True
            # Display "Non Recognition" message
            cv2.putText(imgBackground, "Non Recognition", (275, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if counter != 0:
            if counter == 1:
                # get the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                # get the image from the storage
                blob = bucket.get_blob(f'Images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGR2RGB)

                # Update The data
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 50:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_absensi'] += 1
                    ref.child('total_absensi').set(studentInfo['total_absensi'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_absensi']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(studentInfo['jurusan']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['kelas']), (860, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(studentInfo['gender']), (970, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(studentInfo['angkatan']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['nama'], cv2.FONT_HERSHEY_COMPLEX, 0.7, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['nama']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (50, 50, 50), 1)

                    # Resize and crop the student image to 216x216
                    imgStudentResized = cv2.resize(imgStudent, (216, 216))
                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudentResized

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
