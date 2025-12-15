from config import db

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # one-to-one relationship to Address (address stored in separate table)
    address = db.relationship('Address', uselist=False, back_populates='contact', cascade='all, delete-orphan')

    def json(self):
        addr = None
        if self.address:
            addr = self.address.json()
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'address': addr
        }


class Address(db.Model):
    __tablename__ = 'addresses'
    # Primary key for the address row
    id = db.Column(db.Integer, primary_key=True)
    # Explicit contact_id foreign key (matches existing DB schema)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False, unique=True)
    # store just the address text (nullable allowed)
    address = db.Column(db.String(500), unique=False, nullable=True)

    # relationship back to Contact (one-to-one)
    contact = db.relationship('Contact', back_populates='address', uselist=False)

    def json(self):
        return {
            'id': self.id,
            'address': self.address
        }