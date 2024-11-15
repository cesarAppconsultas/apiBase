from flask import jsonify, request
from app import app
from app.utils.firebase import firebase_db
from app.utils.token_required import token_required


@app.route('/patient/all', methods=['GET'])
@token_required
def get_patients():
    try:
        result = firebase_db.get('/patients', None)
        if result:
            patients = []
            for patient_id, patient_data in result.items():
                patient_data['id'] = patient_id
                patients.append(patient_data)
            return jsonify(patients)
        else:
            return jsonify([])  # Returns an empty list if there are no patients
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/patient/<string:idUser>', methods=['GET'])
@token_required
def by_id_patient(idUser):
    try:
        # Verificar que se ha recibido el id del usuario
        if not idUser:
            return jsonify({'error': 'The "patient" parameter is required in the URL'}), 400

        # Obtener todos los pacientes desde Firebase
        patients = firebase_db.get('/patients', None)

        # Validar que hay pacientes en la base de datos
        if not patients:
            return jsonify({'message': 'No patients found in the database'}), 404

        # Buscar el paciente por la clave específica
        patient = patients.get(idUser)

        # Verificar si el paciente fue encontrado
        if patient:
            patient_with_id = {'id': idUser, **patient}
            return jsonify(patient_with_id), 200
        else:
            return jsonify({'message': 'No patients found with the specified id'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
