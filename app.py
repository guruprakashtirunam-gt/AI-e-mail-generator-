from flask import Flask, request, jsonify, send_from_directory
from prompts import build_email_prompt
from email_generator import generate_email_content
from utils import parse_generated_email
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    
    email_type = data.get('emailType', '')
    recipient = data.get('recipient', '')
    tone = data.get('tone', '')
    length = data.get('length', '')
    additional_details = data.get('additionalDetails', '')
    
    if not additional_details.strip():
        return jsonify({"error": "Please provide some additional details."}), 400
        
    prompt = build_email_prompt(email_type, recipient, tone, length, additional_details)
    raw_response = generate_email_content(prompt)
    
    if raw_response.startswith("Error:") or raw_response.startswith("An error occurred"):
        return jsonify({"error": raw_response}), 500
        
    subject, body = parse_generated_email(raw_response)
    
    return jsonify({
        "subject": subject,
        "body": body
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
