from typing import Mapping
from services import db
from config import REDIS_PREFIX


def exchange(from_currency: str, to_currency: str, amount: float) -> float:
    """Calculates the exchange value of the given amount from one currency to another."""
    if from_currency == 'RUB':
        from_rate_value = 1.0
        from_rate_nominal = 1
    else:
        from_rate_value = db.get(f"{REDIS_PREFIX}{from_currency}")['value']
        from_rate_nominal = db.get(f"{REDIS_PREFIX}{from_currency}")['nominal']
    
    if to_currency == 'RUB':
        to_rate_value = 1.0
        to_rate_nominal = 1
    else:
        to_rate_value = db.get(f"{REDIS_PREFIX}{to_currency}")['value']
        to_rate_nominal = db.get(f"{REDIS_PREFIX}{to_currency}")['nominal']

    result = round((amount * from_rate_value / from_rate_nominal) / (to_rate_value / to_rate_nominal), 3)

    return result


def rates() -> Mapping[str, str]:
    """Return current exchange rates for all available currencies."""
    all_rates = db.keys(f"{REDIS_PREFIX}*")
    rates_dict = {key.decode().split(":")[1]: db.get(key)['value'] for key in all_rates}

    return rates_dict
