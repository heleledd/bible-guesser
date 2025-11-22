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

### 4. Use docker compose to read compose.yaml and build and run both containers 

```bash
docker-compose up --build
```

You can then browse to the React front end at http://localhost:5173 
Remember the React app runs ** in your browser ** so for development the API_URL needs to be http://localhost:8000, **not** http://backend:8000 because your local browser can't resolve "backend", that only works inside the containers 