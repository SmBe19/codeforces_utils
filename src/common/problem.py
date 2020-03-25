import requests
from bs4 import BeautifulSoup
import os

from common.consts import USER_AGENT

class Sample:

    def __init__(self, input, output):
        self.input = input
        self.output = output

    def __str__(self):
        return "{}\n---\n{}".format(self.input, self.output)


class Problem:

    def __init__(self, url, name, description, input, output, samples):
        self.url = url
        self.name = name
        self.description = description
        self.input = input
        self.output = output
        self.samples = samples

    def __str__(self):
        return "{}\n{}\n\n{}\n\n{}\n\n{}\n\n{}".format(
            self.url,
            self.name,
            self.description,
            self.input,
            self.output,
            '\n===\n'.join(map(str, self.samples))
        )

    def submit(self, file):
        cookies = {}
        cookie_file = os.environ.get('CF_COOKIE', '~/.codeforces_cookie')
        with open(os.path.expanduser(cookie_file)) as f:
            for line in f:
                split = line.split('=', 2)
                cookies[split[0].strip()] = split[1].strip()
        print("Submit", file)
        document = requests.get(self.url, cookies=cookies)
        soup = BeautifulSoup(document.text, 'html.parser')
        token = soup.find(attrs={'name': 'csrf_token'})['value'].strip()
        headers = {
            'origin': 'https://codeforces.com',
            'referer': self.url,
            'user-agent': USER_AGENT,
        }
        data = {
            'csrf_token': token,
            'ftaa': '',
            'bfaa': '',
            '_tta': 644,
            'action': 'submitSolutionFormSubmitted',
            'submittedProblemIndex': self.name[0].upper(),
            'source': '',
            'programTypeId': '54',  # GNU G++17 7.3.0
        }
        params = {
            'csrf_token': token,
        }
        with open(file, 'rb') as f:
            files = {
                'sourceFile': f
            }
            res = requests.post(self.url, headers=headers, params=params, data=data, files=files, cookies=cookies)
            if not res.ok:
                print('Submission failed:', res, res.url)
