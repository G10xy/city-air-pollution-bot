import telebot
from rest_data_fetcher import RestDataFetcher
from image_handler import ImageHandler
import os

TELEGRAM_TOKEN = ''

class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.user_choice = None
        self.data_fetcher = RestDataFetcher()
        self.image_handler = ImageHandler()
        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
            current_button = telebot.types.KeyboardButton('Current')
            forecast_button = telebot.types.KeyboardButton('Forecast')
            history_button = telebot.types.KeyboardButton('History')
            markup.add(current_button, forecast_button, history_button)
            self.bot.send_message(message.chat.id, 'Choose an option:', reply_markup=markup)

        @self.bot.message_handler(func=lambda message: message.text in ['Current', 'Forecast', 'History'])
        def handle_option(message):
            self.user_choice = message.text
            self.bot.send_message(message.chat.id, 'Please enter the city name you want to get air pollution data of:')

        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            city_name = message.text
            try:
                lat, lon = self.data_fetcher.get_coordinates(city_name)
                if self.user_choice == 'Current':
                    air_quality_data = self.data_fetcher.get_current_air_quality(lat, lon)
                    img = self.image_handler.create_image(air_quality_data, city_name)
                elif self.user_choice == 'Forecast':
                    air_quality_data = self.data_fetcher.get_forecast_air_quality(lat, lon)
                    img = self.image_handler.create_image(air_quality_data, city_name)
                elif self.user_choice == 'History':
                    air_quality_data = self.data_fetcher.get_historical_air_quality(lat, lon)
                    img = self.image_handler.create_image_average_week(air_quality_data, city_name)
                img.save('air-pollution.png')
                with open('air-pollution.png', 'rb') as photo:
                    self.bot.send_photo(message.chat.id, photo)
                os.remove('air-pollution.png')
            except Exception as e:
                self.bot.send_message(message.chat.id, f"Error: {str(e)}")


if __name__ == '__main__':
    bot_instance = Bot(TELEGRAM_TOKEN)
    if bot_instance:
        print('Bot running')
        bot_instance.bot.polling()
    else:
        print('Bot problem')
