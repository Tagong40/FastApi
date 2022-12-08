from pydantic import BaseModel
from typing import Optional


class PostModel(BaseModel):
    title: str
    body:  str


class ShowPost(PostModel):
    class Config:
        orm_mode = True
