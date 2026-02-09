from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid

from app.database import Base

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    issuer_id = Column(String, index=True)
    cert_uid = Column(String, index=True, unique=True)

    filename = Column(String)
    hash = Column(String, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)
