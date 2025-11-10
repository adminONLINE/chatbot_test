#!/usr/bin/env python3
"""
Simple Flask app for solar panel chatbot demo
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import tempfile
import uuid
from gtts import gTTS
import base64
from professional_chatbot import ProfessionalChatbot as SolarChatbot
from pyngrok import ngrok
import threading

app = Flask(__name__)
chatbot = SolarChatbot()

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/voice')
def voice():
    """Serve the voice interface"""
    return render_template('voice.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages via REST API"""
    try:
        data = request.json
        message = data.get('message', '')
        sender = data.get('sender', 'user')

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Get response from our simple chatbot
        response = chatbot.get_response_json(message)

        return jsonify([response])

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify([{
            'text': 'I\'m experiencing some technical difficulties. Please try again later.',
            'error': str(e)
        }]), 500

@app.route('/api/status')
def status():
    """Check the status of the chatbot system"""
    return jsonify({
        'flask': 'running',
        'chatbot': 'simple rule-based',
        'status': 'ready',
        'endpoints': {
            'chat': '/api/chat',
            'status': '/api/status',
            'tts': '/api/tts'
        }
    })

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    """Convert Turkish text to speech using Google TTS"""
    try:
        data = request.json
        text = data.get('text', '').strip()

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Generate speech using Google TTS with Turkish language
        tts = gTTS(text=text, lang='tr', slow=False)

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
            tts.save(temp_path)

        # Read the file and encode to base64
        with open(temp_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        # Clean up temporary file
        os.unlink(temp_path)

        return jsonify({
            'audio': audio_base64,
            'format': 'mp3',
            'text': text,
            'lang': 'tr'
        })

    except Exception as e:
        print(f"Error in TTS endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/templates/<path:filename>')
def serve_template(filename):
    """Serve template files"""
    return send_from_directory('templates', filename)

if __name__ == '__main__':
    print("🌞 Starting Solar Panel Chatbot (Simple Version)")
    print("=" * 50)
    print("📱 Chatbot Interface: http://localhost:5001")
    print("🔍 API Status: http://localhost:5001/api/status")
    print("💬 Chat API: http://localhost:5001/api/chat")

    # Start ngrok tunnel for HTTPS support
    try:
        public_tunnel = ngrok.connect(5001)
        public_url = public_tunnel.public_url
        print("🔒 HTTPS Tunnel: " + public_url)
        print("🎤 Mikrofon izni için HTTPS linkini kullanın!")
        print("=" * 50)
    except Exception as e:
        print(f"⚠️  Ngrok başlatılamadı: {e}")
        print("🔒 HTTPS olmadan mikrofon çalışmayabilir!")
        print("=" * 50)

    print("Ready to help customers go solar! ☀️")
    print()

    # Run Flask in a separate thread so ngrok stays alive
    def run_flask():
        app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    try:
        # Keep the main thread alive
        flask_thread.join()
    except KeyboardInterrupt:
        print("\n👋 Chatbot kapatılıyor...")