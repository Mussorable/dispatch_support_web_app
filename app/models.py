from typing import Optional
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


class Truck(db.Model):
    __tablename__ = 'trucks'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    truck_number: so.Mapped[str] = so.mapped_column(sa.String(9), index=True, unique=True)
    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, sa.ForeignKey('users.id'))

    trailer: so.Mapped[Optional['Trailer']] = so.relationship('Trailer', back_populates='truck', uselist=False)

    def __repr__(self):
        return f'Truck {self.truck_number} | Trailer {self.trailer.trailer_number}'


class Trailer(db.Model):
    __tablename__ = 'trailers'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    trailer_number: so.Mapped[str] = so.mapped_column(sa.String(9), index=True, unique=True)
    truck_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, sa.ForeignKey('trucks.id', ondelete='SET NULL'))

    truck: so.Mapped[Optional[Truck]] = so.relationship('Truck', back_populates='trailer', uselist=False)

    def __repr__(self):
        return f'Trailer {self.trailer_number}'
