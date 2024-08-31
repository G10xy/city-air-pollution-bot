FROM python:3.11-alpine

WORKDIR /app

COPY src/ .
COPY requirements.txt .

# Install necessary packages for downloading fonts and handling fonts
RUN apk add --no-cache wget fontconfig

# Create a directory for TrueType fonts and download a font
RUN mkdir -p /usr/share/fonts/truetype && wget -O /usr/share/fonts/truetype/custom-font.ttf https://github.com/prawnpdf/prawn/blob/master/data/fonts/DejaVuSans.ttf

# Rebuild the font cache
RUN chmod 644 /usr/share/fonts/truetype/* && fc-cache -fv

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python3", "bot.py"]
