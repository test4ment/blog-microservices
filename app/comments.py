from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, security, models
from app.database import get_db

router = APIRouter(prefix="/api/articles/{slug}/comments", tags=["Comments"])

@router.post("", response_model=schemas.CommentInDB, status_code=status.HTTP_201_CREATED)
def add_comment_to_article(
    slug: str,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    article = crud.get_article_by_slug(db, slug=slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return crud.create_comment(db=db, comment=comment, article_id=article.id, author_id=current_user.id)

@router.get("", response_model=List[schemas.CommentInDB])
def get_comments_from_article(slug: str, db: Session = Depends(get_db)):
    article = crud.get_article_by_slug(db, slug=slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return crud.get_comments_for_article(db=db, article_id=article.id)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    slug: str,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    comment = crud.get_comment_by_id(db, comment_id=comment_id)

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.article.slug != slug:
        raise HTTPException(status_code=404, detail="Comment not found on this article")
        
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(comment)
    db.commit()
    return
