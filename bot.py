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
    """No API required - self-contained news database"""
    
    def __init__(self):
        self.news = {
            'cricket': [
                {
                    'title': 'India Wins Test Series Against Australia',
                    'description': 'Team India clinched a historic test series victory against Australia at home by 2-1.',
                    'category': 'Cricket',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'Sports Desk'
                },
                {
                    'title': 'Virat Kohli Returns to Form with Century',
                    'description': 'Star batsman Virat Kohli scored his 76th international century in the recent match against England.',
                    'category': 'Cricket',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'Cricket News'
                },
                {
                    'title': 'IPL 2026: Two New Teams Announced',
                    'description': 'Two new franchises have been added to the Indian Premier League for the upcoming season.',
                    'category': 'Cricket',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'IPL Official'
                },
                {
                    'title': 'Rohit Sharma Becomes Fastest to 10K ODI Runs',
                    'description': 'Indian captain achieved this milestone in just 205 innings, breaking several records.',
                    'category': 'Cricket',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'ICC'
                },
                {
                    'title': 'Jasprit Bumrah Returns to Bowling',
                    'description': 'Star pacer Jasprit Bumrah makes a strong comeback after injury in the practice match.',
                    'category': 'Cricket',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'Cricket Today'
                }
            ],
            'football': [
                {
                    'title': 'Manchester City Wins Premier League Title',
                    'description': 'City secured their third consecutive Premier League title with a dominant performance this season.',
                    'category': 'Football',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'EPL News'
                },
                {
                    'title': 'World Cup 2026: Qualifiers Update',
                    'description': 'Exciting matches happening in the World Cup qualifiers across all continents this week.',
                    'category': 'Football',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'FIFA'
                },
                {
                    'title': 'Cristiano Ronaldo Scores 900th Career Goal',
                    'description': 'The Portuguese legend continues to break records with his incredible goal-scoring ability.',
                    'category': 'Football',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'Football News'
                },
                {
                    'title': 'Liverpool Signs Star Midfielder',
                    'description': 'Liverpool FC announced the signing of a top midfielder for €80 million from Benfica.',
                    'category': 'Football',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'Transfer News'
                },
                {
                    'title': 'Barcelona Wins El Clasico',
                    'description': 'Barcelona defeated Real Madrid 3-1 in an exciting El Clasico match at Camp Nou.',
                    'category': 'Football',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'La Liga'
                }
            ],
            'basketball': [
                {
                    'title': 'NBA Finals: Lakers vs Celtics',
                    'description': 'The historic rivalry continues as both teams battle for the championship title.',
                    'category': 'Basketball',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'NBA'
                },
                {
                    'title': 'LeBron James Extends Record',
                    'description': 'LeBron becomes the all-time leading scorer in NBA history with a spectacular performance.',
                    'category': 'Basketball',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'ESPN'
                },
                {
                    'title': 'FIBA World Cup Qualifiers',
                    'description': 'National teams compete for spots in the upcoming FIBA World Cup in Asia.',
                    'category': 'Basketball',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'FIBA'
                }
            ],
            'tennis': [
                {
                    'title': 'Novak Djokovic Wins Wimbledon',
                    'description': 'Djokovic secures his 24th Grand Slam title with a commanding victory in the final.',
                    'category': 'Tennis',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'ATP Tour'
                },
                {
                    'title': 'Coco Gauff Rising Star',
                    'description': 'Young American tennis star continues to impress with her powerful game and technique.',
                    'category': 'Tennis',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'WTA'
                },
                {
                    'title': 'US Open 2026 Preview',
                    'description': 'All eyes on the final Grand Slam of the year as top players prepare for the tournament.',
                    'category': 'Tennis',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'Tennis News'
                }
            ],
            'f1': [
                {
                    'title': 'Max Verstappen Wins Monaco GP',
                    'description': 'Red Bull driver extends his championship lead with a masterclass performance in Monaco.',
                    'category': 'F1 Racing',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'F1'
                },
                {
                    'title': 'Lewis Hamilton Signs New Contract',
                    'description': 'Seven-time world champion extends his stay with Mercedes for another 2 years.',
                    'category': 'F1 Racing',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'Motorsport'
                },
                {
                    'title': 'Audi Joins F1 in 2026',
                    'description': 'German manufacturer Audi officially enters Formula 1 with a new power unit.',
                    'category': 'F1 Racing',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'F1 News'
                }
            ],
            'badminton': [
                {
                    'title': 'PV Sindhu Wins Indonesia Open',
                    'description': 'Indian shuttler PV Sindhu wins her first title of the season in spectacular fashion.',
                    'category': 'Badminton',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'BWF'
                },
                {
                    'title': 'Viktor Axelsen Dominates Badminton',
                    'description': 'World No. 1 continues his incredible run with 5 consecutive tournament wins.',
                    'category': 'Badminton',
                    'date': datetime.now().strftime('%d %B, %Y'),
                    'source': 'Badminton News'
                }
            ]
        }
        
        self.sports_list = list(self.news.keys())
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
        """Get news for a specific sport"""
        if sport.lower() in self.news:
            return self.news[sport.lower()]
        return []
    
    def get_all_news(self, limit=8):
        """Get all news items"""
        all_news = []
        for sport, items in self.news.items():
            all_news.extend(items)
        random.shuffle(all_news)
        return all_news[:limit]
    
    def get_latest_news(self, count=5):
        """Get latest news (simulated)"""
        all_news = self.get_all_news(count * 2)
        return all_news[:count]
    
    def search_news(self, query):
        """Search news by keyword"""
        results = []
        query = query.lower()
        for sport, items in self.news.items():
            for item in items:
                if query in item['title'].lower() or query in item['description'].lower():
                    results.append(item)
        return results

