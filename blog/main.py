from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import PostModel, ShowPost
from models import Base, Blog
from database import engine
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi.encoders import jsonable_encoder


Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blogs", status_code=status.HTTP_200_OK, response_model=List[ShowPost])
def blogs(db: Session = Depends(get_db)):
    query = db.query(Blog).all()
    return query


@app.post("/post/blogs", status_code=status.HTTP_201_CREATED)
def create(request: PostModel, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body)
    print(request)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def details(id, response: Response, db: Session = Depends(get_db)):
    get_blog = db.query(Blog).filter(Blog.id == id).first()

    if not get_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog not found")

    else:
        return get_blog


@app.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def destroy(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(
        Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")

    else:
        blog.delete(synchronize_session=False)
        db.commit()
        return {'message': "blog deleted success"}


@app.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: PostModel, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"blog not found")
    else:
        blog.update(jsonable_encoder(request))
        db.commit()
        response.status_code = status.HTTP_200_OK
        return {"message": "update success"}
