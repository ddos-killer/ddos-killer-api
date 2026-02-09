from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import engine, config, blacklist, events

app = FastAPI(title="DDoS Defense API")

# CORS configuration to allow requests from the frontend application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(engine.router)
app.include_router(config.router)
app.include_router(blacklist.router)
app.include_router(events.router)