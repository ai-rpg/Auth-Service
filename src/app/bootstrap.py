import uvicorn
from config import BUILD_VERSION,HOST, METRICS_PATH, NAME, HTTPPORT, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

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
authRepo = AuthRepository(couchbase_repository=couchbaseRepo)
authService = AuthService(auth_repository=authRepo)

@app.post("/")
def base_root(request: Request):
    pass

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
        data={"sub": user[form_data.username]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=UserModel)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(authService.get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserModel, Depends(authService.get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]



