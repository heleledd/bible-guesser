## Local setup instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Backend Setup (FastAPI + SQLite)

Install requirements
```bash
cd backend
python -m venv venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the backend server
```bash
fastapi dev main.py
```

The backend server should be running at localhost:8000

### 3. Frontend Setup (React + JavaScript)

```bash
cd ../frontend
npm install
npm run dev
```

The react app should now be running at localhost:5173