import logging

from fastapi import FastAPI
from jose import jwt
from pydantic import BaseModel
from time import time
from chatter_base.settings import load_settings, SettingsError

app = FastAPI()

try:
    settings = load_settings()
except SettingsError as error:
    logging.error(error)


class UserCredentials(BaseModel):
    login: str
    password: str


@app.post("/register_user")
def register_user():
    object_for_encode = {
        "user_uuid": "123",
        "time_created": time()
    }

    return jwt.encode(object_for_encode, settings.secret_key)
