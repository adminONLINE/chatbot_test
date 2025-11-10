# 🚀 Quick Start Guide

## Your Solar Panel Chatbot is Ready!

### What You've Built
A complete solar panel sales chatbot with:
- **Natural Language Understanding** for customer inquiries
- **Sales Conversation Flow** to guide customers to purchase
- **Information Provider** for educational content
- **Modern Web Interface** with real-time chat
- **Personalized Recommendations** based on location and energy usage

### Quick Setup (5 minutes)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the setup script**:
   ```bash
   python run_chatbot.py
   ```

3. **Choose option 4** (Full setup)

4. **Open your browser**: http://localhost:5000

### Sample Conversations to Try

**Sales Flow**:
- "Hi" → "I want to buy solar panels" → "I live in California" → "I use 1000 kWh per month"

**Information Flow**:
- "Tell me about solar panels" → "What are the benefits?" → "How much does it cost?"

**Quick Questions**:
- "What types of solar panels do you have?"
- "How long does installation take?"
- "Do you offer financing?"
- "What's the warranty?"

### Features Available

✅ **Greeting & Welcome**: Professional customer service start
✅ **Sales Guidance**: Collects location & energy usage for quotes
✅ **Product Information**: Benefits, types, pricing, installation
✅ **Financial Options**: Plans, loans, incentives explained
✅ **Technical Support**: Maintenance, warranty details
✅ **Smart Recommendations**: System sizing and pricing calculator
✅ **Modern UI**: Clean, mobile-friendly interface
✅ **Real-time Chat**: Typing indicators and smooth flow

### File Structure
```
solar-chatbot/
├── 📁 actions/          # Custom Rasa actions
├── 📁 data/            # Training data
├── 📁 templates/       # HTML frontend
├── 🤖 app.py           # Flask backend
├── 🧠 config.yml       # Rasa configuration
├── 🌐 domain.yml       # Chatbot brain
├── 🚀 run_chatbot.py   # Easy setup script
└── 📖 README.md        # Full documentation
```

### Customization Tips

**Add New Responses**: Edit `domain.yml` under `responses:`
**Add New Intents**: Add to `data/nlu.yml` and `domain.yml`
**Modify Actions**: Edit `actions/actions.py`
**Change UI Design**: Edit `templates/index.html`

### Troubleshooting

**Port in use?** Change port in `app.py` (line 180)
**Rasa not working?** Check if all dependencies installed
**Model errors?** Run `rasa train` to rebuild
**Connection issues?** Check firewall/antivirus settings

### Need Help?

1. Check the console output for error messages
2. Run the test script: `python simple_test.py`
3. Review the full README.md documentation
4. Verify all files are present in the directory

---

**🌞 Your solar panel chatbot is ready to help customers go green!**