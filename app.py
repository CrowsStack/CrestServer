from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS
from email.message import EmailMessage
import ssl
import smtplib
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["https://altered-kelly-calendar-connections.trycloudflare.com/contact"]}})

# Configure logging
logging.basicConfig(level=logging.ERROR, filename='error.log')

@app.route('/api/contact', methods=['POST'])
def receive_contact_form():
    # Get the JSON data sent in the POST request
    data = request.json

    # Validate required fields
    required_fields = ['name', 'email', 'message', 'phone', 'loanType']
    for field in required_fields:
        if field not in data:
            return jsonify({"status": "error", "message": f"'{field}' is required."}), 400

    load_dotenv()  # Load environment variables

    # Email credentials from environment variables
    email_sender = os.getenv("EMAIL_SENDER")  # Gmail address
    email_password = os.getenv("EMAIL_PASSWORD")  # Gmail app password
    email_receiver = os.getenv("EMAIL_RECEIVER")  # Recipient's email

    # Ensure credentials are set
    if not (email_sender and email_password and email_receiver):
        return jsonify({"status": "error", "message": "Email credentials are not properly set."}), 500

    # Dynamic email details
    dynamic_sender_email = 'Developer <Developer@crestbeam.com.ng>'
    subject = f"Contact Form Submission: {data['name']} - {data['loanType']}"
    body = (
        f"Name: {data['name']}\n"
        f"Email: {data['email']}\n"
        f"Phone: {data['phone']}\n"
        f"Loan Type: {data['loanType']}\n"
        f"Message: {data['message']}\n"
    )

    # Create email message
    em = EmailMessage()
    em['From'] = dynamic_sender_email
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Send email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        response = {
            "status": "success",
            "message": "Form data received and email sent successfully.",
            "data": data,
        }
        return jsonify(response), 200

    except smtplib.SMTPException as e:
        logging.error("SMTP error occurred", exc_info=True)
        return jsonify({"status": "error", "message": "Failed to send email."}), 500

    except Exception as e:
        logging.error("Unexpected error", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # Run the Flask app
    host = os.getenv("HOST", "10.2.189.1")  # Default host
    port = int(os.getenv("PORT", 5000))   # Default port

    # Print the IP address and port
    print(f"Flask app is running on: http://{host}:{port}")

    app.run(host=host, port=port, debug=True)