from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
from PIL import Image
import os

# SPI ühendus
serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
device = ili9341(serial)

# Kuvame pildi
def display_image(image_path):
    if os.path.exists(image_path):
        img = Image.open(image_path).resize((240, 320))  # Kohanda suurus ekraani jaoks
        device.display(img)
    else:
        print("Faili ei leitud:", image_path)

# Näide
image_path = "static/uploads/test_image.jpg"
display_image(image_path)
