#!/usr/bin/env python3
from bs4 import BeautifulSoup
from json import dumps, loads, load
from time import sleep
import requests, os
# This is all adapted from my youtube scraper.

existing = 'offenders.json'
urls_file = 'git_urls.txt'

def get_lines(url, curl2sudos, intermediate_output_file):
    for i in range(1,5):
        print("Grabbing page {}.".format(i))

        r = requests.get('{0}&p={1}'.format(url, i))
        soup = BeautifulSoup(r.text)
        possicurls = soup.select('.code-list-item')

        for bubble in possicurls:
            curl2sudo_score = 0
            bubble_lines = bubble.select('.line')
            title = bubble.select('.title a')[1].attrs

            for line in bubble_lines:
                low = line.text.lower()

                ###########################################
                # I F  I  W A N T E D  T O  U S E  R E G -
                # U L A R  E X P R E S S I O N S  I ' D
                # B E  D E A D  B Y  N O W  # T R U T H U G
                ###########################################
                if 'curl' not in low and 'wget' not in low:
                    continue
                else:
                    curl2sudo_score = curl2sudo_score + 1

                if ' sh' not in low and ' bash' not in low:
                    continue
                else:
                    curl2sudo_score = curl2sudo_score + 1

                if 'curl $1' in low or 'wget $1' in low:
                    # russian_roulette.jpg
                    curl2sudo_score = curl2sudo_score + 1

                if 'http://' in low:
                    # Http, thats worth a goober
                    curl2sudo_score = curl2sudo_score + 5

                if 'https://' in low:
                    # Yes, lets try to remain secure
                    curl2sudo_score = curl2sudo_score + 2

                if 'ftp://' in low:
                    # Where did you even FIND an ftp server?
                    curl2sudo_score = curl2sudo_score + 10

                if '< <(' in low:
                    # Gettin' fancy in here
                    curl2sudo_score = curl2sudo_score + 7

                if ' sudo' in low or 'sudo ' in low:
                    # I like to live dangerously, too
                    curl2sudo_score = curl2sudo_score + 15

                if ' su' in low or 'su ' in low:
                    # Installed debian recently, eh?
                    curl2sudo_score = curl2sudo_score + 5


                curl2sudos[low] = {
                    'href': 'https://github.com{}'.format(title['href']),
                    'score': curl2sudo_score,
                    'title': title['title'],
                    }

        intermediate_output_file.write(dumps(curl2sudos))
        print("Retrieved page {}. Sleeping.".format(i))
        sleep(5)

def main():
    loaded = open(existing, 'r')
    urls = open(urls_file, 'r')

    try:
        curl2sudos = load(loaded)
    except ValueError as e:
        curl2sudos = {}

    old_len = len(curl2sudos.keys())
    print("Loaded {} existing curl2sudos.".format(old_len))

    loaded.close()

    output_file = open(existing, 'w')
    intermediate_output_file = open('/tmp/intermediate_{}'.format(existing), 'w')

    for url in urls:
        get_lines(url.strip(), curl2sudos, intermediate_output_file)
        import ipdb; ipdb.set_trace()

    output_file.write(dumps(curl2sudos))

    intermediate_output_file.close()
    os.remove(intermediate_output_file)

    output_file.close()
    urls.close()
    diff = len(urls.keys()) - old_len
    print("Added {} new videos.".format(diff))

if __name__ == '__main__':
    main()
