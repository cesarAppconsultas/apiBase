from flask import jsonify
from app import app
from app.user.services import send_email_services
from app.utils.firebase import firebase_db
import bcrypt


@app.route('/user/<string:email>', methods=['GET'])
def recover_password(email):
    try:
        if not email:
            return jsonify({'error': 'The "name" parameter is required in the URL'})

        users = firebase_db.get('/user', None)
        if users:
            for user_id, user_data in users.items():
                if user_data.get('email') == email:

                    # Encripta la contraseña antes de guardarla en la base de datos
                    password =('123456').encode('utf-8')  # Convierte la contraseña en bytes
                    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

                    # Actualiza la contraseña almacenada en la base de datos
                    user_data['password'] = hashed_password.decode('utf-8')

                    # Guarda los cambios en la base de datos
                    firebase_db.put('/user', user_id, user_data)

                    return send_email_services.send_email(email)

        return jsonify({'message': 'User not found'}, 404)

    except Exception as e:
        return jsonify({'error': str(e)}), 500





