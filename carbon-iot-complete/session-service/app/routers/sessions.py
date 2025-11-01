from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix='/sessions', tags=['sessions'])

@router.post('/activate', response_model=schemas.SessionResponse)
def activate(payload: schemas.SessionCreate, db: Session = Depends(get_db)):
    sess = crud.create_or_activate_session(db, payload.device_id, metadata=payload.metadata)
    return sess

@router.post('/deactivate', response_model=schemas.SessionResponse)
def deactivate(payload: schemas.SessionCreate, db: Session = Depends(get_db)):
    sess = crud.deactivate_session(db, payload.device_id)
    if not sess:
        raise HTTPException(status_code=404, detail='session not found')
    return sess

@router.post('/ping', response_model=schemas.SessionResponse)
def ping(payload: schemas.PingPayload, db: Session = Depends(get_db)):
    sess = crud.ping_session(db, payload.device_id, timestamp=payload.timestamp)
    return sess

@router.get('/active', response_model=List[schemas.SessionResponse])
def list_active(db: Session = Depends(get_db)):
    return crud.get_active_sessions(db)

@router.get('/device/{device_id}', response_model=schemas.SessionResponse)
def get_by_device(device_id: int, db: Session = Depends(get_db)):
    sess = crud.get_session_by_device(db, device_id)
    if not sess:
        raise HTTPException(status_code=404, detail='session not found')
    return sess

@router.post('/restart', response_model=schemas.SessionResponse)
def restart(payload: schemas.SessionCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    sess = crud.restart_session(db, payload.device_id)
    if not sess:
        raise HTTPException(status_code=404, detail='session not found')
    return sess

@router.post('/deactivate_bulk', response_model=List[schemas.SessionResponse])
def deactivate_bulk(payload: schemas.BulkDeviceIds, db: Session = Depends(get_db)):
    sessions = crud.deactivate_bulk(db, payload.device_ids)
    return sessions
