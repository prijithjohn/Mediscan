# 🚀 MediScan AI

## AI-Powered Medical Prescription Analysis Platform

MediScan AI is a production-ready medical prescription analysis platform that uses OCR and Generative AI to extract, analyze, and structure information from prescription images.

The platform provides a complete workflow from prescription upload to OCR processing, AI-powered analysis, structured data persistence, usage tracking, history management, and risk-based alerts.

Built with modern backend engineering practices including REST APIs, PostgreSQL, Alembic migrations, Docker, automated testing, GitHub Actions CI, and cloud deployment.

🌐 **Live Demo:** https://mediscan-2lzy.onrender.com

🔗 **Backend API:** https://mediscan-backend-82ft.onrender.com

❤️ **Backend Health:** https://mediscan-backend-82ft.onrender.com/health

---

# 📸 Screenshots

> Replace these placeholders with actual screenshots.

### 🏠 Dashboard

![MediScan Dashboard](screenshots/dashboard.png)

### 📤 Prescription Upload

![Prescription Upload](screenshots/upload.png)

### 🤖 AI Prescription Analysis

![AI Analysis](screenshots/analysis.png)

### 📋 Prescription History

![Prescription History](screenshots/history.png)

### 🚨 Alerts

![Alerts](screenshots/alerts.png)

---

# ✨ Features

- 📤 Upload prescription images
- 🔍 OCR-based text extraction
- 🤖 AI-powered prescription analysis using Gemini
- 💊 Structured prescription information extraction
- 📋 Prescription history
- 👤 User authentication and isolation
- 📊 Usage tracking and limits
- 🚨 Risk-based alert generation
- 📧 Optional email alert support
- 🗄️ PostgreSQL database persistence
- 🔄 Alembic database migrations
- 🔐 JWT-based authentication
- 🛡️ API security and validation
- 🐳 Dockerized application
- 🧪 Automated test suite
- ⚙️ GitHub Actions CI
- ☁️ Render deployment
- 🌐 Configurable CORS
- ❤️ Backend health monitoring

---

# 🏗️ Architecture

```text
                         User
                           │
                           ▼
                    Streamlit Frontend
                           │
                           │ REST API
                           ▼
                    FastAPI Backend
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
        OCR             Gemini AI       PostgreSQL
     Processing          Analysis         / Supabase
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                    Alert & Usage System
                           │
                           ▼
                     Email Service
```

---

# 🔄 Application Workflow

```text
Prescription Image
        │
        ▼
      Upload
        │
        ▼
   Authentication
        │
        ▼
       OCR
        │
        ▼
Extract Prescription Text
        │
        ▼
    Gemini AI
        │
        ▼
Structured Prescription Data
        │
        ▼
   Risk Analysis
        │
        ├───────────────┐
        ▼               ▼
   PostgreSQL        Alert System
        │
        ▼
 Prescription History
```

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Language | Python |
| Database | PostgreSQL |
| Database Hosting | Supabase |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT / Python-Jose |
| Password Hashing | Argon2 |
| OCR | RapidAPI OCR |
| AI | Google Gemini API |
| API Communication | REST |
| Validation | Pydantic |
| Testing | Pytest |
| Containerization | Docker |
| Local Orchestration | Docker Compose |
| CI/CD | GitHub Actions |
| Deployment | Render |

---

# 🔐 Security

MediScan implements several application-level security mechanisms:

- 🔐 JWT authentication
- 🔒 Password hashing using Argon2
- 🛡️ Protected API routes
- 👤 User-level data isolation
- ✅ Request validation using Pydantic
- 📁 File upload validation
- 📊 Usage limit enforcement
- 🔑 Environment-based secret management
- 🌐 CORS configuration
- 🚫 No production secrets committed to Git

---

# 🧪 Testing

The project includes automated tests covering:

- Authentication
- Prescription processing
- Security
- User isolation
- Usage limits
- Alerts
- Alert service
- API client
- Database bootstrap

### Current Test Status

```text
21 passed
0 failed
```

Regression validation also covers the previously completed application phases.

Run the complete test suite:

```bash
pytest -q
```

---

# 🗄️ Database & Migrations

MediScan uses PostgreSQL for production persistence.

Database schema changes are managed using Alembic.

### Run migrations

```bash
python -m alembic upgrade head
```

### Check the current migration

```bash
python -m alembic current
```

The production deployment runs database migrations before starting the backend application.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/prijithjohn/Mediscan.git

cd Mediscan
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

## 3. Activate the Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file for local development.

