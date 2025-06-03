from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import rechart, component

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(rechart.router)
app.include_router(component.router)
