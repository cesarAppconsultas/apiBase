from flask import jsonify
from app import app
from app.utils.firebase import firebase_db
from app.utils.token_required import token_required


@app.route('/patient/delete/<string:id>', methods=['DELETE'])
@token_required
def delete_patient(id):
    try:
        # Verificar si el paciente existe en la base de datos
        patient = firebase_db.get(f'/patients/{id}', None)

        # Si el paciente no existe, devolvemos un 404
        if not patient:
            return jsonify({'message': 'No patient found with the provided ID'}), 404

        # Si el paciente existe, procedemos a eliminarlo
        firebase_db.delete('/patients', id)
        return jsonify({'message': 'Patient record deleted successfully'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500