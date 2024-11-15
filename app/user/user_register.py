from datetime import datetime, timedelta
from flask import jsonify, request
from app import app
from app.utils.firebase import firebase_db
import secrets
import bcrypt
import jwt  # Asegúrate de importar la biblioteca JWT

# Clave secreta para firmar el JWT (debe mantenerse segura y privada)
SECRET_KEY = "tu_clave_secreta_super_segura"

@app.route('/user/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        data['creation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Verificar si el usuario ya existe en Firebase
        existing_user = None
        users = firebase_db.get('/user', None)
        if users:
            for user_id, user_data in users.items():
                if user_data.get('email') == data.get('email'):
                    existing_user = user_id
                    break

        if existing_user:
            return jsonify({'message': 'User already exists', 'id': existing_user}), 400

        # Generar un `user_id` único para el nuevo usuario
        user_id = secrets.token_hex(16)  # Genera un token hexadecimal de 32 caracteres

        # Encripta la contraseña antes de guardarla en la base de datos
        password = data.get('password').encode('utf-8')  # Convierte la contraseña en bytes
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        data['password'] = hashed_password.decode('utf-8')  # Guarda la contraseña encriptada
        data['user_id'] = user_id  # Añade el `user_id` al diccionario de datos

        # Guarda el usuario en Firebase usando el `user_id` como clave principal
        firebase_db.put('/user', user_id, data)

        # Generar el token JWT con el `user_id`
        expiration = datetime.utcnow() + timedelta(days=90)  # Token válido por 90 días (3 meses)
        token = jwt.encode(
            {
                'user_id': user_id,
                'exp': expiration
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        # Retornar el token en la respuesta
        return jsonify({
            'message': 'User record created successfully',
            'id': user_id,
            'token': token
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500