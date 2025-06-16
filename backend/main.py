from fastapi import FastAPI, HTTPException, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from backend.database import Base, engine, SessionLocal, init_db
from backend.models import User, Message
from backend.auth import hash_password_salted, verify_password_salted

from contextlib import contextmanager
import traceback

# Inicializa o banco (cria tabelas)
init_db()

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RegisterModel(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class MessageModel(BaseModel):
    user_id: int
    content: str

@app.get("/index", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register(data: RegisterModel, db: Session = Depends(get_db)):
    try:
        user_exists = db.query(User).filter(User.email == data.email).first()
        if user_exists:
            raise HTTPException(status_code=400, detail="Usuário já existe")

        new_user = User(
            name=data.name,
            email=data.email,
            password=hash_password_salted(data.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return RedirectResponse(url="/home?registered=1", status_code=303)

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        print("Erro no cadastro:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@app.post("/login")
def login(data: LoginModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password_salted(data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    return {
        "message": "Usuário logado com sucesso",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }

@app.get("/messages/{user_id}")
def get_messages(user_id: int, db: Session = Depends(get_db)):
    msgs = db.query(Message).filter(Message.owner_id == user_id).order_by(Message.created_at).all()
    return [
        {
            "id": m.id,
            "content": m.content,
            "user_name": m.owner.name,    # aqui corrigido para enviar o nome do usuário
            "created_at": m.created_at.isoformat()
        } for m in msgs
    ]

# --- WebSocket chat real-time ---

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            user_id = data.get("user_id")
            content = data.get("content")

            if not user_id or not content:
                await websocket.send_json({"error": "Dados inválidos"})
                continue

            db = SessionLocal()
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                await websocket.send_json({"error": "Usuário não encontrado"})
                db.close()
                continue

            new_msg = Message(content=content, owner_id=user.id)
            db.add(new_msg)
            db.commit()
            db.refresh(new_msg)

            # Corrigido: enviar o nome do usuário e a mensagem correta
            await manager.broadcast({
                "user_name": user.name,
                "content": new_msg.content,
                "created_at": new_msg.created_at.isoformat(),
            })

            db.close()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"message": "Usuário desconectou"})
