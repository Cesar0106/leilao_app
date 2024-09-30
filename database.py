import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = st.secrets["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Leilao(Base):
    __tablename__ = 'leiloes'
    id = Column(Integer, primary_key=True)
    item = Column(String, nullable=False)
    descricao = Column(String)
    valor_minimo = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True)  
    lances = relationship('Lance', back_populates='leilao')

class Lance(Base):
    __tablename__ = 'lances'
    id = Column(Integer, primary_key=True)
    leilao_id = Column(Integer, ForeignKey('leiloes.id'))
    usuario = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    leilao = relationship('Leilao', back_populates='lances')

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
