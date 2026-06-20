import streamlit as st
from sqlalchemy import create_engine

def get_connection():
    # Явный путь
    db_url = st.secrets["db_url"]
    engine = create_engine(db_url,
    pool_pre_ping=True,      
    pool_recycle=300,        # пересоздает соединение каждые 5 минут
    pool_size=5,             # держит небольшое количество соединений
    max_overflow=0)
    return engine

