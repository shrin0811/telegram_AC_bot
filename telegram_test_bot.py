
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from datetime import datetime
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Google Sheets Configuration
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "C:/Users/SHRINJANA/Downloads/test_tele_bot/telegrambottest-443210-ffb3f27308b5.json"  
# This .json file will contain your private API key from Google Drive to connect it with your code, to remotely access the sheets, and log the progress there. 
SPREADSHEET_NAME = "tele_test_2"  # Replace with your Google Sheet's name

# Initialize Google Sheets API
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
gc = gspread.authorize(credentials)
sheet = gc.open(SPREADSHEET_NAME).sheet1  # Use the first sheet

generic_astro_words= ['sun', 'mercury', 'venus', 'earth', 'moon', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'belt', 
                      'sky', 'summer', 'winter', 'spring', 'autumn', 'north', 'east', 'south', 'west', 'northern', 'southern', 'eastern', 'western', 'asterism', 
                      'constellation', 'star', 'planet', 'asteroid', 'galaxy', 'galaxies', 'cluster', 'year', 'gap', 'opposition', 'retrograde']

def age_cat(text: str) -> str: 
    if any(word in text.lower() for word in ['junior', 'juniors']):
        return 'junior'
    elif any(word in text.lower() for word in ['senior', 'seniors']):
        return 'senior'
    else:
        return 'general - no age'
    
def categorize(text: str) -> str:
    if 'estimation' in text.lower():
        return 'Estimation - R0'
    elif 'theory jeopardy' in text.lower():
        return 'Theory Jeopardy - R1'
    elif any(word in text.lower() for word in ['observation jeopardy', 'obs jeopardy', 'observation']):
        return 'Obs Jeopardy - R1'
    elif 'jeopardy' in text.lower():
        return 'Jeopardy - R1'
    elif any(word in text.lower() for word in ['mystery', 'mystery round']):
        return 'Mystery - R2'
    elif any(word in text.lower() for word in ['buzzer round', 'buzzer', 'buzz']):
        return 'Buzzer - R3'
    elif any(word in text.lower() for word in generic_astro_words):
        return 'general uncategorized question'
    else:
        return 'general'

# Telegram Bot Handlers
def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message."""
    update.message.reply_text("Hello! Send me a message, photo, or video, and I'll log it to Google Sheets.")
    
async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages with text, photos, or videos."""
    try:
        category = "" 
        age_category=""
        user = update.effective_user
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = update.message.text or update.message.caption or "No text"
        media_url = None

        # Handle photos
        if update.message.photo:
            photo = update.message.photo[-1]  # Get the highest resolution photo
            file = await context.bot.get_file(photo.file_id)  # Await the coroutine
            media_url = f"{file.file_path}"

        # Handle videos
        elif update.message.video:
            video = update.message.video
            file = await context.bot.get_file(video.file_id)  # Await the coroutine
            media_url = f"{file.file_path}"
        
        chat_id = update.message.chat.id
        message_id = update.message.message_id
        
        if update.message.chat.username:
            message_link = f"https://t.me/{update.message.chat.username}/{message_id}"
        else:
            message_link = f"https://t.me/c/{chat_id}/{message_id}"
        
        #media_url = message_link
        
        category = categorize(text)
        age_category = age_cat(text)

        # Log message details
        logging.info(f"User: {user.username}, Text: {text}, Media URL: {media_url}, Category:{category}")

        # Append data to Google Sheets
        if (category=='general' and text=='No text') or (category!='general') or media_url:
            sheet.append_row([timestamp, text, media_url, category, age_category, user.username])
            category = "" 
            age_category=""
        time.sleep(1)  #This allows a time lag to allow telegram to log the response, and then push to sheets. 
        category = "" 
        age_category=""
         
        #await update.message.reply_text("Message logged successfully!")

    except Exception as e:
        logging.error(f"Error handling message: {e}")
        await update.message.reply_text("There was an error processing your message.")

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the bot is started."""
    await update.message.reply_text("Hi! Send me a message, photo, or video, and I'll log it.")


# Main function to run the bot
def main():
    # Replace this with your actual bot token
    TELEGRAM_TOKEN = "8060386574:AAGw17qVjin6WtuUpjO_A4uTS9dkD3mKC0k"

    # Create the application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()


