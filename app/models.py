from typing import Optional

from flask import url_for
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

from flask_login import UserMixin

import sqlalchemy as sa
import sqlalchemy.orm as so


@login.user_loader
def load_user(id):
    return db.session.query(User).get(id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    trucks: so.Mapped[Optional['Truck']] = so.relationship('Truck', backref='user')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.username}'

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'trucks': url_for('api.get_trucks', id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        return data


class Transport(db.Model):
    __abstract__ = True

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    @staticmethod
    def get_transport_type(transport_type):
        if transport_type == 'trucks':
            return Truck
        elif transport_type == 'trailers':
            return Trailer
        else:
            raise BadRequest('Invalid transport type. Available types: trucks, trailers')

    def to_dict(self, include_email=False):
        raise NotImplementedError('Subclasses should implement to_dict method')


class Truck(Transport):
    __tablename__ = 'trucks'

    truck_number: so.Mapped[str] = so.mapped_column(sa.String(9), index=True, unique=True)
    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, sa.ForeignKey('users.id'))

    trailer: so.Mapped[Optional['Trailer']] = so.relationship('Trailer', back_populates='truck', uselist=False)

    def __repr__(self):
        return f'Truck {self.truck_number} | Trailer {self.trailer.trailer_number}'

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'truck_number': self.truck_number,
            'user_id': self.user_id,
            '_links': {
                'self': url_for('api.get_transport', transport_type='trucks', id=self.id),
                'trailer': url_for('api.get_transport', transport_type='trailers', id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        return data


class Trailer(Transport):
    __tablename__ = 'trailers'

    trailer_number: so.Mapped[str] = so.mapped_column(sa.String(9), index=True, unique=True)
    truck_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, sa.ForeignKey('trucks.id', ondelete='SET NULL'))

    truck: so.Mapped[Optional[Truck]] = so.relationship('Truck', back_populates='trailer', uselist=False)

    def __repr__(self):
        return f'Trailer {self.trailer_number}'

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'trailer_number': self.trailer_number,
            'truck_id': self.truck_id,
            '_links': {
                'self': url_for('api.get_transport', transport_type='trailers', id=self.id),
                'truck': url_for('api.get_transport', transport_type='trucks', id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        return data
