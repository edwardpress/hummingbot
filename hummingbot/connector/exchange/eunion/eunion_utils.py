import re
from typing import (
    Optional,
    Tuple)
from hummingbot.client.config.config_var import ConfigVar
from hummingbot.client.config.config_methods import using_exchange
from hummingbot.core.utils.tracking_nonce import get_tracking_nonce_low_res

RE_4_LETTERS_QUOTE = re.compile(r"^(\w+)(usdt|husd)$")
RE_3_LETTERS_QUOTE = re.compile(r"^(\w+)(btc|eth|trx)$")
RE_2_LETTERS_QUOTE = re.compile(r"^(\w+)(ht)$")

CENTRALIZED = True

EXAMPLE_PAIR = "ETH-USDT"

DEFAULT_FEES = [0.2, 0.2]


def split_trading_pair(trading_pair: str) -> Optional[Tuple[str, str]]:
    try:
        m = RE_4_LETTERS_QUOTE.match(trading_pair)
        if m is None:
            m = RE_3_LETTERS_QUOTE.match(trading_pair)
            if m is None:
                m = RE_2_LETTERS_QUOTE.match(trading_pair)
        return m.group(1), m.group(2)
    # Exceptions are now logged as warnings in trading pair fetcher
    except Exception:
        return None


def convert_from_exchange_trading_pair(exchange_trading_pair: str) -> Optional[str]:
    if split_trading_pair(exchange_trading_pair) is None:
        return None

    base_asset, quote_asset = split_trading_pair(exchange_trading_pair)
    return f"{base_asset.upper()}-{quote_asset.upper()}"


def convert_to_exchange_trading_pair(hb_trading_pair: str) -> str:
    return hb_trading_pair.replace("-", "").lower()


# get timestamp in milliseconds
def get_ms_timestamp() -> int:
    return get_tracking_nonce_low_res()


KEYS = {
    "eunion_api_key":
        ConfigVar(key="eunion_api_key",
                  prompt="Enter your Eunion API key >>> ",
                  required_if=using_exchange("eunion"),
                  is_secure=True,
                  is_connect_key=True),
    "eunion_secret_key":
        ConfigVar(key="eunion_secret_key",
                  prompt="Enter your Eunion secret key >>> ",
                  required_if=using_exchange("eunion"),
                  is_secure=True,
                  is_connect_key=True),
}