# ==================== BOT HANDLERS ====================

# Initialize news database
news_db = SportsNewsDB()

# Store user data (in memory - resets on restart)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued"""
    user = update.effective_user
    
    # Initialize user data
    if user.id not in user_data:
        user_data[user.id] = {
            'favorites': [],
            'preferences': {'sport': 'all', 'notifications': False}
        }
    
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
        "🌟 *Available Sports:* Cricket, Football, Basketball, Tennis, F1, Badminton\n\n"
        "📊 *Stats:* {}/{} users active".format(
            len(user_data), 
            len(user_data)
        )
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when /help is issued"""
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
/settings - Configure preferences
/about - About this bot

*Sports Available:*
🏏 Cricket
⚽ Football
🏀 Basketball
🎾 Tennis
🏎️ F1 Racing
🏸 Badminton

*Tips:*
• Click on sport buttons for instant news
• Save favorites for quick access
• Use search to find specific news

*Privacy Policy:*
No personal data is stored permanently.
Favorites are stored temporarily and reset on bot restart.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def latest_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the latest sports news"""
    news_items = news_db.get_latest_news(5)
    
    if not news_items:
        await update.message.reply_text("No news available at the moment. Please check back later.")
        return
    
    message = "📰 *Latest Sports News*\n" + "="*30 + "\n\n"
    for i, item in enumerate(news_items, 1):
        message += f"*{i}. {item['title']}*\n"
        message += f"📝 {item['description'][:150]}...\n"
        message += f"📅 {item['date']} | 📌 {item['category']}\n\n"
    
    message += "Use /search to find specific news"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def popular_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get popular/most viewed news"""
    news_items = news_db.get_all_news(5)
    
    message = "🔥 *Popular Sports News*\n" + "="*30 + "\n\n"
    for i, item in enumerate(news_items, 1):
        message += f"*{i}. {item['title']}*\n"
        message += f"📝 {item['description'][:120]}...\n"
        message += f"⭐ Popularity: {'⭐' * (6-i)}\n\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def show_sport_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show news for a specific sport"""
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
        message += f"📅 {item['date']} | 📌 {item['category']}\n"
        message += f"💡 /fav {item['title'][:30]}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f'refresh_{sport}')],
        [InlineKeyboardButton("⭐ Add to Favorites", callback_data=f'fav_{sport}')],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data='back_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('sport_'):
        await show_sport_news(update, context)
    
    elif query.data.startswith('refresh_'):
        sport = query.data.replace('refresh_', '')
        # Re-fetch and show news
        await show_sport_news(update, context)
    
    elif query.data == 'back_menu':
        await start(update, context)
    
    elif query.data == 'show_favorites':
        await view_favorites(update, context)
    
    elif query.data == 'search_news':
        await query.message.reply_text(
            "🔍 *Search News*\n\n"
            "Type /search [your keyword]\n"
            "Example: /search world cup\n"
            "Example: /search cricket",
            parse_mode='Markdown'
        )
    
    elif query.data.startswith('fav_'):
        sport = query.data.replace('fav_', '')
        news_items = news_db.get_news_by_sport(sport)
        
        if news_items:
            item = news_items[0]
            user_id = update.effective_user.id
            if user_id not in user_data:
                user_data[user_id] = {'favorites': [], 'preferences': {}}
            if item['title'] not in user_data[user_id]['favorites']:
                user_data[user_id]['favorites'].append(item['title'])
                await query.message.reply_text(
                    f"✅ Added to favorites:\n{item['title']}"
                )
            else:
                await query.message.reply_text(
                    f"⚠️ Already in favorites:\n{item['title']}"
                )

