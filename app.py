from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Organization, Donation, Story, Beneficiary, InventoryItem
from datetime import datetime
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'})

# User routes
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(
        name=data['name'],
        email=data['email'],
        password=data['password'],  # In production, hash the password
        role=data['role']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:  # In production, verify hashed password
        token = jwt.encode(
            {'user_id': user.id, 'email': user.email},
            app.config['JWT_SECRET_KEY']
        )
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        })
    return jsonify({'error': 'Invalid credentials'}), 401

# Organization routes
@app.route('/organizations', methods=['GET', 'POST'])
def organizations():
    if request.method == 'POST':
        data = request.json
        org = Organization(
            name=data['name'],
            description=data['description'],
            user_id=data['userId']
        )
        db.session.add(org)
        db.session.commit()
        return jsonify({'message': 'Organization created successfully'})
    
    orgs = Organization.query.all()
    return jsonify([{
        'id': org.id,
        'name': org.name,
        'description': org.description,
        'status': org.status
    } for org in orgs])

# Donation routes
@app.route('/donations', methods=['POST'])
def create_donation():
    data = request.json
    donation = Donation(
        amount=data['amount'],
        frequency=data['frequency'],
        payment_method=data['paymentMethod'],
        organization_id=data['organizationId'],
        is_anonymous=data.get('isAnonymous', False)
    )
    
    if data.get('donorId') and not donation.is_anonymous:
        donor = User.query.get(data['donorId'])
        if donor:
            donation.donors.append(donor)
    
    db.session.add(donation)
    db.session.commit()
    return jsonify({'message': 'Donation recorded successfully'})

# Story routes
@app.route('/stories', methods=['GET', 'POST'])
def stories():
    if request.method == 'POST':
        data = request.json
        story = Story(
            title=data['title'],
            content=data['content'],
            image_url=data.get('image_url'),
            organization_id=data['organization_id']
        )
        db.session.add(story)
        db.session.commit()
        return jsonify({'message': 'Story posted successfully'})
    
    stories = Story.query.all()
    return jsonify([{
        'id': story.id,
        'title': story.title,
        'content': story.content,
        'image_url': story.image_url,
        'created_at': story.created_at.isoformat()
    } for story in stories])

# Beneficiary routes
@app.route('/beneficiaries', methods=['GET', 'POST'])
def beneficiaries():
    if request.method == 'POST':
        data = request.json
        beneficiary = Beneficiary(
            name=data['name'],
            description=data['description'],
            organization_id=data['organization_id']
        )
        db.session.add(beneficiary)
        db.session.commit()
        return jsonify({'message': 'Beneficiary added successfully'})
    
    beneficiaries = Beneficiary.query.all()
    return jsonify([{
        'id': ben.id,
        'name': ben.name,
        'description': ben.description,
        'status': ben.status
    } for ben in beneficiaries])

# Inventory routes
@app.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.json
    item = InventoryItem(
        name=data['item_name'],
        quantity=data['quantity'],
        beneficiary_id=data['beneficiary_id'],
        date_sent=datetime.strptime(data['date_sent'], '%Y-%m-%d')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Inventory item added successfully'})

if __name__ == '__main__':
    app.run(port=8000, debug=True)