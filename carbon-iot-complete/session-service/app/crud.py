from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def create_or_activate_session(db: Session, device_id: int, metadata: str | None = None):
    sess = db.query(models.Session).filter(models.Session.device_id == device_id).first()
    if not sess:
        sess = models.Session(device_id=device_id, status='active', last_seen=datetime.utcnow(), metadata=metadata)
        db.add(sess)
    else:
        sess.status = 'active'
        sess.last_seen = datetime.utcnow()
        if metadata is not None:
            sess.metadata = metadata
    db.commit()
    db.refresh(sess)
    return sess

def deactivate_session(db: Session, device_id: int):
    sess = db.query(models.Session).filter(models.Session.device_id == device_id).first()
    if not sess:
        return None
    sess.status = 'inactive'
    db.commit()
    db.refresh(sess)
    return sess

def ping_session(db: Session, device_id: int, timestamp = None):
    sess = db.query(models.Session).filter(models.Session.device_id == device_id).first()
    if not sess:
        sess = models.Session(device_id=device_id, status='active')
        db.add(sess)
    sess.last_seen = timestamp or datetime.utcnow()
    sess.status = 'active'
    db.commit()
    db.refresh(sess)
    return sess

def get_active_sessions(db: Session):
    return db.query(models.Session).filter(models.Session.status == 'active').all()

def get_session_by_device(db: Session, device_id: int):
    return db.query(models.Session).filter(models.Session.device_id == device_id).first()

def restart_session(db: Session, device_id: int):
    sess = db.query(models.Session).filter(models.Session.device_id == device_id).first()
    if not sess:
        return None
    sess.status = 'restarting'
    sess.restarted_count = (sess.restarted_count or 0) + 1
    db.commit()
    sess.status = 'active'
    from datetime import datetime
    sess.last_seen = datetime.utcnow()
    db.commit()
    db.refresh(sess)
    return sess

def deactivate_bulk(db: Session, device_ids: list[int]):
    sessions = db.query(models.Session).filter(models.Session.device_id.in_(device_ids)).all()
    for s in sessions:
        s.status = 'inactive'
    db.commit()
    return sessions
