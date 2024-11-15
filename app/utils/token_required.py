from functools import wraps
from flask import request, jsonify
import jwt

# Clave secreta utilizada para firmar el JWT
SECRET_KEY = "tu_clave_secreta_super_segura"

from functools import wraps
from flask import request, jsonify
import jwt

# Clave secreta utilizada para firmar el JWT
SECRET_KEY = "tu_clave_secreta_super_segura"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Obtener el token JWT de la cabecera "Authorization"
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1]
            print("Token recibido:", token)  # Imprime el token recibido

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decodificar el token JWT
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print("Payload decodificado:", data)  # Imprime el contenido del token decodificado

            # Extraer el `user_id` de `user_data` en el payload del token
            user_data = data.get('user_data', {})
            request.user_id = user_data.get('user_id')

            if request.user_id is None:
                return jsonify({'message': 'Invalid token: user_id is missing'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated

