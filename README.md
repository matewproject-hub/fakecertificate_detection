Certificate Validation Vault

A backend system for registering and verifying digital certificates. It stores certificate hashes in a database and allows external systems to check certificate validity, detecting tampering if a unique certificate ID is available.

Features

Register certificates securely by storing their hash values.

Verify uploaded certificates:

VALID → exact certificate exists in the database.

TAMPERED → certificate ID exists but hash changed.

NOT FOUND → certificate not in database.

Role-based access:

Issuer → can upload certificates.

Verifier → can verify certificates.

Backend-only API — easily integratable with any frontend or system.

Uses PostgreSQL (e.g., Supabase) as storage.

Supports QR-based certificate UID extraction (optional).

Tech Stack

Python 3.10+

FastAPI — API backend

SQLAlchemy — ORM

PostgreSQL (Supabase recommended)

Pillow + pyzbar — optional QR extraction

Uvicorn — ASGI server

python-dotenv — environment variable management

Installation

Clone the repository:

git clone https://github.com/your-username/fakecertificate_detection.git
cd fakecertificate_detection


Create a virtual environment:

python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install --upgrade pip
pip install -r requirements.txt


Create a .env file in the root directory:

DATABASE_URL=postgresql://<username>:<password>@<host>:5432/<database_name>

Database Setup

The app uses SQLAlchemy to manage tables.

Run this once to create tables:

from app.database import Base, engine
Base.metadata.create_all(bind=engine)


Table certificates schema:

Column	Type	Notes
id	UUID	Primary key, auto-generated
filename	String	Uploaded file name
hash	String	SHA256 hash of certificate
issuer_id	String	Optional from QR
cert_uid	String	Optional unique certificate ID
created_at	DateTime	Timestamp of upload
API Endpoints
1. Root
GET /


Response:

{
  "message": "Certificate Validation Vault Running"
}

2. Upload Certificate (Issuer only)
POST /upload


Form-data:

file → certificate file (PDF, image, etc.)

x-role → issuer (HTTP header)

Response:

{
  "message": "Certificate uploaded",
  "hash": "<hash_value>",
  "issuer_id": "<issuer_id if QR exists>",
  "cert_uid": "<cert_uid if QR exists>"
}

3. Verify Certificate (Verifier or Issuer)
POST /verify


Form-data:

file → certificate file

x-role → verifier or issuer (HTTP header)

Response:

// Case 1: VALID
{
  "status": "VALID",
  "certificate_id": "<id>",
  "filename": "<filename>"
}

// Case 2: TAMPERED
{
  "status": "TAMPERED",
  "certificate_id": "<id>",
  "filename": "<filename>"
}

// Case 3: NOT FOUND
{
  "status": "NOT FOUND"
}

Running Locally
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


Backend will be available at http://127.0.0.1:8000/

Deployment (Render / Railway / Any Cloud)

Add .env variables in the platform’s dashboard.

Use this start command:

uvicorn app.main:app --host 0.0.0.0 --port $PORT


Ensure PORT is set by the platform.

Database must be accessible from the cloud host (check Supabase IP rules if used).

Integration

Any frontend or external system can call /upload and /verify endpoints.

The backend handles all certificate validation logic.
