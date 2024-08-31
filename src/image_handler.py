from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

class ImageHandler:
    def get_color_from_aqi(self, aqi):
        if aqi == 1:
            return (0, 255, 0)  # Green for Good
        elif aqi == 2:
            return (255, 255, 0)  # Yellow for Moderate
        elif aqi == 3:
            return (255, 165, 0)  # Orange for Unhealthy for Sensitive Groups
        elif aqi == 4:
            return (255, 0, 0)  # Red for Unhealthy
        elif aqi == 5:
            return (153, 50, 204)  # Dark Violet for Very Unhealthy
        else:
            return (128, 0, 0)  # Maroon for Hazardous

    def create_image(self, data, city_name):
        img = Image.new('RGB', (400, 300), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        font_size = 20
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        aqi = data['list'][0]['main']['aqi']
        color = self.get_color_from_aqi(aqi)
        metrics = [
            ('Air Quality Index', aqi),
            ('CO', data['list'][0]['components']['co']),
            ('NO2', data['list'][0]['components']['no2']),
            ('O3', data['list'][0]['components']['o3']),
            ('PM2.5', data['list'][0]['components']['pm2_5']),
            ('PM10', data['list'][0]['components']['pm10'])
        ]
        now = datetime.now()
        d.text((10, 10), f"Air Quality in {city_name.capitalize()} at {now.day}/{now.month}/{now.year}", fill=(0, 0, 0), font=font)
        start_y = 40
        for metric, value in metrics:
            metric_color = color if metric == "Air Quality Index" else (0, 0, 0)
            d.text((10, start_y), f'• {metric}: {value}', fill=metric_color, font=font)
            start_y += 30

        return img

    def create_image_average_week(self, data, city_name):
        img = Image.new('RGB', (400, 300), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        font_size = 15
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/custom-font.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        list_part = data['list']

        aqi_list = [i['main']['aqi'] for i in list_part]
        aqi = int(sum(aqi_list) / len(aqi_list))

        co_list = [i['components']['co'] for i in list_part]
        co = round(sum(co_list) / len(co_list), 2)

        no2_list = [i['components']['no2'] for i in list_part]
        no2 = round(sum(no2_list) / len(no2_list), 2)

        o3_list = [i['components']['o3'] for i in list_part]
        o3 = round(sum(o3_list) / len(o3_list), 2)

        pm2_5_list = [i['components']['pm2_5'] for i in list_part]
        pm2_5 = round(sum(pm2_5_list) / len(pm2_5_list), 2)

        pm10_list = [i['components']['pm10'] for i in list_part]
        pm10 = round(sum(pm10_list) / len(pm10_list), 2)

        color = self.get_color_from_aqi(aqi)
        metrics = [
            ('Air Quality Index', aqi),
            ('CO', co),
            ('NO2', no2),
            ('O3', o3),
            ('PM2.5', pm2_5),
            ('PM10', pm10)
        ]

        d.text((10, 10), f"Air Quality Average in {city_name.capitalize()} for the last week", fill=(0, 0, 0), font=font)
        start_y = 40
        for metric, value in metrics:
            metric_color = color if metric == "Air Quality Index" else (0, 0, 0)
            d.text((10, start_y), f'• {metric}: {value}', fill=metric_color, font=font)
            start_y += 30

        return img
