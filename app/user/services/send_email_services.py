from flask import jsonify
from app.utils.config import MAIL_USERNAME
from flask_mail import Message

from app.utils.send_email import mail


def send_email(email):
    recipient = email
    subject = 'Recuperar tucontraseña'
    message = 'recuperacion de mi contraseña'
    additional_text = '123456'

    if not recipient or not subject or not message:
        return jsonify({'error': 'Missing parameters'}), 400

    # Combine the message and additional text
    complete_message = f'{message}\n\ntu contraseña provicional es: {additional_text}'

    # Create a Message object for the email
    msg = Message(subject, sender=MAIL_USERNAME, recipients=[recipient])
    msg.body = complete_message  # Use the complete message

    try:
        # Send the email
        mail.send(msg)
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
