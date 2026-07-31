import os
import random
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== SELF-CONTAINED NEWS DATABASE ====================
class SportsNewsDB:
    def __init__(self):
        self.news = {
            'cricket': [
                {'title': 'India Wins Test Series Against Australia', 'description': 'Team India clinched a historic test series victory against Australia at home by 2-1.', 'category': 'Cricket', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'Sports Desk'},
                {'title': 'Virat Kohli Returns to Form with Century', 'description': 'Star batsman Virat Kohli scored his 76th international century.', 'category': 'Cricket', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'Cricket News'},
                {'title': 'IPL 2026: Two New Teams Announced', 'description': 'Two new franchises have been added to the Indian Premier League.', 'category': 'Cricket', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'IPL Official'},
                {'title': 'Rohit Sharma Becomes Fastest to 10K ODI Runs', 'description': 'Indian captain achieved this milestone in just 205 innings.', 'category': 'Cricket', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'ICC'},
                {'title': 'Jasprit Bumrah Returns to Bowling', 'description': 'Star pacer makes a strong comeback after injury.', 'category': 'Cricket', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'Cricket Today'}
            ],
            'football': [
                {'title': 'Manchester City Wins Premier League Title', 'description': 'City secured their third consecutive Premier League title.', 'category': 'Football', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'EPL News'},
                {'title': 'World Cup 2026: Qualifiers Update', 'description': 'Exciting matches happening in World Cup qualifiers.', 'category': 'Football', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'FIFA'},
                {'title': 'Cristiano Ronaldo Scores 900th Career Goal', 'description': 'The Portuguese legend continues to break records.', 'category': 'Football', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'Football News'},
                {'title': 'Liverpool Signs Star Midfielder', 'description': 'Liverpool FC announced signing of a top midfielder.', 'category': 'Football', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'Transfer News'},
                {'title': 'Barcelona Wins El Clasico', 'description': 'Barcelona defeated Real Madrid 3-1.', 'category': 'Football', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'La Liga'}
            ],
            'basketball': [
                {'title': 'NBA Finals: Lakers vs Celtics', 'description': 'The historic rivalry continues.', 'category': 'Basketball', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'NBA'},
                {'title': 'LeBron James Extends Record', 'description': 'LeBron becomes all-time leading scorer.', 'category': 'Basketball', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'ESPN'},
                {'title': 'FIBA World Cup Qualifiers', 'description': 'National teams compete for spots.', 'category': 'Basketball', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'FIBA'}
            ],
            'tennis': [
                {'title': 'Novak Djokovic Wins Wimbledon', 'description': 'Djokovic secures his 24th Grand Slam title.', 'category': 'Tennis', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'ATP Tour'},
                {'title': 'Coco Gauff Rising Star', 'description': 'Young American continues to impress.', 'category': 'Tennis', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'WTA'},
                {'title': 'US Open 2026 Preview', 'description': 'Final Grand Slam of the year.', 'category': 'Tennis', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'Tennis News'}
            ],
            'f1': [
                {'title': 'Max Verstappen Wins Monaco GP', 'description': 'Red Bull driver extends championship lead.', 'category': 'F1 Racing', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'F1'},
                {'title': 'Lewis Hamilton Signs New Contract', 'description': 'Seven-time champion extends stay with Mercedes.', 'category': 'F1 Racing', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'Motorsport'},
                {'title': 'Audi Joins F1 in 2026', 'description': 'German manufacturer officially enters F1.', 'category': 'F1 Racing', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'F1 News'}
            ],
            'badminton': [
                {'title': 'PV Sindhu Wins Indonesia Open', 'description': 'Indian shuttler wins first title of the season.', 'category': 'Badminton', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'BWF'},
                {'title': 'Viktor Axelsen Dominates Badminton', 'description': 'World No. 1 continues incredible run.', 'category': 'Badminton', 'date': datetime.now().strftime('%d %B, %Y'), 'source': 'Badminton News'}
            ]
        }
        
        self.sport_emojis = {
            'cricket': '🏏',
            'football': '⚽',
            'basketball': '🏀',
            'tennis': '🎾',
            'f1': '🏎️',
            'badminton': '🏸'
        }
        self.sport_names = {
            'cricket': 'Cricket',
            'football': 'Football',
            'basketball': 'Basketball',
            'tennis': 'Tennis',
            'f1': 'F1 Racing',
            'badminton': 'Badminton'
        }
        
    def get_news_by_sport(self, sport):
        if sport.lower() in self.news:
            return self.news[sport.lower()]
        return []
    
    def get_all_news(self, limit=8):
        all_news = []
        for sport, items in self.news.items():
            all_news.extend(items)
        random.shuffle(all_news)
        return all_news[:limit]
    
    def get_latest_news(self, count=5):
        all_news = self.get_all_news(count * 2)
        return all_news[:count]
    
    def search_news(self, query):
        results = []
        query = query.lower()
        for sport, items in self.news.items():
            for item in items:
                if query in item['title'].lower() or query in item['description'].lower():
                    results.append(item)
        return results

