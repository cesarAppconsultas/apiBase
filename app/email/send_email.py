from flask import Flask, request, jsonify
from flask_mail import Mail, Message

from app import app

from app.utils.send_email import mail
from datetime import datetime


@app.route('/email/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        recipient = request.json.get('recipient')
        sender_name = request.json.get('sender_name')  # Nombre del usuario que envía
        sender_phone = request.json.get('sender_phone')  # Teléfono del usuario que envía
        subject = request.json.get('subject')
        message = request.json.get('message')
        additional_text = request.json.get('additional_text')

        # Validar que los datos obligatorios estén presentes
        if not recipient or not sender_name or not sender_phone:
            return jsonify({'error': 'Missing required parameters: recipient, sender_name, or sender_phone'}), 400

        # Personalizar el subject con el nombre y el teléfono
        subject = f"Tienes una solicitud de consulta de {sender_name} ({sender_phone})"

        # Personalizar el message con fecha y hora
        current_datetime = datetime.now().strftime("%d-%m-%Y %H:%M")
        message = f"Tienes una solicitud de reserva el día de hoy, {current_datetime}.\n\n{message}"

        # Combinar el mensaje completo con texto adicional
        complete_message = f"{message}\n\n{additional_text}"

        # Crear un objeto Message para el correo con el "No responder"
        sender_address = "consultasapp2023@gmail.com"
        sender_full = f"No responder <{sender_address}>"
        msg = Message(subject, sender=sender_full, recipients=[recipient])
        msg.body = complete_message

        try:
            # Enviar el correo
            mail.send(msg)
            return jsonify({'message': 'Email sent successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500