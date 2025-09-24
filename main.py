from fastapi import FastAPI
from app import users, articles, comments # Убедитесь, что создали все файлы роутеров
from app.database import engine
from app import models

# Создание таблиц в БД (Alembic является предпочтительным способом в продакшене)
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключение роутеров
app.include_router(users.router)
app.include_router(articles.router)
# app.include_router(comments.router)

@app.get("/")
def root():
    return {"message": "Hello world"}
