import os
from fastapi import FastAPI, HTTPException, Body, Response
from pydantic import BaseModel

app = FastAPI()

USERS_DB_FILE = "users.txt"
MESSAGES_DB_FILE = "messages.txt"

class USER(BaseModel):
    username: str
    password: str

def read_users_db():
    users_db = {}
    try:
        with open(USERS_DB_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(":")
                users_db[username] = password
    except FileNotFoundError:
        pass
    return users_db

def write_to_users_db(username: str, password: str):
    with open(USERS_DB_FILE, "a") as file:
        file.write(f"{username}:{password}\n")

@app.post("/register")
async def register(user: USER = Body(...)):
    if user.username.isupper() or len(user.username) > 15:
        raise HTTPException(status_code=400, detail="아이디가 올바르지 않습니다.")

    if len(user.password) < 8 or len(user.password) >= 20:
        raise HTTPException(status_code=400, detail="비밀번호가 올바르지 않습니다.")

    users_db = read_users_db()
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="중복된 아이디는 존재할 수 없습니다.")

    write_to_users_db(user.username, user.password)
    return {"success": True}

@app.post("/login")
async def login(user: USER = Body(...)):
    users_db = read_users_db()
    if user.username in users_db and users_db[user.username] == user.password:
        response = Response(content='{"success": true}')
        response.set_cookie(key="username", value=user.username)
        return response
    else:
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호를 확인하세요")
