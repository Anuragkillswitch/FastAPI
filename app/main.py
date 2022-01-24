from ast import Raise
from logging import raiseExceptions
from typing import Optional
from xmlrpc.client import boolean
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randint, randrange
import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session




models.Base.metadata.create_all(bind=engine)


app=FastAPI()



        
        
        

while True:
    
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='clear',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was successsful")
        break
    except Exception as error:
        print("Connecting to Database failed")  
        print("The error was",error) 
        time.sleep(3)


my_posts=[{"title":"Title of 1st post","content":"Content of 1st post","id":1},
          {"title":"My favourite food","content":"I love Nachos","id":2}]

class Post(BaseModel):
    title:str
    content:str    
    published:Optional[boolean]=True


def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
        
#Testing out the DB connection and disconnection


    


def findPost(id):
    for p in my_posts:
        if p["id"]==id:
            return p
    return -1        

def deletePost(id):
    for i,p in enumerate(my_posts):
        if p["id"]==id:
          my_posts.pop(i)
          return "Post Successfully Deleted"
    return f"Post with ID {id} not found"  
       
    



@app.get("/")
def root():
    return {"message": "Hey There! Welcome to the API!"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    return {"data":posts}

@app.get("/sqlalchemy")
def sql_alchemyTest( db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
                                # /\ Until we run this last method (.all)
                                # this is just a SQL query that hasn't been run yet
    return {"Data ":posts}

    


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post,db: Session = Depends(get_db)):
    
    new_post=models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"Data ":new_post}




#Retrieving a singular post
@app.get("/posts/{id}")
def get_post(id : int,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post=cursor.fetchone()
    # # post=findPost(id)
    
    post=db.query(models.Post).filter(models.Post.id==id).first()
    
    #.filter is equivalent to where
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return {"post_detail": post }

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(id,))
    # post=cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id)
    
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=post)
        
    post.delete(synchronize_session=False)    
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)    


@app.put("/posts/{id}")
def update_post(id : int,post: Post):
    cursor.execute("""UPDATE posts SET title= %s,content=%s,published=%s WHERE id= %s RETURNING *""",(post.title,post.content,post.published,id))
    updated_post=cursor.fetchone()
    conn.commit()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
      
    return {"data":updated_post}


