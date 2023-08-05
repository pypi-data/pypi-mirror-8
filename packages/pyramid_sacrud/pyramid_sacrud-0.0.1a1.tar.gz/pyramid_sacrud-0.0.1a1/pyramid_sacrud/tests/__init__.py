# -*- coding: utf-8 -*-
"""
action.py tests
"""

import os

from sqlalchemy import orm, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, Enum, Float, Integer, String, Text
from zope.sqlalchemy import ZopeTransactionExtension

from sacrud.exttype import FileStore

Base = declarative_base()

DBSession = orm.scoped_session(
    orm.sessionmaker(extension=ZopeTransactionExtension(),
                     expire_on_commit=False))

DIRNAME = os.path.dirname(__file__)
PHOTO_PATH = os.path.join(DIRNAME)


DB_FILE = os.path.join(os.path.dirname(__file__), 'test.sqlite')
TEST_DATABASE_CONNECTION_STRING = 'sqlite:///%s' % DB_FILE


class MockCGIFieldStorage(object):
    pass


association_table = Table('association', Base.metadata,
                          Column('group_id', Integer, ForeignKey('group.id')),
                          Column('user_id', Integer, ForeignKey('user.id'))
                          )


class Groups(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship("User", secondary=association_table)


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String, info={'verbose_name': 'user password'})
    sex = Column(Enum('male',
                      'female',
                      'alien',
                      'unknown', name="sex"))

    groups = relationship("Groups", secondary=association_table)

    def __init__(self, name, fullname, password, sex='unknown'):
        self.name = name
        self.fullname = fullname
        self.password = password
        self.sex = sex


class Profile(Base):

    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship(User, backref=backref("profile", lazy="joined"))
    phone = Column(String)
    cv = Column(Text)
    married = Column(Boolean)
    salary = Column(Float)
    photo = Column(FileStore(path="/assets/photo", abspath=PHOTO_PATH))
