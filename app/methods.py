from sqlalchemy.orm import Session
from slugify import slugify
from . import models, schemas, security

# --- Пользователи ---
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Статьи ---
def get_article_by_slug(db: Session, slug: str):
    return db.query(models.Article).filter(models.Article.slug == slug).first()

def create_article(db: Session, article: schemas.ArticleCreate, user_id: int):
    slug = slugify(article.title)
    # Проверка на уникальность slug и добавление суффикса при необходимости
    original_slug = slug
    counter = 1
    while db.query(models.Article).filter(models.Article.slug == slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1
    
    db_article = models.Article(**article.dict(), author_id=user_id, slug=slug)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

# ... (другие CRUD функции для статей и комментариев будут в роутерах для простоты)