# Face Attendance System

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Firebase](https://img.shields.io/badge/firebase-%23039BE5.svg?style=for-the-badge&logo=firebase)

A Face Attendance System using Python, OpenCV, face_recognition, and Firebase for database storage.

## 📋 Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Features

- Real-time face detection and recognition
- Attendance tracking with timestamp
- Firebase integration for data storage
- User-friendly GUI
- Support for multiple faces in a single frame

## 🛠 Requirements

- Python 3.7+
- OpenCV
- face_recognition
- Firebase Admin SDK
- Other dependencies listed in `requirements.txt`

## 💻 Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/apresiasi-uniska/FaceRecognition.git
    cd FaceRecognition
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up Firebase:
    - Create a Firebase project
    - Download the Firebase Admin SDK JSON file
    - Rename it to `serviceAccountKey.json` and place it in the project root

## 🚀 Usage

1. Add images of individuals to the `Images` folder. Name each image with the person's name.

2. Generate encodings for the faces in the `Images` folder:
    ```sh
    python EncodeGenerator.py
    ```

3. Start the attendance system:
    ```sh
    python main.py
    ```

4. The system will open your webcam and start recognizing faces. Recognized faces will be marked for attendance in the Firebase database.

## ⚙ Configuration

- Modify `Config.py` to change Firebase configuration and other settings.
- Adjust face recognition parameters in `main.py` if needed.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
