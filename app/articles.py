from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, security, models
from app.database import get_db

router = APIRouter(prefix="/api/articles", tags=["Articles"])

@router.post("", response_model=schemas.ArticleInDB, status_code=status.HTTP_201_CREATED)
def create_new_article(article: schemas.ArticleCreate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    return crud.create_article(db=db, article=article, user_id=current_user.id)

@router.get("", response_model=List[schemas.ArticleInDB])
def get_all_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all()
    return articles

@router.get("/{slug}", response_model=schemas.ArticleInDB)
def get_article_by_slug(slug: str, db: Session = Depends(get_db)):
    db_article = crud.get_article_by_slug(db, slug=slug)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

# ... PUT и DELETE эндпоинты реализуются аналогично, с проверкой,
# что current_user.id == db_article.author_id