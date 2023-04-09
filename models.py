import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Gender(Base):
    __tablename__ = 'gender'

    id_gender = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=10), nullable=False)

class Status(Base):
    __tablename__ = 'status'

    id_status = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=15), nullable=False)

class Clients(Base):
    __tablename__ = 'clients'

    id_client = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=40), nullable=False)
    link_profile = sq.Column(sq.String(length=255), nullable=False)
    city = sq.Column(sq.String(length=50), nullable=False)
    id_gender = sq.Column(sq.Integer, sq.ForeignKey('gender.id_gender'), nullable=False)

    gender = relationship(Gender, backref='clients')

class Users(Base):
    __tablename__ = 'users'

    id_user = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=15), nullable=False)
    last_name = sq.Column(sq.String(length=40), nullable=False)
    link_profile = sq.Column(sq.String(length=255), nullable=False)
    city = sq.Column(sq.String(length=50), nullable=False)
    id_gender = sq.Column(sq.Integer, sq.ForeignKey('gender.id_gender'), nullable=False)
    id_status = sq.Column(sq.Integer, sq.ForeignKey('status.id_status'), nullable=False)

    gender = relationship(Gender, backref='users')
    status = relationship(Status, backref='users')

class ClientsUsers(Base):
    __tablename__ = 'client_user'

    id_client_user = sq.Column(sq.Integer, primary_key=True)
    id_client = sq.Column(sq. Integer, sq.ForeignKey('clients.id_client'), nullable=False)
    id_user = sq.Column(sq. Integer, sq.ForeignKey('users.id_user'), nullable=False)

    clients_us = relationship(Clients, backref='client_user')
    users_cl = relationship(Users, backref='client_user')


class LinksFoto(Base):
    __tablename__ = 'links'

    id_link = sq.Column(sq.Integer, primary_key=True)
    link = sq.Column(sq.String(length=255), nullable=False)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('users.id_user'), nullable=False)

    users = relationship(Users, backref='links')

def create_tables(engine):
    #Base.metadata.drop_all(engine)  #для обнуления базы раскоментировать
    Base.metadata.create_all(engine)