# Initialize news database
news_db = SportsNewsDB()
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if user.id not in user_data:
        user_data[user.id] = {'favorites': [], 'preferences': {'sport': 'all', 'notifications': False}}
    
    keyboard = [
        [InlineKeyboardButton("🏏 Cricket", callback_data='sport_cricket'),
         InlineKeyboardButton("⚽ Football", callback_data='sport_football')],
        [InlineKeyboardButton("🏀 Basketball", callback_data='sport_basketball'),
         InlineKeyboardButton("🎾 Tennis", callback_data='sport_tennis')],
        [InlineKeyboardButton("🏎️ F1 Racing", callback_data='sport_f1'),
         InlineKeyboardButton("🏸 Badminton", callback_data='sport_badminton')],
        [InlineKeyboardButton("📰 All Sports", callback_data='sport_all')],
        [InlineKeyboardButton("⭐ Favorites", callback_data='show_favorites'),
         InlineKeyboardButton("🔍 Search", callback_data='search_news')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"🏆 *Welcome to Sports News Bot, {user.first_name}!*\n\n"
        "Get the latest sports news, updates, and scores.\n\n"
        "📌 *How to use:*\n"
        "• Choose a sport below to see news\n"
        "• Use /latest for recent updates\n"
        "• Add favorites with /fav [news title]\n"
        "• Search with /search [keyword]\n\n"
        "🌟 *Available Sports:* Cricket, Football, Basketball, Tennis, F1, Badminton"
    )
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 *Sports News Bot Help*

*Commands:*
/start - Start the bot
/help - Show this help
/latest - Get latest news
/popular - Most popular news
/fav [news title] - Add to favorites
/favorites - View your favorites
/search [keyword] - Search news
/sport [sport] - Get sport-specific news
/about - About this bot

*Sports Available:*
🏏 Cricket ⚽ Football 🏀 Basketball
🎾 Tennis 🏎️ F1 Racing 🏸 Badminton
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def latest_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_items = news_db.get_latest_news(5)
    
    if not news_items:
        await update.message.reply_text("No news available at the moment.")
        return
    
    message = "📰 *Latest Sports News*\n" + "="*30 + "\n\n"
    for i, item in enumerate(news_items, 1):
        message += f"*{i}. {item['title']}*\n"
        message += f"📝 {item['description'][:150]}...\n"
        message += f"📅 {item['date']} | 📌 {item['category']}\n\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def popular_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_items = news_db.get_all_news(5)
    
    message = "🔥 *Popular Sports News*\n" + "="*30 + "\n\n"
    for i, item in enumerate(news_items, 1):
        message += f"*{i}. {item['title']}*\n"
        message += f"📝 {item['description'][:120]}...\n"
        message += f"⭐ Popularity: {'⭐' * (6-i)}\n\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def show_sport_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    sport = query.data.replace('sport_', '')
    
    if sport == 'all':
        news_items = news_db.get_all_news(8)
        title = "📰 *All Sports News*"
    else:
        news_items = news_db.get_news_by_sport(sport)
        emoji = news_db.sport_emojis.get(sport, '📌')
        name = news_db.sport_names.get(sport, sport.title())
        title = f"{emoji} *{name} News*"
    
    if not news_items:
        await query.message.reply_text("No news available for this sport.")
        return
    
    message = title + "\n" + "="*30 + "\n\n"
    
    for i, item in enumerate(news_items[:5], 1):
        message += f"*{i}. {item['title']}*\n"
        message += f"📝 {item['description'][:120]}...\n"
        message += f"📅 {item['date']} | 📌 {item['category']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f'refresh_{sport}')],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data='back_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('sport_'):
        await show_sport_news(update, context)
    elif query.data.startswith('refresh_'):
        await show_sport_news(update, context)
    elif query.data == 'back_menu':
        await start(update, context)
    elif query.data == 'show_favorites':
        user_id = update.effective_user.id
        if user_id not in user_data or not user_data[user_id]['favorites']:
            await query.message.reply_text("⭐ You have no favorites yet.")
        else:
            message = "⭐ *Your Favorites*\n" + "="*30 + "\n\n"
            for i, title in enumerate(user_data[user_id]['favorites'][:10], 1):
                message += f"{i}. {title}\n"
            await query.message.reply_text(message, parse_mode='Markdown')
    elif query.data == 'search_news':
        await query.message.reply_text("🔍 Type /search [your keyword]")

async def search_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🔍 Please provide a search term.\nExample: /search world cup")
        return
    
    query = ' '.join(context.args)
    results = news_db.search_news(query)
    
    if not results:
        await update.message.reply_text(f"No news found for: '{query}'")
        return
    
    message = f"🔍 *Search Results for: '{query}'*\n" + "="*30 + "\n\n"
    for i, item in enumerate(results[:5], 1):
        message += f"*{i}. {item['title']}*\n"
        message += f"📝 {item['description'][:100]}...\n"
        message += f"📌 {item['category']}\n\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def add_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⭐ Please provide a news title.\nExample: /fav World Cup")
        return
    
    query = ' '.join(context.args).lower()
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {'favorites': [], 'preferences': {}}
    
    found = None
    for sport, items in news_db.news.items():
        for item in items:
            if query in item['title'].lower():
                found = item
                break
        if found:
            break
    
    if found:
        if found['title'] not in user_data[user_id]['favorites']:
            user_data[user_id]['favorites'].append(found['title'])
            await update.message.reply_text(f"⭐ Added to favorites:\n{found['title']}")
        else:
            await update.message.reply_text("Already in favorites!")
    else:
        await update.message.reply_text("No news found with that title.")

