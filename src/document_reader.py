from io import BytesIO
import os
import sys
from time import sleep
import logging

import pytesseract
from gtts import gTTS
from PIL import Image
from picamera import PiCamera


class OCR:

    def extract_text(self, image_path, language="eng"):
        try:
            image = Image.open(image_path)
            return pytesseract.image_to_string(image, lang=language)
        except Exception as e:
            logging.error("can not extract text from image - {}".format(e.message))


class TTS:

    def text_to_speech(self, text, save_to, language="en"):
        try:
            tts = gTTS(text=text, lang=language)
            tts.save(save_to)

        except Exception as e:
            logging.error("can not convert text to speech")
            print(str(e))


class DocumentReader:

    image_dir = "/tmp/images"
    image_path = "{}/{}".format(image_dir, "image.jpg")

    mp3_dir = "/tmp/mp3-files"
    mp3_file = "{}/{}".format(mp3_dir, "speech.mp3")

    def __init__(self):
        if not os.path.exists(self.mp3_dir):
            os.mkdir(self.mp3_dir, 0o755)


    def run(self):
        self.capture_image(self.image_path)
        text = OCR().extract_text(self.image_path)
        logging.info("extracted text: {}".format(text))

        TTS().text_to_speech(text, self.mp3_file, "en")
        try:
            os.system("mpg123 {}".format(self.mp3_file))
        except Exception as e:
            logging.error("can not read mp3 file - {}".format(e.message))

        self.clean()

    def capture_image(self, save_to):
        try:
            camera = PiCamera()
            logging.debug("About to take an image...")
            camera.capture(save_to)
            logging.debug("Image taken...")

        except Exception as e:
            logging.error("can not capture image - {}".format(e.message))

    def clean(self):
        logging.debug("cleaning image files...")
        os.remove(self.image_path)
        logging.debug("cleaning mp3 files...")
        os.system(self.mp3_file)
        logging.debug("All cleaned up !")