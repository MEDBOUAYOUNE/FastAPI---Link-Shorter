from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from cryptography.fernet import Fernet
import uuid

from app.db import Base
from app.settings import HASHING_SECRET



class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, is_active={self.is_active})>"
    
    def __str__(self):
        return self.__repr__()
    
    @staticmethod
    def encode_password(password: str):
        f = Fernet(HASHING_SECRET)
        return f.encrypt(password.encode()).decode()


    def verify_password(self, password: str) -> bool:
        f = Fernet(HASHING_SECRET)
        try:
            return f.decrypt(self.hashed_password.encode()).decode() == password
        except Exception:
            return False

