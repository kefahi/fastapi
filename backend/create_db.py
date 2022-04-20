""" Create database example """

from utils.db import User, engine, Base, db

Base.metadata.create_all(bind=engine)
user = User(name="Ali baba", email="Hello6", password="World")
db.add(user)
db.commit()
db.refresh(user)
print(user.id, user.name, user.email)
