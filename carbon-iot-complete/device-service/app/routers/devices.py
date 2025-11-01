from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.auth_utils import get_current_user, require_admin

router = APIRouter(prefix='/devices', tags=['devices'])

@router.get('/', response_model=List[schemas.Device])
def list_devices(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(models.Device).all()

@router.post('/register_bulk', response_model=List[schemas.Device])
def register_bulk(devices: List[schemas.DeviceCreate], db: Session = Depends(get_db), admin = Depends(require_admin)):
    db_devices = [models.Device(**d.model_dump()) for d in devices]
    db.add_all(db_devices)
    db.commit()
    for d in db_devices:
        db.refresh(d)
    return db_devices

@router.put('/activate_bulk', response_model=List[schemas.Device])
def activate_bulk(device_ids: List[int], db: Session = Depends(get_db), admin = Depends(require_admin)):
    devices = db.query(models.Device).filter(models.Device.id.in_(device_ids)).all()
    if not devices:
        raise HTTPException(status_code=404, detail='No devices found to activate.')
    for device in devices:
        device.status = 'active'
    db.commit()
    return devices

@router.put('/update_bulk', response_model=List[schemas.Device])
def update_bulk(updates: List[schemas.DeviceUpdate], db: Session = Depends(get_db), admin = Depends(require_admin)):
    updated_devices = []
    for upd in updates:
        if upd.id is None:
            continue
        device = db.query(models.Device).filter(models.Device.id == upd.id).first()
        if not device:
            continue
        for field, value in upd.model_dump(exclude_unset=True).items():
            if field == 'id':
                continue
            setattr(device, field, value)
        db.commit()
        db.refresh(device)
        updated_devices.append(device)
    return updated_devices

@router.delete('/delete_bulk')
def delete_bulk(device_ids: List[int], db: Session = Depends(get_db), admin = Depends(require_admin)):
    devices = db.query(models.Device).filter(models.Device.id.in_(device_ids)).all()
    if not devices:
        raise HTTPException(status_code=404, detail='No devices found to delete.')
    for device in devices:
        db.delete(device)
    db.commit()
    return {'deleted_count': len(devices)}
