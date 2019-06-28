from app import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now)
    updated_at = db.Column(db.DateTime, default=func.now)

    def __repr__(self):
        return f"User('{self.id}', '{self.public_id}', '{self.username}', '{self.email}', '{self.created_at}', '{self.updated_at}')"

class Vehicule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(128), unique=True, nullable=False)
    pac = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now)
    updated_at = db.Column(db.DateTime, default=func.now)

    def __repr__(self):
        return f"Vehicule('{self.id}', '{self.public_id}', '{self.pac}', '{self.created_at}', '{self.updated_at}')"

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text(1000), unique=True, nullable=False)
    stat_end_time = db.Column(db.Float)
    stat_percentage = db.Column(db.Float)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now)
    updated_at = db.Column(db.DateTime, default=func.now)

    def __repr__(self):
        return f"Model('{self.id}', '{self.path}', '{self.stat_end_time}', '{self.stat_percentage}', '{self.created_at}', '{self.updated_at}')"

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_key = db.Column(db.Text(1000), unique=True, nullable=False)
    address = db.Column(db.Text(1000), unique=True, nullable=False)
    passphrase = db.Column(db.Text(1000), unique=True)

    return f"Wallet('{self.id}', '{self.public_key}', '{self.address}', '{self.passphrase}')"

class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime, default=func.now)
    created_at = db.Column(db.DateTime, default=func.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now)

    return f"Contest('{self.id}', '{self.public_id}', '{self.name}', '{self.starts_at}', '{self.ends_at}', '{self.created_at}', '{self.updated_at}')"

class Race(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer) # foreign key ?
    user_id = db.Column(db.Integer) # foreign key ?
    vehicule_id = db.Column(db.Integer) # foreign key ?
    created_at = db.Column(db.DateTime, default=func.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now)
    stats = db.relatioship('Stats', backref='race', lazy=True)

    return f"Race('{self.id}', '{self.contest_id}', '{self.user_id}', '{self.vehicule_id}', '{self.created_at}', '{self.updated_at}')"

class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    value = db.Column(db.Integer)
    race_id = db.Column(db.Integer, db.foreignKey('user.id'), nullable=False) # foreign key

    return f"Stat('{self.id}', '{self.name}', '{self.value}', '{self.race_id}')"