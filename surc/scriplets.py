import re
import urllib.request

import requests


class BaseScriptlet:
    @property
    def name(self):
        raise NotImplementedError("Must be implemented for each scriplet")

    @property
    def source(self):
        raise NotImplementedError("Must be implemented for each scriplet")

    def get_latest(self):
        raise NotImplementedError("Must be implemented for each scriplet")


class AndroidStudioStable(BaseScriptlet):
    def __init__(self) -> None:
        super().__init__()
        self._url = 'https://developer.android.com/studio/index.html'

    @property
    def name(self):
        return 'android-studio-stable'

    @property
    def source(self):
        return 'https://github.com/snapcrafters/android-studio.git'

    def get_latest(self):
        with urllib.request.urlopen(self._url) as response:
            html = response.read().decode()

        matched = re.findall('"((https)?://.*linux.zip)"', html)
        # Ensure unique and then convert to a list for easy access.
        links = list(set(matched))

        if len(links) == 0:
            raise ValueError('Url matching our query not found.')
        elif len(links) > 1:
            raise ValueError('Multiple urls found, expected only one, urls are: {}'.format(' '.join(links)))

        url = links[0][0]
        version = url.split('/')[-2]
        return version


class SublimeTextStable(BaseScriptlet):
    def __init__(self) -> None:
        super().__init__()
        self._url = 'https://download.sublimetext.com/latest/stable'

    @property
    def name(self):
        return 'sublime-text-stable'

    @property
    def source(self):
        return 'https://github.com/snapcrafters/sublime-text.git'

    def get_latest(self):
        response = requests.get(self._url)
        if response.status_code == 200:
            return response.text.strip()

        raise ValueError("Unable to fetch data from server or something...")
