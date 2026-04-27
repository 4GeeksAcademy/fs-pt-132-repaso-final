from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class UserGroup(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    #conectar con tablas:
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))   
    #m-m
    user: Mapped["User"] = relationship(back_populates="groups")
    group: Mapped["Group"] = relationship(back_populates="users")
    #tener columnas propias de la tabla
    rating: Mapped[int] = mapped_column(Integer())


    def serialize(self):
        return{
            "id": self.id,
            "user": {
                "email": self.user.email
            },
            "group": {
                "name": self.group.name
            }
        }


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    #1-1
    profile: Mapped["Profile"] = relationship(back_populates="user") #devuelve UN obj
    #1-m
    posts: Mapped[List["Post"]] = relationship(back_populates="author") #no devuelve un obj, sino una coleccion de objs
    #m-m
    groups: Mapped[List["UserGroup"]] = relationship(back_populates="user") #no devuelve un obj, sino una coleccion de objs


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            #devolviendo un solo obj
            "profile": self.profile.serialize() if self.profile else None,
            #devolviendo una coleccion de datos que estan dentro de una coleccion
            "posts": [post.serialize() for post in self.posts] if self.posts else None,
            # do not serialize the password, its a security breach
            "groups": [g.serialize() for g in self.groups] if self.groups else None
        }
    
class Profile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[str] = mapped_column(Text())
    #conectando con tabla User
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    #1-1
    user: Mapped["User"] = relationship(back_populates="profile")

    def serialize(self):
        return{
            "id": self.id,
            "bio": self.bio,
            "user": {
                "email": self.user.email 
            } if self.user else None
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    #conectando con tabla User
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    #1-m
    author: Mapped["User"] = relationship(back_populates="posts")

    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
            "author": {
                "email": self.author.email if self.author else None 
            }
        }

class Group(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    #m-m
    users: Mapped[List["UserGroup"]] = relationship(back_populates="group") #no devuelve un obj, sino una coleccion de objs

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "users": [u.serialize() for u in self.users] if self.users else None

        }

