import argparse
import os

from common.parse import parse_problem


def get_problem_name(problem):
    sp = problem.url.split('/')
    if 'problemset' in problem.url:
        contest = sp[-2]
    else:
        contest = sp[-3]
    index = sp[-1]
    problemname = problem.name.split(' ', 1)[1]
    return "CF_{}{}_{}".format(contest, index, problemname.replace(' ', '_'))


def main():
    parser = argparse.ArgumentParser(description="Download a CF problem for copsy")
    parser.add_argument('url', help='URL of Problem')
    parser.add_argument('--destination', '-d', default=os.getcwd(), help='Folder to create problem folder in')
    args = parser.parse_args()

    problem = parse_problem(args.url, use_cookie=False)
    destination = os.path.join(args.destination, get_problem_name(problem))
    os.makedirs(destination)
    with open(os.path.join(destination, 'samples.txt'), 'w') as f:
        f.write("\n===\n".join(map(str, problem.samples)) + "\n")
    with open(os.path.join(destination, 'desc.md'), 'w') as f:
        print("#", problem.name, file=f)
        print(file=f)
        print(problem.url, file=f)
        print(file=f)
        print(problem.description, file=f)
        print(file=f)
        print("## ", end='', file=f)
        print(problem.input, file=f)
        print(file=f)
        print("## ", end='', file=f)
        print(problem.output, file=f)
    with open(os.path.join(destination, 'problem.csy'), 'w') as f:
        print("data: (int, int)", file=f)
        print("init():", file=f)
        print("  pre: true", file=f)
        print("  post: () -> true", file=f)
        print("solve(int, int) -> int:", file=f)
        print("  pre: true", file=f)
        print("  post: ((a, b), result, old_data, new_data) -> new_data == old_data && result == a + b", file=f)


if __name__ == '__main__':
    main()
