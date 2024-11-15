from flask import jsonify,request
from app import app
from app.utils.firebase import firebase_db
import bcrypt


@app.route('/user/change_password', methods=['POST'])
def change_password():
    try:
        data = request.get_json()

        users = firebase_db.get('/user', None)
        if users:
            for user_id, user_data in users.items():
                if user_data.get('email') == data.get('email'):
                    # Genera una nueva contraseña y encripta la nueva contraseña
                    new_password = data.get('new_password').encode('utf-8')

                    hashed_password = bcrypt.hashpw(new_password, bcrypt.gensalt())

                    user_data['password'] = hashed_password.decode('utf-8')


                    # Guarda los cambios en la base de datos
                    firebase_db.put('/user', user_id, user_data)

                    return jsonify({'message': 'Password changed successfully'}), 200

        # Si no se encuentra un usuario con el correo electrónico proporcionado, devuelve un mensaje de error.
        return jsonify({'message': 'User not found'}, 404)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


