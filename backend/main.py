from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import chat, customer, cpr_registry, health, upload_id

app = FastAPI(title="Danske Bank Onboarding API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(customer.router)      
app.include_router(cpr_registry.router)
app.include_router(upload_id.router)
