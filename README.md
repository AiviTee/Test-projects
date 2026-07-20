# README: REST API for Job Postings (FastAPI + PostgreSQL + SQLAlchemy)
This project implements a REST API backend for managing job postings. It includes entities for jobs, skills, and locations, many‑to‑many relationships, test data generation, and a basic retrieval endpoint.

## <div align="center">Features</div>
* CRUD foundation for job postings (currently, the GET /jobs endpoint is implemented).
* Skills and locations stored in separate tables.
* Many‑to‑many relationships: job ↔ skills, job ↔ locations.
* Seed script to generate 200 test jobs, 10 locations, and 10 skills.
* Normalized JSON response with nested lists of skills and locations.

## <div align="center">Technical Requirements (Hardware & Environment)</div>
### Minimum requirements:

- OS: Windows 10/11, macOS, or Linux.
- CPU: 2 cores.
- RAM: at least 4 GB (for running the Python app and PostgreSQL).
- Disk space: at least 500 MB.

### Required software:

- Python 3.9–3.12.
- PostgreSQL 12–16 (local installation or Docker).
- VS Code or any code editor.
- pip and venv (included with Python).

## <div align="center">Installation and Setup</div>
### 1. Clone the Repository
```bash
git clone <URL_of_the_repository>
cd <project_folder>
```
### 2. Create a Virtual Environment and Install Dependencies

#### Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## <div align="center">PostgreSQL Setup</div>
### Local PostgreSQL (Manual Setup)
* Install PostgreSQL from the official website.
* Create the database:
```sql
CREATE DATABASE job_board;
```
* Create a user (optional; you can use postgres):
```sql
CREATE USER job_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE job_board TO job_user;
```
* Ensure the server accepts local connections (check pg_hba.conf and postgresql.conf).

### Environment Variables Configuration

Create a .env file in the project root:

```text
DATABASE_URL=postgresql://job_user:strong_password@localhost:5432/job_board
```

### Database Initialization and Test Data Population
* Make sure the virtual environment is activated.
* Run the seed script:
```bash
python seed.py
```
* On the first run, the script will create the tables and populate them with data.


#### Verify the number of records:

```bash
python -c "import os; from sqlalchemy import create_engine; e = create_engine(os.getenv('DATABASE_URL')); with e.connect() as c: print('jobs:', c.execute('SELECT count(*) FROM jobs').scalar()); print('locations:', c.execute('SELECT count(*) FROM locations').scalar()); print('skills:', c.execute('SELECT count(*) FROM skills').scalar())"
```
Expected output: jobs: 200, locations: 10, skills: 10.

## <div align="center">Running the FastAPI Server</div>
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
The server will be available at:

- API documentation (Swagger UI): http://127.0.0.1:8000/docs
- Main endpoint: http://127.0.0.1:8000/jobs (returns a list of jobs in JSON)



### Improving the Data (For Portfolio and Demo)
Currently, skills are generated randomly (fake.word()). For a more professional look, replace the skills generation block in seed.py:

```python
skill_names = [
    "Python", "SQL", "Docker", "Git", "FastAPI",
    "JavaScript", "PostgreSQL", "CI/CD", "Testing", "Kubernetes"
]
skills = [Skill(name=name) for name in skill_names]
```