async def view_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in user_data or not user_data[user_id]['favorites']:
        await update.message.reply_text("⭐ You have no favorites yet.")
        return
    
    message = "⭐ *Your Favorites*\n" + "="*30 + "\n\n"
    for i, title in enumerate(user_data[user_id]['favorites'][:10], 1):
        message += f"{i}. {title}\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = """
🤖 *Sports News Bot*

Version: 1.0.0
Created: 2026

*Features:*
• 6 Sports categories
• Favorites system
• Smart search
• No API required

*Sports:*
🏏 Cricket ⚽ Football 🏀 Basketball
🎾 Tennis 🏎️ F1 Racing 🏸 Badminton

Made with ❤️ for sports fans
    """
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("⚠️ An error occurred. Please try again.")

def main():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN not set!")
        logger.error("Please add environment variable: TELEGRAM_BOT_TOKEN")
        return
    
    logger.info("✅ Token found! Starting bot...")
    
    try:
        # Create application
        application = Application.builder().token(token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("latest", latest_news))
        application.add_handler(CommandHandler("popular", popular_news))
        application.add_handler(CommandHandler("search", search_news))
        application.add_handler(CommandHandler("fav", add_favorite))
        application.add_handler(CommandHandler("favorites", view_favorites))
        application.add_handler(CommandHandler("about", about))
        
        # Add callback query handler for buttons
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Start the bot
        logger.info("🏆 Sports News Bot is running...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

if __name__ == '__main__':
    main()
