import tomllib
import os


def load_config():
    with open("conf.toml", "rb") as file:
        data = tomllib.load(file)
        return data

def set_env():
    data = load_config()

    os.environ['public'] = data['binance']['public']
    os.environ['private'] = data['binance']['private']
