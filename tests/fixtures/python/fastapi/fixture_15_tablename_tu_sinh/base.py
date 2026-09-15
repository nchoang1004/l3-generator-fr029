# Dung cach cua Netflix/dispatch: lop co so tu sinh __tablename__ luc chay bang
# cach tach ten class theo chu hoa. Khong the doc quy tac nay bang cu phap.
import re

from sqlalchemy.orm import declarative_base, declared_attr


def resolve_table_name(name):
    names = re.split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


Base = declarative_base()


class NamedBase(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return resolve_table_name(cls.__name__)