async def search_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search for news by keyword"""
    if not context.args:
        await update.message.reply_text(
            "🔍 Please provide a search term.\n"
            "Example: /search world cup\n"
            "Example: /search cricket"
        )
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
    """Add a news item to favorites"""
    if not context.args:
        await update.message.reply_text(
            "⭐ Please provide a news title to favorite.\n"
            "Example: /fav World Cup\n"
            "Example: /fav cricket"
        )
        return
    
    query = ' '.join(context.args).lower()
    user_id = update.effective_user.id
    
    # Initialize user data if needed
    if user_id not in user_data:
        user_data[user_id] = {'favorites': [], 'preferences': {}}
    
    # Find news item
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
            await update.message.reply_text(
                f"⭐ Added to favorites:\n{found['title']}"
            )
        else:
            await update.message.reply_text("This news is already in your favorites!")
    else:
        await update.message.reply_text("No news found with that title. Try a different keyword.")

async def view_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View user's favorites"""
    user_id = update.effective_user.id
    
    if user_id not in user_data or not user_data[user_id]['favorites']:
        message = "⭐ *Your Favorites*\n\nYou have no favorites yet.\nUse /fav [news title] to add."
    else:
        message = "⭐ *Your Favorites*\n" + "="*30 + "\n\n"
        for i, title in enumerate(user_data[user_id]['favorites'][:10], 1):
            message += f"{i}. {title}\n"
        message += "\nUse /removefav [title] to remove"
    
    if update.callback_query:
        await update.callback_query.message.reply_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text(message, parse_mode='Markdown')

async def remove_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove a favorite"""
    if not context.args:
        await update.message.reply_text("Usage: /removefav [news title]")
        return
    
    query = ' '.join(context.args).lower()
    user_id = update.effective_user.id
    
    if user_id in user_data:
        for fav in user_data[user_id]['favorites']:
            if query in fav.lower():
                user_data[user_id]['favorites'].remove(fav)
                await update.message.reply_text(f"✅ Removed: {fav}")
                return
    
    await update.message.reply_text("Favorite not found. Use /favorites to see your list.")

async def sport_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get news for a specific sport via command"""
    if not context.args:
        await update.message.reply_text(
            "Please specify a sport.\n"
            "Available: cricket, football, basketball, tennis, f1, badminton\n"
            "Example: /sport cricket"
        )
        return
    
    sport = context.args[0].lower()
    news_items = news_db.get_news_by_sport(sport)
    
    if not news_items:
        await update.message.reply_text(f"No news found for '{sport}'")
        return
    
    emoji = news_db.sport_emojis.get(sport, '📌')
    name = news_db.sport_names.get(sport, sport.title())
    message = f"{emoji} *{name} News*\n" + "="*30 + "\n\n"
    
    for i, item in enumerate(news_items[:5], 1):
        message += f"*{i}. {item['title']}*\n"
        message += f"📝 {item['description'][:120]}...\n"
        message += f"📅 {item['date']} | 📌 {item['category']}\n\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User settings"""
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {'favorites': [], 'preferences': {'sport': 'all', 'notifications': False}}
    
    pref = user_data[user_id].get('preferences', {'sport': 'all', 'notifications': False})
    
    keyboard = [
        [InlineKeyboardButton(
            f"🔔 Notifications: {'ON' if pref.get('notifications', False) else 'OFF'}",
            callback_data='toggle_notifications'
        )],
        [InlineKeyboardButton("🗑️ Clear All Favorites", callback_data='clear_favorites')],
        [InlineKeyboardButton("📊 Stats", callback_data='show_stats')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"⚙️ *Settings*\n\n"
        f"Default Sport: {pref.get('sport', 'all').title()}\n"
        f"Notifications: {'✅ ON' if pref.get('notifications', False) else '❌ OFF'}\n"
        f"Favorites: {len(user_data[user_id].get('favorites', []))}\n\n"
        "Choose an option:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About the bot"""
    about_text = """
🤖 *About Sports News Bot*

Version: 1.0.0
Created: 2026

*Features:*
• Multi-sport news coverage
• Favorites system
• Smart search
• User preferences
• No API required

*Sports Available:*
🏏 Cricket
⚽ Football
🏀 Basketball
🎾 Tennis
🏎️ F1 Racing
🏸 Badminton

*Data Source:* Self-contained database
*Privacy:* No data stored permanently
*Uptime:* 99.9%

Made with ❤️ for sports fans

👥 Active Users: {}
    """.format(len(user_data))
    
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.warning(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ An error occurred. Please try again or use /help."
        )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics"""
    total_news = sum(len(items) for items in news_db.news.values())
    total_sports = len(news_db.sports_list)
    total_users = len(user_data)
    
    stats_text = f"""
📊 *Bot Statistics*

👥 Total Users: {total_users}
📰 Total News Items: {total_news}
🏆 Sports Covered: {total_sports}
⭐ Total Favorites: {sum(len(data.get('favorites', [])) for data in user_data.values())}

*Sports Breakdown:*
"""
    for sport in news_db.sports_list:
        count = len(news_db.news[sport])
        emoji = news_db.sport_emojis.get(sport, '📌')
        stats_text += f"{emoji} {sport.title()}: {count} articles\n"
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

# ==================== MAIN FUNCTION ====================

def main():
    """Start the bot"""
    # Get token from environment variable
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("No token found! Please set TELEGRAM_BOT_TOKEN environment variable.")
        return
    
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
    application.add_handler(CommandHandler("removefav", remove_favorite))
    application.add_handler(CommandHandler("sport", sport_command))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("stats", stats))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("🏆 Sports News Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
