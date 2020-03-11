from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from flask_login import UserMixin
Base=declarative_base()
class Register(Base,UserMixin):
	 __tablename__="register"
	 id = Column(Integer,primary_key=True)
	 name=Column(String(20),nullable=False)
	 email=Column(String(100),nullable=False)
	 phno = Column(Integer,nullable=False)
	 password=Column(String(30),nullable=False)
engine=create_engine("sqlite:///jntua.db") 
Base.metadata.create_all(engine)
print("database created")