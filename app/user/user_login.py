from flask import jsonify, request
from app import app
from app.utils.firebase import firebase_db
import bcrypt
import jwt  # Importa la biblioteca JWT
from datetime import datetime, timedelta

# Clave secreta para firmar el JWT (debe mantenerse segura y privada)
SECRET_KEY = "tu_clave_secreta_super_segura"


@app.route('/user/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()

        # Obtén todos los usuarios desde Firebase
        users = firebase_db.get('/user', None)
        if users:
            for user_id, user_data in users.items():
                if user_data.get('email') == data.get('email'):
                    # Extraer la contraseña encriptada almacenada en la base de datos
                    stored_password = user_data.get('password')
                    # Verificar si la contraseña ingresada por el usuario coincide con la contraseña encriptada
                    if bcrypt.checkpw(data.get('password').encode('utf-8'), stored_password.encode('utf-8')):
                        # Las contraseñas coinciden, crea el token JWT con los datos del usuario
                        selected_fields = {
                            'user_id': user_id,
                            'last_name': user_data.get('last_name'),
                            'name': user_data.get('name'),
                            'phone': user_data.get('phone'),
                            'email': user_data.get('email'),
                            'creation_date': user_data.get('creation_date')
                        }

                        # Establece el tiempo de expiración del token a 3 meses (90 días)
                        expiration = datetime.utcnow() + timedelta(days=90)

                        # Crea el token JWT
                        token = jwt.encode(
                            {
                                'user_data': selected_fields,
                                'exp': expiration
                            },
                            SECRET_KEY,
                            algorithm="HS256"
                        )

                        # Devuelve el token JWT en lugar de los datos directamente
                        return jsonify({'message': 'User logged in successfully', 'token': token}), 200

        # Si no se encuentra un usuario coincidente o las contraseñas no coinciden, devuelve un mensaje de error.
        return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500