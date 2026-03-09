# 💪 FitBuddy – AI Fitness Plan Generator

A web-based application that uses **Google Gemini AI** to generate personalized 7-day workout plans and nutrition tips based on a user's fitness goals.

Built with **FastAPI** · **Jinja2** · **SQLite** · **Google Gemini 1.5**

---

## 🚀 Features

- **Personalized 7-Day Workout Plans** — Input name, age, weight, goal & intensity; get a full day-by-day schedule
- **AI Nutrition Tips** — Goal-aligned nutrition and recovery advice
- **Feedback Loop** — Submit feedback to regenerate and refine your plan
- **Admin Panel** — View all users and their plans at `/admin`
- **SQLite Database** — Persistent storage via SQLAlchemy ORM

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| AI | Google Gemini 1.5 Pro & Flash |
| Database | SQLite + SQLAlchemy |
| Frontend | Jinja2 Templates + HTML/CSS/JS |
| Server | Uvicorn |

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fitbuddy.git
cd fitbuddy
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

> **Get your Gemini API key** at [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 5. Run the application

```bash
python run.py
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📁 Project Structure

```
fitbuddy/
├── app/
│   ├── main.py               # FastAPI app entry point
│   ├── models/
│   │   └── database.py       # SQLAlchemy models & DB setup
│   ├── routes/
│   │   ├── routes.py         # URL endpoints
│   │   └── ai_service.py     # Gemini AI integration
│   ├── templates/
│   │   ├── base.html         # Shared layout
│   │   ├── index.html        # Home / form page
│   │   ├── result.html       # Generated plan page
│   │   └── all_users.html    # Admin panel
│   └── static/
│       ├── css/style.css     # Stylesheet
│       └── js/main.js        # Frontend JS
├── run.py                    # Dev server runner
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🌐 Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with input form |
| `/generate` | POST | Generate 7-day workout plan |
| `/feedback/{plan_id}` | POST | Regenerate plan with feedback |
| `/plan/{plan_id}` | GET | View a specific plan |
| `/admin` | GET | Admin panel – all users |

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key (required) |

---

## 📦 Deployment

### Deploy to Render

1. Push code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `GEMINI_API_KEY`

### Deploy to Railway

1. Connect your GitHub repo on [Railway](https://railway.app)
2. Add environment variable: `GEMINI_API_KEY`
3. Railway auto-detects Python and deploys

---

## 👥 Team

| Name | Role |
|------|------|
| Aditya Sharma | Team Lead |
| Amit Kumar | Member |
| Ayush Kumar Mishra | Member |
| Shivam Kumar Verma | Member |
