from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import false, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

#Creating model classes
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String,nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String,nullable=False, unique=True)
    password = Column(String, nullable=False)
    inst_id = Column(Integer,ForeignKey("institutions.id", ondelete="CASCADE"),nullable=False)
    is_master = Column(Boolean,nullable=False,server_default="False")
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, nullable=False)
    dept_code = Column(String, nullable=False)
    dept_name = Column(String, nullable=False)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    UniqueConstraint(dept_code,user_id)

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, nullable=False)
    dept_id = Column(Integer,ForeignKey("departments.id", ondelete="CASCADE"),nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    time_limit = Column(Integer, nullable=False, server_default= '60')
    exam_date = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    exam_active = Column(Boolean,nullable=False,server_default="False")
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class ExamQstn(Base):
    __tablename__ = "exam_qstns"

    id = Column(Integer, primary_key=True, nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id",ondelete="CASCADE"),nullable=False)
    question = Column(String, nullable=False)
    ch1 = Column(String, nullable=False)
    ch2 = Column(String, nullable=False)
    ch3 = Column(String, nullable=False)
    ch4 = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    status = Column(Boolean, nullable=False , server_default="True")

class ExamAns(Base):
    __tablename__ = "exam_answers"

    id = Column(Integer, primary_key=True, nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id",ondelete="CASCADE"),nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    qstn_id = Column(Integer,ForeignKey("exam_qstns.id",ondelete="CASCADE"),nullable=False)
    stdnt_answer = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    UniqueConstraint(user_id,exam_id,qstn_id)
    
class ExamAtmpt(Base):
    __tablename__ = "exam_attempt"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id",ondelete="CASCADE"),nullable=False)
    exam_status = Column(String, nullable=False, server_default='assigned')
    UniqueConstraint(user_id,exam_id)