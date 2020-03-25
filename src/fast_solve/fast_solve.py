#!/usr/bin/env python3

import argparse
import os
import subprocess
import threading

from common.parse import parse_problem


def get_dest_file(problem, destination):
    dest_dir = os.path.abspath(destination)
    os.makedirs(dest_dir, exist_ok=True)
    problem_code = problem.name[0].lower()
    num = 0
    while os.path.isfile(os.path.join(dest_dir, '{}{:03}.cpp'.format(problem_code, num))):
        num += 1
    return os.path.join(dest_dir, '{}{:03}.cpp'.format(problem_code, num))


class TextRewriter:

    def __init__(self, src):
        self.src = src
        self.line_iter = iter(src.splitlines(True))
        self.line = next(self.line_iter)
        self.dst = ""

    def next(self):
        self.dst += self.line
        self.line = next(self.line_iter, None)

    def skip(self, dest, go_next=True):
        while self.line.strip() != dest:
            self.next()
            if self.line is None:
                return
        if go_next:
            self.next()

    def add_text(self, text, prefix='// '):
        for line in text.splitlines(True):
            self.dst += prefix + line.strip() + '\n'


def init_slide(problem, dest_file):
    subprocess.run(['slide', dest_file, 'init'])
    with open(dest_file) as f:
        src = f.read()

    rewriter = TextRewriter(src)

    rewriter.skip('/*!slide config')
    rewriter.skip('*/')
    rewriter.dst += '\n'

    rewriter.add_text(problem.input)
    rewriter.dst += '\n\n'
    rewriter.add_text(problem.description)

    rewriter.skip('//!slide end_input')
    rewriter.add_text(problem.output)
    rewriter.skip('/*!slide testdata')
    rewriter.add_text('\n===\n'.join(map(str, problem.samples)), '')
    rewriter.skip(None)

    with open(dest_file, 'w') as f:
        f.write(rewriter.dst)


def _do_start_slide_watch(dest_file):
    subprocess.run(['slide', dest_file, 'watch'])


def start_slide_watch(dest_file):
    thread = threading.Thread(target=_do_start_slide_watch, args=(dest_file,))
    thread.start()


def submit_loop(problem, dest_file):
    try:
        while True:
            input()
            problem.submit(dest_file)
    except KeyboardInterrupt:
        pass


def main():
    parser = argparse.ArgumentParser(description="Help to solve a CF problem fast")
    parser.add_argument('url', help='URL of Problem')
    parser.add_argument('--destination', '-d', default=os.getcwd(), help='Folder to save files')
    parser.add_argument('--no-watch', '-w', action='store_true', help='Do not watch file')
    args = parser.parse_args()

    problem = parse_problem(args.url)
    dest_file = get_dest_file(problem, args.destination)
    init_slide(problem, dest_file)
    if not args.no_watch:
        start_slide_watch(dest_file)
    submit_loop(problem, dest_file)


if __name__ == '__main__':
    main()
