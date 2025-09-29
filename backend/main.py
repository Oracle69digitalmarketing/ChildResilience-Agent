# backend/app/main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.endpoints import (
    report,
    shelters,
    shelters_admin,
    auth,
    incidents,
)
from backend.app.services import realtime_dashboard

app = FastAPI(
    title="ChildResilience-Agent",
    description="Child-centered climate resilience platform for reporting, analyzing, and routing incidents in real-time",
    version="1.0.0",
)

# --- CORS setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Routes ---
app.include_router(report.router, prefix="/api")
app.include_router(shelters.router, prefix="/api")
app.include_router(shelters_admin.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(incidents.router, prefix="/api")

# --- WebSocket Endpoint for Real-time Dashboard ---
@app.websocket("/ws/dashboard")
async def dashboard_ws(websocket: WebSocket):
    await realtime_dashboard.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except Exception:
        await realtime_dashboard.disconnect(websocket)

# --- Startup & Shutdown Events ---
@app.on_event("startup")
async def startup_event():
    print("ChildResilience-Agent Backend Started")

@app.on_event("shutdown")
async def shutdown_event():
    print("ChildResilience-Agent Backend Shutting Down")
