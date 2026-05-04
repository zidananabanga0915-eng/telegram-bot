from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Restaurant Info
RESTAURANT_NAME = "Joe's Restaurant"
OWNER_CHAT_ID = "7902164997"  # Replace with owner's Telegram chat ID

# Menu
MENU = """
🍽️ *OUR MENU*

🍔 Burger - $5
🍕 Pizza - $8
🍗 Chicken - $6
🍟 Fries - $3
🥤 Drink - $2

Type the food name to order!
"""

# Store orders temporarily
orders = {}

# Main keyboard
def main_keyboard():
    keyboard = [
        [KeyboardButton("🍽️ Menu"), KeyboardButton("🛒 Order")],
        [KeyboardButton("📍 Location"), KeyboardButton("⏰ Opening Hours")],
        [KeyboardButton("📞 Contact Us"), KeyboardButton("🛵 Delivery Info")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Welcome to *{RESTAURANT_NAME}*, {name}!\n\n"
        "We serve delicious meals fresh and fast! 🍔🍕\n\n"
        "How can I help you today?",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

# Handle all messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = update.effective_user.id
    name = update.effective_user.first_name

    # Menu
    if "menu" in text:
        await update.message.reply_text(MENU, parse_mode="Markdown")

    # Opening hours
    elif "opening" in text or "hours" in text:
        await update.message.reply_text(
            "⏰ *Opening Hours*\n\n"
            "Monday - Friday: 8am - 10pm\n"
            "Saturday: 9am - 11pm\n"
            "Sunday: 10am - 8pm",
            parse_mode="Markdown"
        )

    # Location
    elif "location" in text:
        await update.message.reply_text(
            "📍 *Our Location*\n\n"
            "123 Main Street, Downtown\n\n"
            "We are opposite the Central Mall!",
            parse_mode="Markdown"
        )

    # Contact
    elif "contact" in text:
        await update.message.reply_text(
            "📞 *Contact Us*\n\n"
            "Phone: +1234567890\n"
            "Email: joes@restaurant.com\n"
            "Instagram: @joesrestaurant",
            parse_mode="Markdown"
        )

    # Delivery info
    elif "delivery" in text:
        await update.message.reply_text(
            "🛵 *Delivery Info*\n\n"
            "✅ We deliver within 5km radius\n"
            "✅ Delivery fee: $2\n"
            "✅ Estimated time: 30-45 minutes\n"
            "✅ Minimum order: $10",
            parse_mode="Markdown"
        )

    # Order
    elif "order" in text or "burger" in text or "pizza" in text or "chicken" in text or "fries" in text or "drink" in text:
        orders[user_id] = text
        await update.message.reply_text(
            f"🛒 *Order Received!*\n\n"
            f"Thank you {name}! Your order has been placed.\n\n"
            f"📝 Order: {text.title()}\n\n"
            "Please provide your delivery address or let us know if you are picking up! 📍",
            parse_mode="Markdown"
        )
        # Notify owner
        await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=f"🔔 *New Order!*\n\n"
                 f"Customer: {name}\n"
                 f"Order: {text.title()}\n"
                 f"User ID: {user_id}",
            parse_mode="Markdown"
        )

    # Default
    else:
        await update.message.reply_text(
            "Sorry I didn't understand that 😊\n\n"
            "Please use the menu buttons below or type:\n"
            "Menu, Order, Location, Hours, Delivery",
            reply_markup=main_keyboard()
        )

# /help command
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Here is what I can do:*\n\n"
        "🍽️ Show you our Menu\n"
        "🛒 Take your Order\n"
        "📍 Show our Location\n"
        "⏰ Tell you our Opening Hours\n"
        "🛵 Explain Delivery Info\n"
        "📞 Give you our Contact details\n\n"
        "Just press the buttons below!",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

app = ApplicationBuilder().token("8736961543:AAHuNijHyQtg0qM993H1GDjK6tHWPoUGZao").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
