from flask import Flask, request, jsonify
from flask_mail import Mail, Message

from app import app

from app.utils.send_email import mail

@app.route('/email/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        recipient = request.json.get('recipient')
        subject = request.json.get('subject')
        message = request.json.get('message')
        additional_text = request.json.get('additional_text')  # New field for additional text

        if not recipient or not subject or not message:
            return jsonify({'error': 'Missing parameters'}), 400

        # Combine the message and additional text
        complete_message = f'{message}\n\nAdditional Text: {additional_text}'

        # Create a Message object for the email
        msg = Message(subject, sender='consultasapp2023@gmail.com', recipients=[recipient])
        msg.body = complete_message  # Use the complete message

        try:
            # Send the email
            mail.send(msg)
            return jsonify({'message': 'Email sent successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
