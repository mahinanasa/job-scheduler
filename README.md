# Job Scheduler App

A Django-based job scheduling application that allows users to submit jobs with different priority levels. The system ensures that high-priority jobs run first and limits the number of concurrent jobs.

## 🚀 Features
- Job submission with priority levels (High, Medium, Low)
- Concurrent execution limit
- Periodic job processing using Celery
- PostgreSQL as the database
- Docker support for easy deployment
- API endpoints for job submission and retrieval

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2️⃣ Create & Activate Virtual Environment
```sh
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate (Linux/Mac)
venv\Scripts\activate  # Activate (Windows)
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file in the project root:
```sh
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/job_scheduler
CELERY_BROKER_URL=redis://localhost:6379/0
```

### 5️⃣ Apply Migrations & Create Superuser
```sh
python manage.py migrate
python manage.py createsuperuser
```

### 6️⃣ Start Services
#### Start Redis (for Celery)
```sh
redis-server
```

#### Start Celery Worker
```sh
celery -A job_scheduler worker --loglevel=info
```

#### Start Celery Beat (For Periodic Tasks)
```sh
celery -A job_scheduler beat --loglevel=info
```

#### Run Django Server
```sh
python manage.py runserver
```

## 📡 API Endpoints
- **Submit Job**: `POST /api/jobs/submit/`
- **List Jobs**: `GET /api/jobs/`
- **Retrieve Job**: `GET /api/jobs/<id>/`
