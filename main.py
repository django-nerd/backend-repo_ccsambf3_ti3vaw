import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List

from database import db, create_document, get_documents
from schemas import Announcement, Event, Contactmessage

app = FastAPI(title="Pacific Christian School API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Pacific Christian School API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                response["collections"] = db.list_collection_names()
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# ============ Announcements ============
@app.get("/api/announcements", response_model=List[Announcement])
def list_announcements():
    docs = get_documents("announcement", limit=50)
    for d in docs:
        d.pop("_id", None)
    return docs

@app.post("/api/announcements")
def create_announcement(payload: Announcement):
    data = payload.model_dump()
    if not data.get("published_at"):
        data["published_at"] = datetime.utcnow()
    doc_id = create_document("announcement", data)
    return {"id": doc_id}

# ============ Events ============
@app.get("/api/events", response_model=List[Event])
def list_events():
    docs = get_documents("event", limit=100)
    for d in docs:
        d.pop("_id", None)
    return docs

@app.post("/api/events")
def create_event(payload: Event):
    doc_id = create_document("event", payload)
    return {"id": doc_id}

# ============ Contact ============
class ContactResponse(BaseModel):
    ok: bool

@app.post("/api/contact", response_model=ContactResponse)
def submit_contact(payload: Contactmessage):
    create_document("contactmessage", payload)
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
