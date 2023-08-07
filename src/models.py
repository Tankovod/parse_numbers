from sqlalchemy import Column, VARCHAR, BOOLEAN, INT, ForeignKey, BIGINT

from src.database import Base


class Number(Base):
    __tablename__ = 'number'

    number = Column(VARCHAR(15), nullable=False, unique=True)


class UserNumber(Base):
    __tablename__ = 'user_number'

    user_id = Column(BIGINT, ForeignKey('user.id'), nullable=False)
    number_id = Column(INT, ForeignKey('number.id'), nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(BIGINT, primary_key=True)
