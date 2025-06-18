from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import rechart
from api.endpoints import component
from api.endpoints import ui_component
from api.endpoints import iframe_component

app = FastAPI()

origins = ["http://localhost:3000", "http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(rechart.router, prefix="/rechart", tags=["Chart Generation"])
app.include_router(component.router, prefix="/component", tags=["Component Generation"])
app.include_router(ui_component.router, prefix="/ui_component", tags=["UI Component"])
app.include_router(iframe_component.router, prefix="/iframe", tags=["UI Component"])
