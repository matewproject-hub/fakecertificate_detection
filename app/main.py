from fastapi import FastAPI,UploadFile,File,Depends
from sqlalchemy.orm import Session
import uuid
from fastapi.middleware.cors import CORSMiddleware


from app.database import SessionLocal,engine,Base
from app.models import Certificate
from app.utils import generate_hash
from app.qr_utils import extract_qr
# app/main.py





Base.metadata.create_all(bind=engine)

app=FastAPI(title="Fake Certificate Detection")




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
    
    # Try to extract cert UID (optional)
    qr_data = extract_qr(data)
    cert_uid = None
    if qr_data:
        parts = qr_data.split("|")
        cert_uid = parts[1]

    # Case 1: Exact hash exists → VALID
    found = db.query(Certificate).filter(Certificate.hash == new_hash).first()
    if found:
        return {
            "status": "VALID",
            "certificate_id": found.id,
            "filename": found.filename
        }
    
    # Case 2: Tampered → same cert_uid exists but hash changed
    if cert_uid:
        tampered = db.query(Certificate).filter(Certificate.cert_uid == cert_uid).first()
        if tampered:
            return {
                "status": "TAMPERED",
                "certificate_id": tampered.id,
                "filename": tampered.filename
            }

    # Case 3: Not found → no matching cert_uid or hash
    return {"status": "NOT FOUND"}

    
    


