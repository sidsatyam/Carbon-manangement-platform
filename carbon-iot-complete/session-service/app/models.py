from sqlalchemy import Column, Integer, String, DateTime, func, Text
from .database import Base

class Session(Base):
    __tablename__ = "device_sessions"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, index=True)
    status = Column(String, default="inactive")
    last_seen = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    restarted_count = Column(Integer, default=0)
    metadata = Column(Text, nullable=True)
