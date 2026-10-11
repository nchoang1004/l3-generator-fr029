from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///shop.db")
Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, nullable=False)


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, primary_key=False, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=False, nullable=True)


def load_items():
    return []


Base.metadata.create_all(engine)
