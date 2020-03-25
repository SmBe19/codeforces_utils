import requests
from bs4 import BeautifulSoup
from common.problem import Sample, Problem

from common.consts import USER_AGENT

replacements = {
    '$$$': '`',
    '\\ldots': '...',
    '\\neq': '!=',
    '\\leq': '<=',
    '\\geq': '>=',
}


def _make_nice(element):
    def process_all(join=''):
        return join.join(_make_nice(x) for x in element.contents)

    if element.name in ['div', 'p', 'center', 'pre']:
        return process_all() + '\n'
    elif element.name == 'span' or element.name == 'i' or element.name=='b':
        return '*{}*'.format(process_all())
    elif element.name == 'ul':
        return process_all('\n')
    elif element.name == 'li':
        return '- ' + process_all()
    elif element.name == 'img':
        return '![{}]'.format(element['src'])
    elif element.name == 'br':
        return '\n'
    else:
        val = str(element)
        for key, value in replacements.items():
            val = val.replace(key, value)
        return val


def make_nice(element):
    return _make_nice(element).strip()


def parse_samples(element):
    samples = []
    for inp, out in zip(element.find_all(class_='input'), element.find_all(class_='output')):
        samples.append(Sample(
            make_nice(inp.pre).strip(),
            make_nice(out.pre).strip(),
        ))
    return samples


def parse_problem(url, debug=False):
    if debug:
        with open('test/problem.html') as f:
            document_text = f.read()
    else:
        headers = {
            'origin': 'https://codeforces.com',
            'user-agent': USER_AGENT,
        }
        document = requests.get(url, headers=headers)
        if not document.ok:
            print('Could not download document from', url)
            exit(1)
        document_text = document.text
    soup = BeautifulSoup(document_text, 'html.parser')

    name = soup.find(class_='title').string.strip()
    description_raw = soup.find(class_='header').next_sibling
    input_raw = soup.find(class_='input-specification')
    output_raw = soup.find(class_='output-specification')
    samples_raw = soup.find(class_='sample-test')

    return Problem(
        url,
        name,
        make_nice(description_raw),
        make_nice(input_raw),
        make_nice(output_raw),
        parse_samples(samples_raw),
    )


def get_contest_problems(url, debug=False):
    if debug:
        with open('test/contest.html') as f:
            document_text = f.read()
    else:
        headers = {
            'origin': 'https://codeforces.com',
            'user-agent': USER_AGENT,
        }
        document = requests.get(url, headers=headers)
        if not document.ok:
            print('Could not download document from', url)
            exit(1)
        document_text = document.text
    soup = BeautifulSoup(document_text, 'html.parser')
    problems = soup.find(class_='problems')
    return [
        'https://codeforces.com{}'.format(element.a['href']) for element in problems.find_all(class_='id')
    ]
