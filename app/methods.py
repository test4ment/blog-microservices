from sqlalchemy.orm import Session
from slugify import slugify
from . import models, schemas, security

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


def get_article_by_slug(db: Session, slug: str):
    return db.query(models.Article).filter(models.Article.slug == slug).first()

def generate_unique_slug(db: Session, title: str) -> str:
    """Генерирует уникальный slug для статьи."""
    slug = slugify(title)
    original_slug = slug
    counter = 1
    while db.query(models.Article).filter(models.Article.slug == slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1
    return slug

def create_article(db: Session, article: schemas.ArticleCreate, user_id: int):
    slug = generate_unique_slug(db, article.title)
    db_article = models.Article(**article.dict(), author_id=user_id, slug=slug)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_comments_for_article(db: Session, article_id: int):
    return db.query(models.Comment).filter(models.Comment.article_id == article_id).order_by(models.Comment.created_at.desc()).all()

def create_comment(db: Session, comment: schemas.CommentCreate, article_id: int, author_id: int):
    db_comment = models.Comment(**comment.dict(), article_id=article_id, author_id=author_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment_by_id(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()
