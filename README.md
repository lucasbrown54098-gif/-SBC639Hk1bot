# 🏆 Sports News Telegram Bot

A self-contained Telegram bot delivering sports news without external APIs.

## ✨ Features

- **6 Sports Categories**: Cricket, Football, Basketball, Tennis, F1, Badminton
- **Smart Search**: Find news by keywords
- **Favorites System**: Save your favorite news
- **User Preferences**: Customize your experience
- **Interactive Buttons**: Easy navigation
- **No API Required**: Fully self-contained

## 🚀 Quick Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

### Manual Deployment:

1. **Fork this repository**
2. **Create a new project on Railway**
3. **Connect your GitHub repository**
4. **Add environment variable:**
   - `TELEGRAM_BOT_TOKEN` = Your bot token from @BotFather
5. **Deploy!**

## 📦 Environment Variables

| Variable | Description |
|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from @BotFather |

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome menu with sports selection |
| `/help` | Show all commands |
| `/latest` | Get latest news |
| `/popular` | Most popular news |
| `/search [keyword]` | Search news |
| `/fav [title]` | Add to favorites |
| `/favorites` | View your favorites |
| `/removefav [title]` | Remove from favorites |
| `/sport [sport]` | Get sport-specific news |
| `/settings` | User preferences |
| `/stats` | Bot statistics |
| `/about` | About this bot |

## 🛠️ Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/sports-news-bot.git
cd sports-news-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export TELEGRAM_BOT_TOKEN="your_bot_token"

# Run the bot
python bot.py
