from datetime import datetime
from app.utils.firebase import firebase_db

from flask import request, jsonify
from app import app
from app.utils.token_required import token_required


@app.route('/patient/create', methods=['POST'])
@token_required
def create_patient():
    try:
        data = request.get_json()
        data['creation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Associate patient with the `user_id` from the authenticated token
        data['user_id'] = request.user_id

        # Use user-specific path in Firebase to segregate patients by user
        result = firebase_db.post(f'/patients/{data["user_id"]}', data)

        return jsonify({'message': 'Patient record created successfully', 'id': result['name']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500