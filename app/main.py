from fastapi import FastAPI

from . import models
from .database import engine
from .routers import user, auth, dialog, qna, wish,upload,qna
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
 
origins = [
    "http://localhost:3000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # 클라이언트의 URL
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(dialog.router)
app.include_router(qna.router)
app.include_router(upload.router)
app.include_router(wish.router)