from fastapi import FastAPI

from . import models
from .database import engine
from .routers import user, auth, dialog, qna, wish, follow

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(dialog.router)
app.include_router(qna.router)
app.include_router(wish.router)
app.include_router(follow.router)
