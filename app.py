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

        # Try to send message to Rasa first
        try:
            rasa_payload = {
                "sender": sender,
                "message": message
            }
            response = requests.post(RASA_API_URL, json=rasa_payload, timeout=2)

            if response.status_code == 200:
                rasa_response = response.json()
                return jsonify(rasa_response)
        except:
            pass  # Fallback to simple responses if Rasa is not available

        # Simple fallback responses when Rasa is not available
        message_lower = message.lower()

        # Greeting patterns
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'merhaba', 'selam']):
            response_text = "Hello! Welcome to CW Enerji Solar Panel Chatbot. How can I help you today? I can answer questions about solar panels, pricing, installation, and more."

        # Solar panel information
        elif any(keyword in message_lower for keyword in ['solar panel', 'solar', 'energy', 'panel', 'güneş', 'enerji']):
            response_text = "Solar panels are an excellent investment for clean energy! CW Enerji offers high-quality solar panels with 25-year warranties. Our systems can help you save on electricity bills while reducing your carbon footprint. Would you like to know more about pricing or installation?"

        # Pricing questions
        elif any(keyword in message_lower for keyword in ['price', 'cost', 'fiyat', 'ücret']):
            response_text = "Solar panel pricing varies based on your energy needs and location. Typically, a residential system costs between $10,000-$25,000, but many financing options are available. Would you like a personalized quote? I'll need to know your location and average monthly electricity consumption."

        # Installation questions
        elif any(keyword in message_lower for keyword in ['install', 'installation', 'montaj', 'kurulum']):
            response_text = "CW Enerji provides professional installation services. Our certified technicians handle everything from site assessment to final connection. Installation usually takes 1-3 days depending on system size. We also handle all permits and paperwork."

        # Benefits questions
        elif any(keyword in message_lower for keyword in ['benefit', 'advantage', 'fayda', 'avantaj']):
            response_text = "Solar panels offer numerous benefits: reduced electricity bills, energy independence, environmental protection, increased property value, and government incentives. Most systems pay for themselves within 5-7 years!"

        # Warranty questions
        elif any(keyword in message_lower for keyword in ['warranty', 'guarantee', 'garanti']):
            response_text = "CW Enerji offers comprehensive warranties: 25-year performance guarantee, 10-year product warranty, and 5-year workmanship warranty. Our panels are built to last and maintain high efficiency throughout their lifetime."

        # Purchase intent
        elif any(keyword in message_lower for keyword in ['buy', 'purchase', 'order', 'al', 'satın']):
            response_text = "Great! I'd be happy to help you purchase a solar system. To provide you with an accurate quote, I'll need: 1) Your location/address, 2) Average monthly electricity bill, 3) Roof type and available space. Could you share this information?"

        # Goodbye patterns
        elif any(greeting in message_lower for greeting in ['bye', 'goodbye', 'güle güle', 'hoşça kal']):
            response_text = "Thank you for contacting CW Enerji! Feel free to reach out anytime with questions about solar energy. Have a wonderful day!"

        # Thanks patterns
        elif any(greeting in message_lower for greeting in ['thank', 'thanks', 'teşekkür']):
            response_text = "You're welcome! I'm here to help with any solar energy questions you may have. Is there anything else you'd like to know about our solar panels or services?"

        # Default response
        else:
            response_text = "I'm here to help you with solar panel information! I can answer questions about pricing, installation, benefits, warranties, and purchasing options. What would you like to know about CW Enerji solar solutions?"

        return jsonify([{'text': response_text}])

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify([{'text': 'I apologize, but I\'m having trouble processing your request. Please try again.'}]), 500

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
            'status': '/api/status',
            'tts': '/api/tts'
        }
    })

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    """Simple TTS endpoint - returns empty response to disable voice for now"""
    try:
        data = request.json
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Return a simple response to prevent JavaScript errors
        return jsonify({
            'audio': '',
            'message': 'Voice disabled for now'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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