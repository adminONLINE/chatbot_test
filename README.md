# 🌞 Solar Panel Chatbot

A complete chatbot solution for solar panel sales built with Rasa, Python, and HTML. This chatbot helps customers with solar panel information, pricing, installation details, and guides them through the purchase process.

## Features

- **Natural Language Understanding**: Understands user intents related to solar panels
- **Sales Flow**: Guides customers through the solar panel purchasing process
- **Information Provider**: Answers questions about benefits, pricing, types, installation, and maintenance
- **Personalized Recommendations**: Provides system size and pricing based on location and energy usage
- **Modern UI**: Clean, responsive web interface
- **Real-time Chat**: Live conversation with typing indicators

## Project Structure

```
solar-chatbot/
├── actions/                 # Custom actions for Rasa
│   ├── __init__.py
│   └── actions.py          # Custom action implementations
├── data/                   # Rasa training data
│   ├── nlu.yml            # Intent training examples
│   ├── stories.yml        # Conversation stories
│   └── rules.yml          # Conversation rules
├── templates/              # HTML templates
│   └── index.html         # Main chat interface
├── app.py                 # Flask backend server
├── config.yml             # Rasa configuration
├── domain.yml             # Rasa domain (intents, entities, responses)
├── credentials.yml        # Channel credentials
├── endpoints.yml          # Action server endpoints
├── requirements.txt       # Python dependencies
├── run_chatbot.py         # Setup and run script
└── README.md             # This file
```

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Quick Start

1. **Clone or download the project files**
2. **Run the setup script**:
   ```bash
   python run_chatbot.py
   ```
3. **Choose option 4** for full setup (install dependencies, train model, start chatbot)
4. **Open your browser** and go to: `http://localhost:5000`

### Manual Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the Rasa model**:
   ```bash
   rasa train
   ```

3. **Start Rasa action server** (in one terminal):
   ```bash
   rasa run actions
   ```

4. **Start Rasa core server** (in another terminal):
   ```bash
   rasa run --enable-api --cors "*"
   ```

5. **Start the Flask web application** (in a third terminal):
   ```bash
   python app.py
   ```

6. **Open your browser** and go to: `http://localhost:5000`

## Chatbot Capabilities

### Intents Supported

- **Greeting/Goodbye**: Basic conversation etiquette
- **Purchase Intent**: User wants to buy solar panels
- **Information Request**: User wants to learn about solar panels
- **Pricing Questions**: Cost and investment information
- **Benefits Inquiry**: Advantages of solar energy
- **Types of Panels**: Different panel options
- **Installation Process**: How installation works
- **Maintenance**: Panel upkeep requirements
- **Financing Options**: Payment plans and loans
- **Warranty Information**: Product guarantees
- **Location & Energy Usage**: For personalized recommendations

### Sample Conversations

**Sales Flow**:
```
User: Hi
Bot: Hello! Welcome to SolarTech Solutions. Are you looking to purchase solar panels or would you like information?

User: I want to buy solar panels
Bot: Great! To provide the best recommendations, could you tell me your location and approximate monthly energy usage?

User: I live in California and use 1000 kWh per month
Bot: Based on your location and usage, I recommend a 5kW system costing approximately $15,000. This would eliminate about 90% of your electricity bill!
```

**Information Flow**:
```
User: Tell me about solar panels
Bot: I'd be happy to provide information! What specifically would you like to know?

User: What are the benefits?
Bot: Solar panels offer numerous benefits: reduce electricity bills by 70-90%, increase property value, reduce carbon footprint, earn tax credits, and achieve energy independence!
```

## API Endpoints

- **Main Chat Interface**: `GET /`
- **Chat API**: `POST /api/chat`
- **System Status**: `GET /api/status`
- **Train Model**: `POST /api/train`

### Chat API Usage

```javascript
const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        sender: 'user',
        message: 'How much do solar panels cost?'
    })
});

const data = await response.json();
console.log(data); // [{ text: "Solar panels typically cost..." }]
```

## Customization

### Adding New Intents

1. Add intent examples to `data/nlu.yml`
2. Add responses to `domain.yml`
3. Create stories/rules in `data/stories.yml` and `data/rules.yml`
4. Retrain the model with `rasa train`

### Modifying Responses

Edit the `utter_*` responses in `domain.yml` to customize the chatbot's personality and information.

### Adding Custom Actions

1. Create new action methods in `actions/actions.py`
2. Add action names to `domain.yml`
3. Use actions in stories or rules

## Development

### Testing the Chatbot

1. Start all services using the setup script
2. Open `http://localhost:5000` in your browser
3. Test various conversation flows
4. Check system status at `http://localhost:5000/api/status`

### Debugging

- Check the terminal output for error messages
- Use Rasa's interactive mode: `rasa interactive`
- Test individual components:
  - NLU: `rasa shell nlu`
  - Actions: `rasa test actions`

## Production Deployment

For production deployment:

1. **Use a production WSGI server** (Gunicorn, uWSGI)
2. **Configure HTTPS** with SSL certificates
3. **Set up proper CORS policies**
4. **Implement logging and monitoring**
5. **Use environment variables** for configuration
6. **Deploy Rasa servers separately** for better scaling

Example Gunicorn command:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py`
2. **Rasa server not starting**: Check if Rasa is properly installed
3. **CORS errors**: Ensure Rasa server is started with `--cors "*"`
4. **Model not responding**: Retrain the model with `rasa train`

### Getting Help

- Check the console output for error messages
- Verify all dependencies are installed
- Ensure all required files exist
- Test Rasa components individually

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the console output
3. Verify your setup matches the requirements
4. Test with the provided examples

---

**🌞 Start your solar journey today with our intelligent chatbot assistant!**