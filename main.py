from flask import request, jsonify
from config import app, db
from models import Contact, Address

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.json(), contacts))
    return jsonify({"contacts": json_contacts}), 200

@app.route('/create_contact', methods=['POST'])
def create_contact():
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    email = request.json.get('email')
    address_text = request.json.get('address')  # optional, can be string
    if not first_name or not last_name or not email:
        return jsonify({"error": "Missing required fields"}), 400
    try:
        # create contact and flush to obtain an id
        new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
        db.session.add(new_contact)
        db.session.flush()  # assigns new_contact.id without committing
        # attach address if provided (set contact_id explicitly to match DB schema)
        if address_text:
            new_address = Address(contact_id=new_contact.id, address=address_text)
            db.session.add(new_address)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    return jsonify({"message":"User created!"}), 201

@app.route('/update_contact/<int:user_id>', methods=['PATCH'])
def update_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({"message": "User not found"}), 404
    data = request.json
    contact.first_name = data.get('firstName', contact.first_name)
    contact.last_name = data.get('lastName', contact.last_name)
    contact.email = data.get('email', contact.email)
    # update address if provided
    address_text = data.get('address')
    if address_text is not None:
        if contact.address:
            contact.address.address = address_text
        else:
            # create Address row with explicit contact_id to match DB
            new_address = Address(contact_id=contact.id, address=address_text)
            db.session.add(new_address)
            contact.address = new_address
    db.session.commit()
    return jsonify({"message": "User updated"}), 200


@app.route('/delete_contact/<int:user_id>', methods=['DELETE'])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
