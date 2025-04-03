import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "any_key"
