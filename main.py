import os
import requests
import m3u8
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# M3U8 video download function
def download_m3u8(url, download_path):
    playlist = m3u8.load(url)
    segments = playlist.segments
    os.makedirs(download_path, exist_ok=True)
    
    for i, segment in enumerate(segments):
        segment_url = segment.uri
        segment_data = requests.get(segment_url).content
        with open(os.path.join(download_path, f"segment_{i}.ts"), 'wb') as file:
            file.write(segment_data)

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me an M3U8 URL and I will download the video for you.")

# Download command handler
def download(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 1:
        url = context.args[0]
        download_path = "downloads"
        download_m3u8(url, download_path)
        update.message.reply_text("Download started!")
    else:
        update.message.reply_text("Please send a valid M3U8 URL.")

def main():
    # Your bot's API token from BotFather
    TOKEN = 'YOUR_BOT_API_TOKEN'

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("download", download))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    