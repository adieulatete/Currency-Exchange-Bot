import aiohttp
import json
import xml.etree.ElementTree as ET
from config import URL, REDIS_PREFIX
from services import db


async def fetch_exchange_rates() -> str:
    """Fetches the XML data of exchange rates from the Central Bank."""
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            return await response.text()


def parse_and_store_rates(xml_data) -> None:
    """Parses the XML data and stores the exchange rates in Redis."""
    root = ET.fromstring(xml_data)

    for valute in root.findall('Valute'):
        char_code = valute.find('CharCode').text
        nominal = float(valute.find('Nominal').text)
        value = float(valute.find('Value').text.replace(',', '.'))

        data = json.dumps({'nominal': nominal, 'value': value})

        db.set(f"{REDIS_PREFIX}{char_code}", data)


async def update_rates() -> None:
    """Fetches the latest exchange rates and stores them in Redis."""
    xml_data = await fetch_exchange_rates()
    parse_and_store_rates(xml_data)
