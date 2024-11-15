from datetime import datetime
from app.utils.firebase import firebase_db

from flask import request, jsonify
from app import app
from app.utils.token_required import token_required


@app.route('/patient/update/<string:id_patients>', methods=['PATCH'])
@token_required
def update_patient(id_patients):
    try:
        # Obtener los datos enviados en el cuerpo de la solicitud
        data = request.get_json()

        # Verificar si el paciente existe antes de actualizar
        patient = firebase_db.get(f'/patients/{id_patients}', None)
        if not patient:
            return jsonify({'message': 'No patient found with the provided ID'}), 404

        # Actualizar solo los campos especificados en `data`
        data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for key, value in data.items():
            firebase_db.put(f'/patients/{id_patients}', key, value)

        return jsonify({'message': 'Patient record updated successfully', 'id': id_patients}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500