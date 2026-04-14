from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db
from ..redis_client import get_cache, set_cache, delete_cache

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # Create cache key based on query parameters
    cache_key = f"posts:limit={limit}:skip={skip}:search={search}"
    
    # Try to get from cache
    cached_posts = get_cache(cache_key)
    if cached_posts:
        print(f"✅ CACHE HIT - Returning {len(cached_posts)} posts from Redis")
        return cached_posts
    
    print(f"❌ CACHE MISS - Querying database")
    
    # If not in cache, query database
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    
    # Convert to dict for caching
    posts_dict = [
        {
            "Post": {
                "id": post.Post.id,
                "title": post.Post.title,
                "content": post.Post.content,
                "published": post.Post.published,
                "created_at": post.Post.created_at.isoformat(),
                "owner_id": post.Post.owner_id,
                "owner": {
                    "id": post.Post.owner.id,
                    "email": post.Post.owner.email,
                    "created_at": post.Post.owner.created_at.isoformat(),
                }
            },
            "votes": post.votes
        }
        for post in posts
    ]
    
    # Cache for 5 minutes
    set_cache(cache_key, posts_dict, expire=300)
    print(f"💾 Cached {len(posts_dict)} posts in Redis")
    
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # Invalidate posts cache
    delete_cache("posts:*")
    
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action.",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    
    # Invalidate posts cache
    delete_cache("posts:*")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action.",
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    # Invalidate posts cache
    delete_cache("posts:*")
    
    return post
