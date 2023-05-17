from telegram import Update
from telegram.ext import Updater, CommandHandler
import requests
import json

def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to your weather bot!")

def weather(update: Update, context):
    location = " ".join(context.args)
    api_key = ""

    # Make API call to get weather information
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()

    print(json.dumps(weather_data, indent=4))  # Print the API response to the console

    if weather_data["cod"] == 200:
        # Extract relevant weather information from the response
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]

        # Send weather information to the user
        message = f"Weather in {location}:\nTemperature: {temperature}K\nDescription: {description}"
    else:
        message = "Failed to retrieve weather information. Please try again."

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def main():
    bot_token = ""
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("weather", weather))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
