# README: REST API for Job Postings (FastAPI + PostgreSQL + SQLAlchemy)
This project implements a REST API backend for managing job postings. It includes entities for jobs, skills, and locations, many‑to‑many relationships, test data generation, and a basic retrieval endpoint.

Features
CRUD foundation for job postings (currently, the GET /jobs endpoint is implemented).
Skills and locations stored in separate tables.
Many‑to‑many relationships: job ↔ skills, job ↔ locations.
Seed script to generate 200 test jobs, 10 locations, and 10 skills.
Normalized JSON response with nested lists of skills and locations.
Technical Requirements (Hardware & Environment)
Minimum requirements:

OS: Windows 10/11, macOS, or Linux.
CPU: 2 cores.
RAM: at least 4 GB (for running the Python app and PostgreSQL).
Disk space: at least 500 MB.
Required software:

Python 3.9–3.12.
PostgreSQL 12–16 (local installation or Docker).
VS Code or any code editor.
pip and venv (included with Python).
Installation and Setup (Step‑by‑Step)
1. Clone the Repository
bash
git clone <URL_of_the_repository>
cd <project_folder>
2. Create a Virtual Environment and Install Dependencies
Windows (PowerShell):

powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
macOS / Linux:

bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Example requirements.txt:

text
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
faker
pydantic
PostgreSQL Setup
Option A: Local PostgreSQL (Manual Setup)
Install PostgreSQL from the official website.
Create the database:
sql
CREATE DATABASE job_board;
Create a user (optional; you can use postgres):
sql
CREATE USER job_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE job_board TO job_user;
Ensure the server accepts local connections (check pg_hba.conf and postgresql.conf).
Option B: Using Docker (Recommended for Quick Start)
Create docker-compose.yml:

yaml
version: '3.8'
services:
  db:
    image: postgres:15
    container_name: pg_job_board
    environment:
      POSTGRES_DB: job_board
      POSTGRES_USER: job_user
      POSTGRES_PASSWORD: strong_password
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
Start the service:

bash
docker compose up -d
Environment Variables Configuration
Create a .env file in the project root:

text
DATABASE_URL=postgresql://job_user:strong_password@localhost:5432/job_board
⚠️ If you’re using Docker, keep the host as localhost because the container is mapped to port 5432 on the host.

Database Initialization and Test Data Population
Make sure the virtual environment is activated.
Run the seed script:
bash
python seed_jobs.py
On the first run, the script will create the tables and populate them with data.
⚠️ In production mode, do not keep the Base.metadata.drop_all(...) line in seed_jobs.py. It was used only for debugging.

Verify the number of records:

bash
python -c "import os; from sqlalchemy import create_engine; e = create_engine(os.getenv('DATABASE_URL')); with e.connect() as c: print('jobs:', c.execute('SELECT count(*) FROM jobs').scalar()); print('locations:', c.execute('SELECT count(*) FROM locations').scalar()); print('skills:', c.execute('SELECT count(*) FROM skills').scalar())"
Expected output: jobs: 200, locations: 10, skills: 10.

Running the FastAPI Server
bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
The server will be available at:

API documentation (Swagger UI): http://127.0.0.1:8000/docs
Main endpoint: http://127.0.0.1:8000/jobs (returns a list of jobs in JSON)
Example response:

json
[
  {
    "id": 1,
    "title": "Research scientist (life sciences)",
    "salary": 134286,
    "remote": true,
    "skills": ["light", "newspaper", "across"],
    "locations": ["West Dominique", "Charlotteberg"]
  }
]
Project Structure
text
project/
├── .env                    # environment variables (DATABASE_URL)
├── requirements.txt        # dependencies
├── seed_jobs.py           # script to populate the database
├── docker-compose.yml      # (optional) to run PostgreSQL in Docker
└── app/
    ├── __init__.py
    ├── main.py            # FastAPI app and routes
    └── models.py          # SQLAlchemy models (Job, Skill, Location, many‑to‑many tables)
└── README.md
Improving the Data (For Portfolio and Demo)
Currently, skills are generated randomly (fake.word()). For a more professional look, replace the skills generation block in seed_jobs.py:

python
skill_names = [
    "Python", "SQL", "Docker", "Git", "FastAPI",
    "JavaScript", "PostgreSQL", "CI/CD", "Testing", "Kubernetes"
]
skills = [Skill(name=name) for name in skill_names]
This will make the JSON responses meaningful and suitable for showcasing in your portfolio.

Testing and Debugging
Check DB connection: ensure DATABASE_URL in .env is correct and the job_board database exists.
View logs: when running uvicorn, SQLAlchemy, connection, and validation errors are printed to the console.
Swagger UI: use http://127.0.0.1:8000/docs to test endpoints.
SQL checks: in psql or pgAdmin:
sql
SELECT count(*) FROM jobs;
SELECT * FROM locations LIMIT 5;
Common Issues and Solutions
Issue	Solution
UndefinedColumn	Tables were created before the model was updated. For testing: temporarily add Base.metadata.drop_all(bind=engine) before create_all. For production, use migrations (Alembic).
InvalidRequestError (back_populates)	Verify that property names and back_populates values match exactly (letter‑for‑letter) in both models.
Cannot connect to the database	Check DATABASE_URL, credentials, database existence, and whether port 5432 is accessible.
Error with random.sample / fake.sample	Use random.sample(list, k=N); do not call fake.sample.
Suggestions for Project Enhancement (Great for Resume)
Add pagination: /jobs?page=1&size=20.
Implement filtering: ?remote=true&min_salary=150000.
Write tests with pytest (endpoint checks, JSON validation).
Integrate Alembic for database migrations.
Add authentication (JWT) and CRUD for creating/updating jobs.
