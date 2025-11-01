from fastapi import FastAPI
from app.database import engine, Base
from app.routers import devices
from app import auth
from fastapi.middleware.cors import CORSMiddleware

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Carbon IoT Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(auth.router)
app.include_router(devices.router)

@app.get('/')
def root():
    return {'message': 'Carbon IoT Service running'}
