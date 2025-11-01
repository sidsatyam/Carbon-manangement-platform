Carbon IoT Complete Package
===========================

This archive contains:
 - device-service: FastAPI device management with JWT auth, bulk ops
 - session-service: FastAPI device session manager
 - simulator: lightweight async simulator to exercise APIs
 - docker-compose.yml to run db + pgadmin + api + session + simulator
 - Jenkinsfile, Makefile, rpm spec and tests

Quick start:
  1. Edit .env to set secure credentials.
  2. docker compose up --build
  3. API docs: http://<host>:8000/docs
  4. Session service docs: http://<host>:8010/docs
  5. pgAdmin: http://<host>:5050
