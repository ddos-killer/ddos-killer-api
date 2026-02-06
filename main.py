from fastapi import FastAPI
from controllers import engine, config, blacklist, events

app = FastAPI(title="DDoS Defense API")

app.include_router(engine.router)
app.include_router(config.router)
app.include_router(blacklist.router)
app.include_router(events.router)
