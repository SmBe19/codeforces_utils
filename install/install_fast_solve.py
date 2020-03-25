#!/usr/bin/env python3

import os
import stat
import argparse
rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

orig_path = os.getcwd()
os.chdir(rootdir)
if not os.path.isdir('venv'):
    os.system('python3 -m venv venv')
    os.system('. venv/bin/activate; pip install -r requirements.txt')
os.chdir(orig_path)

blub = """
#!/bin/sh
ORIG=`pwd`
cd {rootdir}
. venv/bin/activate
cd src
python3 -m fast_solve.fast_solve "$@" --destination "$ORIG"
""".strip()

parser = argparse.ArgumentParser(description='Install fast_solve')
parser.add_argument('destination', nargs='?', default='~/.local/bin/cf', help='file to create')
args = parser.parse_args()

destfile = os.path.expanduser(args.destination)
with open(destfile, 'w') as f:
    f.write(blub.format(rootdir=rootdir))
st = os.stat(destfile)
os.chmod(destfile, st.st_mode | stat.S_IEXEC)