```env
DATABASE_URL=postgresql://username:password@host:5432/database

SECRET_KEY=your_secret_key

GEMINI_API_KEY=your_gemini_api_key

RAPIDAPI_KEY=your_rapidapi_key

RAPIDAPI_HOST=pen-to-print-handwriting-ocr.p.rapidapi.com

CORS_ALLOW_ORIGINS=http://localhost:8501
```

### Optional Email Configuration

Email alerts can be enabled by configuring:

```env
SMTP_HOST=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
ALERT_EMAIL=
```

> ⚠️ Never commit real API keys, database passwords, JWT secrets, or SMTP credentials to Git.

---

# 🐳 Run with Docker

Build and start the application:

```bash
docker compose up --build
```

The application runs as:

```text
Frontend:
http://localhost:8501

Backend:
http://localhost:8000

Health:
http://localhost:8000/health
```

### Stop the Containers

```bash
docker compose down
```

---

# 🧪 Run Tests

Run the complete test suite:

```bash
pytest -q
```

Expected result:

```text
21 passed
```

---

# 🚀 Deployment

MediScan is deployed using:

- 🐳 Docker
- ☁️ Render
- 🗄️ PostgreSQL
- 🟢 Supabase
- ⚙️ GitHub Actions
- 🔄 Alembic

### Frontend

🌐 https://mediscan-2lzy.onrender.com

### Backend

🌐 https://mediscan-backend-82ft.onrender.com

### Health Check

❤️ https://mediscan-backend-82ft.onrender.com/health

The backend uses Render's dynamic `PORT` environment variable and binds to:

```text
0.0.0.0
```

Database migrations are executed during backend startup.

---

# ⚙️ CI/CD

GitHub Actions validates the application before deployment.

The CI pipeline performs:

```text
Push to GitHub
      │
      ▼
Install Dependencies
      │
      ▼
Validate Workflow
      │
      ▼
Run Pytest
      │
      ▼
Validate Docker Build
      │
      ▼
Validate Docker Compose
      │
      ▼
      ✅ PASS
```

---

# 📂 Project Structure

```text
Mediscan/
│
├── backend/
│   └── app/
│       ├── api/
│       │   ├── routes/
│       │   │   ├── auth.py
│       │   │   ├── prescriptions.py
│       │   │   ├── usage.py
│       │   │   ├── alerts.py
│       │   │   └── pipeline.py
│       │   │
│       │   ├── deps.py
│       │   └──
│       │
│       ├── core/
│       │   ├── config.py
│       │   └── security.py
│       │
│       ├── db/
│       │   ├── models/
│       │   ├── base.py
│       │   └── session.py
│       │
│       ├── schemas/
│       │
│       ├── services/
│       │   ├── ocr_service.py
│       │   ├── gemini_service.py
│       │   ├── prescription_service.py
│       │   ├── usage_service.py
│       │   ├── alert_service.py
│       │   └── email_service.py
│       │
│       └── main.py
│
├── frontend/
│   ├── app.py
│   └── api_client.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── scripts/
│   ├── container_e2e.py
│   └── create_e2e_data.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_prescription.py
│   ├── test_security.py
│   ├── test_usage.py
│   ├── test_alerts.py
│   ├── test_alert_service.py
│   ├── test_api_client.py
│   └── test_db_bootstrap.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
├── alembic.ini
├── requirements.txt
└── README.md
```

---

# 💡 Engineering Skills Demonstrated

- ⚡ FastAPI Backend Development
- 🔌 REST API Design
- 🖥️ Streamlit Application Development
- 🐍 Python Backend Engineering
- 🗄️ PostgreSQL
- 🔗 SQLAlchemy ORM
- 🔄 Alembic Database Migrations
- 🔐 JWT Authentication
- 🛡️ API Security
- 🔍 OCR API Integration
- 🤖 Google Gemini API Integration
- 🧠 AI Application Development
- 🐳 Docker & Docker Compose
- ⚙️ GitHub Actions CI
- ☁️ Cloud Deployment
- 🟢 Supabase
- 🧪 Automated Testing
- 🔬 End-to-End Validation
- 🔧 Environment Configuration
- 🐛 Production Debugging

---

# 👨‍💻 Author

## Prijith John

- 🔗 **GitHub:** https://github.com/prijithjohn
- 💼 **LinkedIn:** https://www.linkedin.com/in/prijith-john-dev/
- 🌐 **Portfolio:** https://prijith-portfolio.vercel.app/

---

# ⭐ Support

If you found MediScan useful, consider giving the project a **⭐ Star** on GitHub.

It helps support the project and makes it easier for others to discover.

---

## ⚠️ Disclaimer

MediScan AI is an experimental software project intended for educational and demonstration purposes.

The system uses OCR and Generative AI to analyze prescription images and may produce inaccurate, incomplete, or incorrect information.

**MediScan AI should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional before making medical decisions.**
