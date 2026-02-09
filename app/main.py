from fastapi import FastAPI,UploadFile,File,Depends
from sqlalchemy.orm import Session
import uuid
from fastapi.middleware.cors import CORSMiddleware


from app.database import SessionLocal,engine,Base
from app.models import Certificate
from app.utils import generate_hash
from app.qr_utils import extract_qr
# app/main.py
from fastapi.staticfiles import StaticFiles




Base.metadata.create_all(bind=engine)

app=FastAPI(title="Fake Certificate Detection")

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Certificate Validation Vault Running"}


@app.post("/upload")
async def upload_certificate(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    data = await file.read()
    hash_value=generate_hash(data)
    qr_data = extract_qr(data)

    issuer_id = None
    cert_uid = None

    if qr_data:
        parts = qr_data.split("|")
        issuer_id = parts[0]
        cert_uid = parts[1]


    cert = Certificate(
    issuer_id=issuer_id,
    cert_uid=cert_uid,
    filename=file.filename,
    hash=hash_value
    )


    db.add(cert)
    db.commit()
    return {
        "message": "Certificate uploaded",
        "hash": hash_value,
        "issuer_id": issuer_id,
        "cert_uid": cert_uid
    }


@app.post("/verify")
async def verify_certificate(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):


    data = await file.read()
    new_hash = generate_hash(data)

    found = db.query(Certificate).filter(Certificate.hash == new_hash).first()

    if found:
        return {
            "status": "VALID",
            "certificate_id": found.id,
            "filename": found.filename
        }

    return {
        "status": "TAMPERED / NOT FOUND"
    }


    
    


