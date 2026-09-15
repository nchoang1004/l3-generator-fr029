from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TimestampedBase(Base):
    __abstract__ = True

    def touch(self):
        return None
