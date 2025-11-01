from fastapi import FastAPI
from app.database import engine, Base
from app.routers import sessions

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Carbon Session Service')

app.include_router(sessions.router)

@app.get('/')
def root():
    return {'message': 'Carbon Session Service up'}
