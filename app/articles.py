from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, security, models
from app.database import get_db

router = APIRouter(prefix="/api/articles", tags=["Articles"])

@router.post("", response_model=schemas.ArticleInDB, status_code=status.HTTP_201_CREATED)
def create_new_article(
    article: schemas.ArticleCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    return crud.create_article(db=db, article=article, user_id=current_user.id)

@router.get("", response_model=List[schemas.ArticleInDB])
def get_all_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).order_by(models.Article.created_at.desc()).all()
    return articles

@router.get("/{slug}", response_model=schemas.ArticleInDB)
def get_single_article(slug: str, db: Session = Depends(get_db)):
    db_article = crud.get_article_by_slug(db, slug=slug)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.put("/{slug}", response_model=schemas.ArticleInDB)
def update_article(
    slug: str, 
    article_update: schemas.ArticleCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_article = crud.get_article_by_slug(db, slug=slug)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if db_article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this article")

    update_data = article_update.dict(exclude_unset=True)
    
    if 'title' in update_data and db_article.title != update_data['title']:
        db_article.slug = crud.generate_unique_slug(db, update_data['title'])

    for key, value in update_data.items():
        setattr(db_article, key, value)

    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    slug: str, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_article = crud.get_article_by_slug(db, slug=slug)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")

    if db_article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this article")
    
    db.delete(db_article)
    db.commit()
    return
