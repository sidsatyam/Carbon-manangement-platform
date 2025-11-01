from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    type: str
    location: Optional[str] = None

    @field_validator('name', 'type')
    def not_empty(cls, v):
        if not v or not str(v).strip():
            raise ValueError('Field cannot be empty')
        return v

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None

class Device(DeviceBase):
    id: int
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {'from_attributes': True}

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = 'user'

    @field_validator('username', 'password')
    def not_empty(cls, v):
        if not str(v).strip():
            raise ValueError('Field cannot be empty')
        return v

class UserRead(BaseModel):
    id: int
    username: str
    role: str

    model_config = {'from_attributes': True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
