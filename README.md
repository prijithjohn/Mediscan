# 🩺 MediScan – Doctor’s Handwriting OCR & AI Medical Assistant

## 📌 Overview

**MediScan** is a smart healthcare assistant that helps users understand handwritten prescriptions using OCR and AI.
It extracts text from doctor prescriptions, summarizes it, identifies possible diseases, analyzes medications, and even provides emergency alerts.

---

## 🚀 Features

### 📝 OCR & Summarization

* Upload handwritten prescription images
* Extract text using OCR API
* Generate clear summaries using Gemini AI

### 🧠 Disease Identification

* Detect possible diseases based on symptoms
* Supports both automatic (from summary) and manual input

### 💊 Drug Analysis

* Extract drug names from prescriptions
* Analyze drug compatibility and suggest alternatives

### 🚨 Emergency Alert System

* Detect high-risk conditions
* Send alerts via email in case of emergencies

### 👤 User Authentication

* Login & Registration system
* Trial-based usage (free usage limit)

### 💳 Subscription Module

* Plans for continued usage after trial ends

---

## 🛠️ Tech Stack

* **Frontend & Backend:** Python, Streamlit
* **AI Model:** Google Gemini
* **OCR API:** RapidAPI (Handwriting Recognition)
* **Email Service:** SMTP (Gmail)
* **Data Storage:** JSON (for user management)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/mediscan.git
cd mediscan
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Environment Variables

Create a `.env` file or set variables manually:

```env
GEMINI_API_KEY=your_api_key
EMAIL_PASSWORD=your_email_app_password
```

---

### 4️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 📷 How It Works

1. Upload prescription image
2. OCR extracts handwritten text
3. Gemini AI summarizes the content
4. System identifies diseases
5. Drug analysis is performed
6. Emergency alerts triggered if needed

---

## 🔐 Security Note

* API keys and credentials should not be hardcoded
* Use environment variables to keep them secure

---

## 📈 Future Improvements

* Database integration (MySQL / MongoDB)
* Payment gateway integration (Stripe/Razorpay)
* Real-time hospital API integration
* Mobile app version

---

## 👨‍💻 Author

**Prijith John**
Computer Science Engineering Student

---

## ⭐ Acknowledgements

* Google AI Studio
* RapidAPI OCR services
* Streamlit community

---

## 📌 Disclaimer

This application is for educational purposes only and should not be used as a substitute for professional medical advice.
