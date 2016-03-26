from sqlalchemy import *
from sqlalchemy.ext.declarative import *

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


class User(Base):
    # must have
    __tablename__ = 'users'

    # at lease one primary key column
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name={1}, fullname={2}, password={3})>".format(
            self.name, self.fullname, self.password)
