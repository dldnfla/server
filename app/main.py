from fastapi import FastAPI

from . import models
from .database import engine
from .routers import user, auth, dialog,upload,qna

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(dialog.router)
app.include_router(qna.router)
app.include_router(upload.router)