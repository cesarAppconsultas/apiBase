from flask import jsonify, request
from app import app
from app.utils.firebase import firebase_db
from app.utils.token_required import token_required


@app.route('/patient/all', methods=['GET'])
@token_required
def get_patients():
    try:
        # Fetch patients only for the current authenticated user
        result = firebase_db.get(f'/patients/{request.user_id}', None)

        # Check if result exists and format as a list of patients
        if result:
            patients = []
            for patient_id, patient_data in result.items():
                patient_data['id'] = patient_id
                patients.append(patient_data)
            return jsonify(patients), 200
        else:
            return jsonify([]), 200  # Returns an empty list if there are no patients
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/patient/<string:patient_id>', methods=['GET'])
@token_required
def by_id_patient(patient_id):
    try:
        # Get the authenticated user's ID from the token
        authenticated_user_id = request.user_id

        # Fetch all patients associated with this user
        patients = firebase_db.get(f'/patients/{authenticated_user_id}', None)

        # Verify if patients exist for the authenticated user
        if not patients:
            return jsonify({'message': 'No patients found for the authenticated user'}), 404

        # Search for the patient with the specified patient_id
        patient_data = patients.get(patient_id)

        # Check if the patient with the specified ID was found
        if patient_data:
            # Include the patient_id in the response data
            patient_with_id = {'id': patient_id, **patient_data}
            return jsonify(patient_with_id), 200
        else:
            return jsonify({'message': 'No patient found with the specified ID'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500