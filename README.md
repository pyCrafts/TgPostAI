<p align="center">
    <a href="https://github.com/pyCrafts/TgPostAI/blob/main/README.md"><u><b>ENGLISH</b></u></a> •
    <a href="https://github.com/pyCrafts/TgPostAI/blob/main/README.ru_RU.md"><u><b>РУССКИЙ</b></u></a>
</p>

# 🤖 AI Telegram Post Bot

A powerful Telegram bot that uses Google Gemini AI to help you create, improve, and publish high-quality posts for your Telegram channels and groups.

## ✨ Features

- **🎯 Smart Post Improvement**: Enhance structure, readability, and engagement
- **🔧 Error Correction**: Fix grammar, spelling, and punctuation mistakes
- **✍️ Content Creation**: Generate new posts from topic descriptions
- **📊 Post Analysis**: Get detailed recommendations for improvement
- **✂️ Text Optimization**: Shorten or expand content as needed
- **📢 Direct Publishing**: Publish posts directly to your channels/groups
- **🌐 Multi-language**: Support for Russian and English interfaces
- **📈 Usage Statistics**: Track your AI requests and limits
- **⚡ Rate Limiting**: Built-in daily request limits for responsible usage

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Google Gemini API Key (from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/pyCrafts/TgPostAI.git
   cd TgPostAI
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your credentials:

   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

### Docker Deployment

1. **Using Docker Compose**

   ```bash
   docker-compose up -d
   ```

2. **Using Docker directly**
   ```bash
   docker build -t telegram-post-ai .
   docker run -d --name telegram-post-ai --env-file .env telegram-post-ai
   ```

## 📖 How to Use

1. **Start the bot** - Send `/start` to begin
2. **Choose language** - Select your preferred interface language
3. **Select action** - Pick from the main menu:

   - ✍️ **Create Post** - Generate new content from a topic
   - ✨ **Improve Post** - Enhance existing text
   - 🔧 **Fix Errors** - Correct grammar and spelling
   - 🎯 **Make Engaging** - Add calls-to-action and emotion
   - ✂️ **Shorten** - Make text more concise
   - 📝 **Expand** - Add more details and examples
   - 📊 **Analyze** - Get improvement recommendations

4. **Send your text** or topic description
5. **Get AI-processed result**
6. **Publish directly** to your channels (optional)

## 🔧 Configuration

### Environment Variables

| Variable             | Description             | Required |
| -------------------- | ----------------------- | -------- |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | ✅       |
| `GEMINI_API_KEY`     | Google Gemini API key   | ✅       |
| `DEBUG`              | Enable debug logging    | ❌       |

### Bot Settings

- **Daily Request Limit**: 25 requests per user per day
- **Max Message Length**: 4,096 characters
- **Gemini Model**: `gemini-2.0-flash-exp`

## 📢 Publishing to Channels

To publish posts directly to your channels:

1. Add the bot as an administrator to your channel
2. Grant "Post Messages" permission
3. Use the 📢 **Publish** button after processing
4. Send channel username (@channel) or ID (-1001234567890)
5. Confirm and publish!

## 🏗️ Project Structure

```
TgPostAI/
├── bot.py                 # Main bot application
├── config.py             # Configuration settings
├── keyboards.py          # Telegram keyboards
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker deployment
├── Dockerfile           # Docker image
├── handlers/            # Message handlers
│   ├── start.py         # Start command
│   ├── menu.py          # Menu navigation
│   ├── create.py        # Post creation
│   ├── edit.py          # Post editing
│   ├── publish.py       # Publishing
│   ├── stats.py         # Statistics
│   ├── help.py          # Help system
│   ├── language.py      # Language switching
│   └── common.py        # Common handlers
├── models/              # Data models
│   └── states.py        # FSM states
└── services/            # Business logic
    ├── ai_service.py    # Gemini AI integration
    ├── channel_service.py # Channel management
    ├── language_service.py # Localization
    └── rate_limiter.py  # Request limiting
```

## 🔒 Security Features

- **Rate Limiting**: Prevents API abuse with daily request limits
- **Permission Checks**: Validates bot permissions before publishing
- **Data Privacy**: No persistent storage of user messages

## 🌐 Supported Languages

- 🇷🇺 **Russian** - Full interface translation
- 🇺🇸 **English** - Complete localization
- Easy to extend with additional languages

## 📊 Monitoring

The bot includes built-in statistics tracking:

- Daily and total request counts per user
- Global usage statistics
- Rate limit monitoring
- Error tracking and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 **Issues**: [GitHub Issues](https://github.com/pyCrafts/TgPostAI/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/pyCrafts/TgPostAI/discussions)
- 📖 **Documentation**: Check the code comments and this README

---

<p align="center">
    Made with ❤️ for the Telegram community
</p>
