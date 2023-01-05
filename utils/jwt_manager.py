import os
from jwt import encode, decode
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv('SECRET_KEY')

def create_token(data: dict) -> str:
    token:str = encode(payload=data, key=KEY, algorithm='HS256')
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key=KEY, algorithms=['HS256'])
    return data