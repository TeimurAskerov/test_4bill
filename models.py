from sqlalchemy import create_engine, Column, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime

engine = create_engine('sqlite:///app.db', echo=False)

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transaction'

    def __init__(self, amount):
        self.amount = amount
        self.time = datetime.now()

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    time = Column(TIMESTAMP)


def create_connection():
    connection = engine.connect()
    session = sessionmaker(engine)

    return connection, session()


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    connection, session = create_connection()

    r = session.query(Transaction).all()
    print(r)

    connection.close()
