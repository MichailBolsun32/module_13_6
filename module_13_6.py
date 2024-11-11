from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

#   Необходимо дополнить код предыдущей задачи,
#   чтобы при нажатии на кнопку 'Рассчитать' присылалась Inline-клавиатруа.

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb_r = ReplyKeyboardMarkup(resize_keyboard=True)# создание клавиатуры reblay
button1 = KeyboardButton(text='Расчитать')
button2 = KeyboardButton(text='Информация')
kb_r.insert(button1)
kb_r.insert(button2)

#   Создайте клавиатуру InlineKeyboardMarkup с 2 кнопками InlineKeyboardButton:
#    С текстом 'Рассчитать норму калорий' и callback_data='calories'
#    С текстом 'Формулы расчёта' и callback_data='formulas'

kb_i = InlineKeyboardMarkup() # создание клавиатуры inline
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_i.add(button3)
kb_i.add(button4)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands='start')
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb_r)

#Создайте новую функцию main_menu(message), которая:
    # Будет обёрнута в декоратор message_handler, срабатывающий при передаче текста 'Рассчитать'.
    # Сама функция будет присылать ранее созданное Inline меню и текст 'Выберите опцию:'

@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_i)

#Создайте новую функцию get_formulas(call), которая:
 # Будет обёрнута в декоратор callback_query_handler, который будет реагировать на текст 'formulas'.
 # Будет присылать сообщение с формулой Миффлина-Сан Жеора.

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('BMR=10×масса тела (кг)+6,25×рост (см)−5×возраст (годы)+5')

#Измените функцию set_age и декоратор для неё:
#Декоратор смените на callback_query_handler, который будет реагировать на текст 'calories'.
#Теперь функция принимает не message, а call. Доступ к сообщению будет следующим - call.message.

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(text = 'Информация')
async def info_message(message):
    await message.answer('Я бот, помогающий твоему здоровью!')


@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f"Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f"Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    bmr = int(data['weight']) * 10 + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f"Ваша норма калорий: {bmr}")
    await state.finish()

@dp.message_handler()
async def start_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)