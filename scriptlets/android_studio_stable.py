import re
import urllib.request


def main():
    with urllib.request.urlopen('https://developer.android.com/studio/index.html') as response:
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
