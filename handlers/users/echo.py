from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from loader import dp
from scripts import get_avg_price


class Form(StatesGroup):
    car = State()


@dp.message_handler(state=Form.car)
async def converter(message: types.Message, state: FSMContext):
    car = message.text.split()

    if len(car) != 3:
        await message.reply('Некорректный ввод')
        await state.finish()
        return

    avg_price = get_avg_price(*car)

    if avg_price is None:
        await message.reply('Не удалось найти. Попробуйте ввести другой год, марку или модель')
        await state.finish()
    else:
        await message.reply(f'Средняя цена: {avg_price} KZT')
        await state.finish()


@dp.message_handler(commands=['find'])
async def find_avg_price(message: types.Message):
    await Form.car.set()
    await message.reply('Введите марку модель и год производства, Пример: "toyota corolla 2005"', reply=False)
