# ❤️ Heart Disease Prediction Using Multimodal 

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![Machine Learning](https://img.shields.io/badge/ML-XGBoost%20%7C%20CNN-green.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)
![FYP](https://img.shields.io/badge/FYP-Final%20Year%20Project-orange.svg)

---

## 📌 Overview

Heart Disease Prediction Using Multimodal AI is a machine learning-based final year project that predicts heart disease by combining **ECG image analysis** and **clinical patient data**.

The system uses:
- 🫀 CNN for ECG image classification  
- 📊 XGBoost for clinical data prediction  
- 🔗 Fusion-based decision system for final risk assessment  

A Streamlit web application is used to provide real-time predictions.

---

## 🧠 System Architecture

### 🔵 ECG Pipeline
- ECG image upload  
- Grayscale conversion  
- Signal extraction  
- Lead processing  
- CNN-based prediction  

---

### 🟢 Clinical Pipeline
- Input of 13 medical features  
- Data preprocessing  
- XGBoost classification  

---

### 🔗 Fusion Module
Both model outputs are combined using a weighted fusion approach to improve prediction accuracy and reliability.

---

## 🚀 Features

- ⚡ Real-time prediction system  
- 🫀 ECG image classification using CNN  
- 📊 Clinical data analysis using XGBoost  
- 🔗 Multimodal fusion of predictions  
- 📈 Risk levels: Low, Moderate, High  
- 🖥 Streamlit interactive web app  
- 📊 ECG processing visualization  

---

## 🛠 Tech Stack

- Python  
- Streamlit  
- XGBoost  
- TensorFlow / Keras  
- Scikit-learn  
- OpenCV  
- NumPy  
- Pandas  
- Matplotlib  
- Scikit-image  

---

## 📂 Project Structure
Heart-Disease-Detection-Using-Multimodel/
│
├── app.py
├── Ecg.py
├── Clinical_XGBoost_Model.pkl
├── models/
├── utils/
├── assets/
├── requirements.txt
└── README.md

---

## ▶️ How to Run

```bash
git clone https://github.com/your-username/heart-disease-prediction-using-Multimodal.git
cd heart-disease-prediction-using-Multimodal
pip install -r requirements.txt
streamlit run app.py
```

## 🧪 Workflow
```
Upload ECG image 🫀
Enter clinical data 📊
ECG processed using CNN
Clinical data processed using XGBoost
Fusion engine combines results
Final risk prediction displayed
```

## 📊 Output Classes
```
✅ Low Risk
⚠️ Moderate Risk
🚨 High Risk

The class of ECG means which type of ECG it is
Separate risk of both clinical and ECG data
```

##🎯 Objective
```
To develop an AI-based multimodal system that improves early detection of heart disease by combining ECG image analysis and clinical data, reducing diagnostic errors and improving accuracy.
```
```
👨‍💻 Author
Abdullah Zahid
Final Year Computer Science Student
FYP Project (2026)
```
```
📌 Note
This project is developed for academic purposes as a Final Year Project.

```
Datasets link
ECG: https://data.mendeley.com/datasets/gwbz3fsgp8/2
Clinical: https://archive.ics.uci.edu/dataset/45/heart+disease or https://github.com/AbdullahZahid1/Heart-Disease-Detection-using-Multimodal/blob/main/Datasets%20sample/heart.csv (preprocessed)

