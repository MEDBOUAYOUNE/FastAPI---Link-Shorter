from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PGUUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"))
    original_url = Column(String, nullable=False)
    shortened_url = Column(String, unique=True, nullable=False)
    open_count = Column(Integer, default=0)
    open_ips = Column(ARRAY(String), default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="links")

    def __repr__(self):
        return f"<Link(id={self.id}, original_url={self.original_url}, shortened_url={self.shortened_url})>"
    
    def __str__(self):
        return self.__repr__()

    @staticmethod
    def generate_shortened_url(base_url: str):
        shortened_url = uuid.uuid4().hex[:6]
        return f"{base_url}/{shortened_url}"
    
    def increment_open_count(self, ip_address: str):
        self.open_count += 1
        if ip_address not in self.open_ips:
            self.open_ips.append(ip_address)
        return self.open_count