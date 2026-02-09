# Fake Certificate Detection & Verification Vault

**Live Demo:** [https://your-deployed-url.com](https://your-deployed-url.com)

## Features

- Register certificates (hash & QR data stored securely)
- Verify certificates (VALID / TAMPERED / NOT FOUND)
- QR code extraction from PDF / image
- PostgreSQL backend via Supabase
- Dockerized for easy deployment

## Screenshots

### 1. Backend Health Check
![Health Check](screenshots/health_check.png)

### 2. Upload Certificate
![Upload Certificate](screenshots/upload.png)

### 3. Verify Certificate
![Verify Certificate](screenshots/verify.png)

### 4. Database Table
![Database](screenshots/db_table.png)

---

## How to Use

1. Upload a certificate via `/upload`  
2. Verify a certificate via `/verify`  

**Responses**:  
- `VALID` → Certificate exists in database  
- `TAMPERED` → Hash does not match any stored certificate  
- `NOT FOUND` → Certificate not registered

---

## Tech Stack

- FastAPI + Uvicorn  
- PostgreSQL (Supabase)  
- SQLAlchemy ORM  
- Dockerized Deployment  
- Python libraries: pyzbar, pillow, pdf2image
