from flask import Flask, render_template, request, jsonify
import requests
import os
import subprocess
import threading
import time

app = Flask(__name__)

# Rasa configuration
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

class RasaManager:
    def __init__(self):
        self.rasa_process = None
        self.rasa_running = False

    def start_rasa(self):
        """Start Rasa server in the background"""
        try:
            # Start Rasa action server
            action_server = subprocess.Popen(
                ["rasa", "run", "actions"],
                cwd="/data/data/com.termux/files/home/solar-chatbot",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Wait a moment for action server to start
            time.sleep(3)

            # Start Rasa server
            rasa_server = subprocess.Popen(
                ["rasa", "run", "--enable-api", "--cors", "*"],
                cwd="/data/data/com.termux/files/home/solar-chatbot",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Wait for Rasa server to be ready
            time.sleep(5)
            self.rasa_running = True
            print("Rasa server started successfully!")
            return True

        except Exception as e:
            print(f"Error starting Rasa: {e}")
            return False

    def stop_rasa(self):
        """Stop Rasa server"""
        if self.rasa_process:
            self.rasa_process.terminate()
            self.rasa_process = None
        self.rasa_running = False

rasa_manager = RasaManager()

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages via REST API"""
    try:
        data = request.json
        message = data.get('message', '')
        sender = data.get('sender', 'user')

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Send message to Rasa
        rasa_payload = {
            "sender": sender,
            "message": message
        }

        response = requests.post(RASA_API_URL, json=rasa_payload)

        if response.status_code == 200:
            rasa_response = response.json()
            return jsonify(rasa_response)
        else:
            return jsonify({
                'text': 'I apologize, but I\'m having trouble processing your request right now. Please try again.',
                'error': 'Rasa server error'
            }), 500

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'text': 'I\'m experiencing some technical difficulties. Please try again later.',
            'error': str(e)
        }), 500

@app.route('/api/status')
def status():
    """Check the status of the chatbot system"""
    rasa_status = "running" if rasa_manager.rasa_running else "stopped"

    try:
        # Test Rasa connection
        response = requests.get("http://localhost:5005/", timeout=2)
        rasa_connected = response.status_code == 200
    except:
        rasa_connected = False

    return jsonify({
        'flask': 'running',
        'rasa': rasa_status,
        'rasa_connected': rasa_connected,
        'endpoints': {
            'chat': '/api/chat',
            'status': '/api/status'
        }
    })

@app.route('/api/train', methods=['POST'])
def train_model():
    """Train the Rasa model"""
    try:
        # Run training in a subprocess
        result = subprocess.run(
            ["rasa", "train"],
            cwd="/data/data/com.termux/files/home/solar-chatbot",
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )

        if result.returncode == 0:
            return jsonify({
                'status': 'success',
                'message': 'Model trained successfully',
                'output': result.stdout
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Training failed',
                'error': result.stderr
            }), 500

    except subprocess.TimeoutExpired:
        return jsonify({
            'status': 'error',
            'message': 'Training timed out after 5 minutes'
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Training error: {str(e)}'
        }), 500

def initialize_rasa():
    """Initialize and start Rasa server"""
    print("Initializing Rasa server...")
    success = rasa_manager.start_rasa()

    if not success:
        print("Failed to start Rasa server. Please check if Rasa is installed.")
        print("You can start Rasa manually with:")
        print("  cd /data/data/com.termux/files/home/solar-chatbot")
        print("  rasa run actions")
        print("  rasa run --enable-api --cors \"*\"")

if __name__ == '__main__':
    # Start Rasa in a background thread
    rasa_thread = threading.Thread(target=initialize_rasa, daemon=True)
    rasa_thread.start()

    # Give Rasa time to start
    time.sleep(8)

    # Start Flask server
    print("Starting Solar Panel Chatbot...")
    print("Access the chatbot at: http://localhost:5000")
    print("API Status endpoint: http://localhost:5000/api/status")

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)