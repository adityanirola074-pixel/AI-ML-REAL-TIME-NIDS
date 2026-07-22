from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///database.db")

Base = declarative_base()

class AttackLog(Base):

    __tablename__ = "attacks"

    id = Column(Integer, primary_key=True)

    time = Column(String)

    src_ip = Column(String)

    dst_ip = Column(String)

    protocol = Column(String)

    attack = Column(String)

    confidence = Column(Float)

    risk = Column(String)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)