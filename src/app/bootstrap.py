import uvicorn
import json
from config import (
    BUILD_VERSION,
    HOST,
    METRICS_PATH,
    NAME,
    HTTPPORT,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

from datetime import datetime, timedelta
from flask import Flask, request
from typing import Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from starlette_prometheus import metrics, PrometheusMiddleware
from metrics import PORT

from adapter.couchbase_repository import CouchbaseRepository
from adapter.auth_repository import AuthRepository
from services.auth_service import AuthService
from domain.token_model import TokenModel
from domain.user_model import UserModel
from domain.create_user_model import CreateUserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

PORT.info({"port": HTTPPORT})

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route(("/" + METRICS_PATH), metrics)

couchbaseRepo = CouchbaseRepository()
authRepo = AuthRepository(i_couchbase_repository=couchbaseRepo)
authService = AuthService(i_auth_repository=authRepo)


@app.get("/")
def base_root(request: Request):
    pass


@app.post("/createUser", response_model=TokenModel)
def create_user(new_user: Annotated[CreateUserModel, Depends()]):
    authService.create_user(new_user)


@app.post("/token", response_model=TokenModel)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = authService.create_access_token(
        data={"sub": json.dumps(user.__dict__)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=UserModel)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(authService.get_current_active_user)]
):
    return current_user


@app.get("/users/{username}")
async def get_user_by_username(username: str):
    return authService.get_user(username)


if __name__ == "__main__":
    uvicorn.run("bootstrap:app", host=HOST, port=int(HTTPPORT), log_level="info")
