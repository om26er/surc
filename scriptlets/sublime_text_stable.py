import requests


def main():
    response = requests.get('https://download.sublimetext.com/latest/stable')
    if response.status_code == 200:
        return response.text.strip()
    raise ValueError("Unable to fetch data from server or something...")
