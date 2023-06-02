from config import BUILD_VERSION, METRICS_PATH, NAME, HTTPPORT

from flask import Flask, request
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from starlette_prometheus import metrics, PrometheusMiddleware
from metrics import PORT

from adapter.couchbase_repository import CouchbaseRepository
from adapter.auth_repository import AuthRepository
from services.auth_service import AuthService

PORT.info({"port": HTTPPORT})

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origains=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route(("/" + METRICS_PATH), metrics)

couchbaseRepo = CouchbaseRepository()
authRepo = AuthRepository(mangement_api_token, couchbase_repository=couchbaseRepo)
authService = AuthService(auth_repository=authRepo)

@app.post("/")
def base_root(request: Request):
    pass


if __name__ == "__main__":
    unvicorn.run("main:app", host=HOST, port=int(HTTPPORT), log_level="info")

