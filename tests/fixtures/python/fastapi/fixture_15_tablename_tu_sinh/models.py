from sqlalchemy import Column, Integer, String

from base import NamedBase


class CaseNotes(NamedBase):
    # Ten bang that la "case_notes". Quy uoc "ten class viet thuong" cho ra
    # "casenotes" - sai.
    id = Column(Integer, primary_key=True)
    content = Column(String)


class Order(NamedBase):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
