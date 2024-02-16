import os
import telebot
import speech_recognition
from pydub import AudioSegment
from PIL import Image, ImageEnhance, ImageFilter


token = '6503457289:AAHOnU_u-zp9_wfntqSXkkGee5HX1h4-SF4'

bot = telebot.TeleBot(token)


def blur(filename):
    source_image = Image.open(filename)
    enhanced_image = source_image.filter(ImageFilter.BLUR)
    enhanced_image = enhanced_image.convert('RGB')
    width = enhanced_image.size[0]
    height = enhanced_image.size[1]

    enhanced_image = enhanced_image.resize((width // 2, height // 2))

    enhanced_image.save(filename)
    return filename

def detail(filename):
    source_image = Image.open(filename)
    enhanced_image = source_image.filter(ImageFilter.DETAIL)
    enhanced_image = enhanced_image.convert('RGB')
    width = enhanced_image.size[0]
    height = enhanced_image.size[1]

    enhanced_image = enhanced_image.resize((width // 2, height // 2))

    enhanced_image.save(filename)
    return filename

def contour(filename):
    source_image = Image.open(filename)
    enhanced_image = source_image.filter(ImageFilter.CONTOUR)
    enhanced_image = enhanced_image.convert('RGB')
    width = enhanced_image.size[0]
    height = enhanced_image.size[1]

    enhanced_image = enhanced_image.resize((width // 2, height // 2))

    enhanced_image.save(filename)
    return filename

def emboss(filename):
    source_image = Image.open(filename)
    enhanced_image = source_image.filter(ImageFilter.EMBOSS)
    enhanced_image = enhanced_image.convert('RGB')
    width = enhanced_image.size[0]
    height = enhanced_image.size[1]

    enhanced_image = enhanced_image.resize((width // 2, height // 2))

    enhanced_image.save(filename)
    return filename

def oga2wav(filename):
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename


def recognize_speech(oga_filename):
    wav_filename = oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:     
        wav_audio = recognizer.record(source)

    text = recognizer.recognize_google(wav_audio, language='ru')

    if os.path.exists(oga_filename):
        os.remove(oga_filename)

    if os.path.exists(wav_filename):
        os.remove(wav_filename)

    return text


def download_file(bot, file_id):
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path
    filename = filename.replace('/', '_')
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    return filename

@bot.message_handler(content_types=['text'])
def answer(message):
    bot.forward_message(chat_id='administration.chat.id', from_chat_id=message.chat.id, message_id=message.message_id)
    if message.text == 'фильтры':
        bot.send_message(message.chat.id, 'фильтры: emboss, blur, contour, detail. присылай фото с названием фильтра в подписи и я его обработаю. ')
    elif message.text == 'chat.id':
        bot.send_message(message.chat.id, message.chat.id)

@bot.message_handler(commands=['start'])
def say_hi(message):
    bot.forward_message(chat_id='administration.chat.id', from_chat_id=message.chat.id, message_id=message.message_id)
    bot.forward_message(chat_id='administration.chat.id')
    bot.send_message(message.chat.id, 'я могу перевести гс в текст и обработать фото, чтоб посмотреть фильтры - пиши фильтры')


@bot.message_handler(content_types=['voice'])
def transcript(message):
    bot.forward_message(chat_id='administration.chat.id', from_chat_id=message.chat.id, message_id=message.message_id)
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['photo'])
def resend_photo(message):
    bot.forward_message(chat_id='administration.chat.id', from_chat_id=message.chat.id, message_id=message.message_id) 
    file_id = message.photo[-1].file_id
    filename = download_file(bot, file_id)
    if message.caption == 'blur':
        blur(filename)
        image = open(filename, 'rb')
        bot.send_photo(message.chat.id, image)
        image.close()
    elif message.caption == 'detail':
        detail(filename)
        image = open(filename, 'rb')
        bot.send_photo(message.chat.id, image)
        image.close()
    elif message.caption == 'emboss':
        emboss(filename)
        image = open(filename, 'rb')
        bot.send_photo(message.chat.id, image)
        image.close()
    elif message.caption == 'contour':
        contour(filename)
        image = open(filename, 'rb')
        bot.send_photo(message.chat.id, image)
        image.close()
    else:
        bot.send_message(message.chat.id, 'Вы не указали фильтр')

    if os.path.exists(filename):
        os.remove(filename)

bot.polling()