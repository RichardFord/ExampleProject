from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy import String


Base = declarative_base()


class People(Base):

    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(32))
    last_name = Column(String(32))

    @property
    def response(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
