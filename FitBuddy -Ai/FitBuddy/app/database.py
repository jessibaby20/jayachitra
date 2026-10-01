from datetime import datetime, timezone
from sqlalchemy import create_engine, String, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, Session
from .config import DATABASE_URL
connect_args={"check_same_thread":False} if DATABASE_URL.startswith("sqlite") else {}
engine=create_engine(DATABASE_URL,connect_args=connect_args,future=True)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False,expire_on_commit=False)
class Base(DeclarativeBase): pass
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id:Mapped[str]=mapped_column(String(100),unique=True,index=True)
    name:Mapped[str]=mapped_column(String(120))
    age:Mapped[int]=mapped_column(Integer)
    weight:Mapped[float]=mapped_column(Float)
    goal:Mapped[str]=mapped_column(String(100))
    intensity:Mapped[str]=mapped_column(String(20))
    created_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
    plans:Mapped[list["Plan"]]=relationship(back_populates="user",cascade="all, delete-orphan")
class Plan(Base):
    __tablename__="plans"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    original_plan:Mapped[str]=mapped_column(Text)
    updated_plan:Mapped[str|None]=mapped_column(Text,nullable=True)
    nutrition_tip:Mapped[str]=mapped_column(Text)
    feedback:Mapped[str|None]=mapped_column(Text,nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
    user:Mapped[User]=relationship(back_populates="plans")
def init_db(): Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
def save_user(db:Session,data):
    u=db.query(User).filter(User.user_id==data.user_id).first()
    if u:
        for k in ["name","age","weight","goal","intensity"]: setattr(u,k,getattr(data,k))
    else:
        u=User(**data.model_dump()); db.add(u)
    db.commit(); db.refresh(u); return u
def save_plan(db,user,workout_plan,nutrition_tip):
    p=Plan(user_id=user.id,original_plan=workout_plan,nutrition_tip=nutrition_tip); db.add(p); db.commit(); db.refresh(p); return p
def update_plan(db,plan,revised_plan,feedback):
    plan.updated_plan=revised_plan; plan.feedback=feedback; plan.updated_at=datetime.now(timezone.utc)
    db.commit(); db.refresh(plan); return plan
