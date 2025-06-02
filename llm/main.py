from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.rechart import generate_ui

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


@app.get("/")
def hello():
    return {"message": "hello"}


@app.get("/generative-ui")
def generative_ui():
    response = generate_ui()
    return {"message": response}
