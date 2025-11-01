from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SessionCreate(BaseModel):
    device_id: int
    metadata: Optional[str] = None

class SessionResponse(BaseModel):
    id: int
    device_id: int
    status: str
    last_seen: Optional[datetime] = None
    started_at: Optional[datetime] = None
    restarted_count: int
    metadata: Optional[str] = None

    model_config = {'from_attributes': True}

class PingPayload(BaseModel):
    device_id: int
    timestamp: Optional[datetime] = None

class BulkDeviceIds(BaseModel):
    device_ids: List[int]
