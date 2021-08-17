import os
import configparser

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'alembic.ini'))

engine = create_engine(config['alembic']['sqlalchemy.url'])
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    tags = Column(String)
    creation_date = Column(DateTime, nullable=False)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    text = Column(String, unique=True, nullable=False)
    creation_date = Column(DateTime, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    creation_date = Column(DateTime, nullable=False)


class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    game = relationship('Game', backref='matches')
    player_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    player = relationship('User', backref='matches')
    score = Column(Float)

Base.metadata.create_all()
