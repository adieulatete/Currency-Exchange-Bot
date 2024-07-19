from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging
import aiocron
import asyncio
from jinja2 import Environment, FileSystemLoader
from services.rates_updater import update_rates
from config import *
from services import exchanger


# Configure logging
logging.basicConfig(level=logging.INFO, filename="./logging.txt", filemode="w", format="%(name)s %(asctime)s %(levelname)s %(message)s")

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))


@dp.message(Command('exchange'))
async def exchange(message: types.Message):
    """
    Handles the /exchange command. Calculates the exchange value of the given amount from one currency to another.

    Example command: /exchange USD RUB 10
    """
    try:
        _, from_currency, to_currency, amount = message.text.split()

        result = exchanger.exchange(from_currency, to_currency, float(amount))

        template = env.get_template('exchange_result.txt')
        response = template.render(
            amount=amount,
            from_currency=from_currency,
            to_currency=to_currency,
            result=result
        )
        await message.reply(response)

    except Exception as e:
        await message.reply("Error in the command. Use format: /exchange USD RUB 10")


@dp.message(Command('rates'))
async def rates(message: types.Message):
    """Handles the /rates command. Sends the current exchange rates for all available currencies."""

    rates_dict = exchanger.rates()

    template = env.get_template('rates.txt')
    response = template.render(rates=rates_dict)
    await message.reply(response)


@aiocron.crontab('0 0 * * *')
async def scheduled_update():
    """Scheduled task to update exchange rates daily at midnight."""
    await update_rates()


async def main() -> None:
    # Run events dispatching
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(update_rates())
    asyncio.run(main())
