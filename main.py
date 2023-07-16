from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from PIL import Image, ImageFilter, ImageDraw, ImageFont


bot = Bot(token="TOKEN")
namebot = '@NAME BOT'

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer('Привет! Это бот для создания цитат')


@dp.message_handler(content_types=['text'])
async def message(message):
    if len(message.text) > 94:
        await message.answer('Слишком большой объем текста...')
    elif message.text.count('\n') > 4:
        await message.answer('Слишком много строк текста\nДопустимо не больше 4-х.')
    else:
        profile_pictures = await bot.get_user_profile_photos(message.from_user.id)
        photo_path = "avatar.jpg"
        await profile_pictures.photos[0][-1].download(destination=photo_path)
        img = Image.open('index.jpg')
        img_avatar = Image.open('avatar.jpg')
        img_avatar_finaly = img_avatar.resize((140, 140))
        idraw = ImageDraw.Draw(img)
        headline_zagolovok = ImageFont.truetype('arial.ttf', size=50)
        headline_text = ImageFont.truetype('arial.ttf', size=40)
        idraw.text((100, 20), f'Цитаты великих людей', font=headline_zagolovok)
        if len(message.text) > 47 and message.text.count('\n') == 0:
            idraw.text((20, 160), f'«{message.text[:47]}', font=headline_text)
            idraw.text((20, 210), f'{message.text[47:]}».', font=headline_text)
        else:
            idraw.text((20, 160), f' «{message.text}».', font=headline_text)
        mask_im = Image.new("L", img_avatar_finaly.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((0, 0, 130, 130), fill=255)
        img.paste(img_avatar_finaly, (20, 300), mask_im)
        idraw.text((170, 345), f'© {message.from_user.full_name}', font=headline_text)
        img.save('result.png')
        await message.answer('Готово!')
        await bot.send_photo(message.chat.id, types.InputFile('result.png'))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
