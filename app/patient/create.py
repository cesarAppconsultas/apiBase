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

        # Asociar el paciente con el `user_id` del usuario autenticado extraído del token
        data['user_id'] = request.user_id

        # Crear el registro en Firebase
        result = firebase_db.post('/patients', data)
        return jsonify({'message': 'Patient record created successfully', 'id': result['name']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500