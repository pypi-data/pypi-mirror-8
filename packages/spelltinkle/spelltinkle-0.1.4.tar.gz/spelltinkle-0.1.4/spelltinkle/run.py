import os
import sys
import random
import logging
import argparse
import traceback
import subprocess

from .session import Session
from .screen import Screen
from .exceptions import StopSession


dir = os.path.expanduser('~/.spelltinkle')
if not os.path.isdir(dir):
    os.mkdir(dir)

logging.basicConfig(filename=os.path.join(
    dir, 'debug%d.txt' % random.randint(0, 10000)),
                    filemode='w', level=logging.DEBUG)


def run(args=None, input=None):
    parser = argparse.ArgumentParser()
    add = parser.add_argument
    add('files', nargs='*')
    add('-w', '--new-window', action='store_true')
    add('-S', '--self-test', action='store_true')
    add('-D', '--debug', action='store_true')
    args = parser.parse_args(args)

    if args.new_window:
        for option in ['-w', '--new-window']:
            if option in sys.argv:
                sys.argv.remove(option)
                break
        else:
            assert 0
        subprocess.call([os.environ['COLORTERM'], '-e'] +
                        [' '.join(sys.argv)])
        return
        
    if args.self_test:
        from .test.selftest import test
        return test(args.files)
    
    scr = Screen()

    try:
        session = Session(args.files, scr, input)
        session.run()
    except StopSession:
        scr.stop()
        for doc in session.docs:
            doc.color.stop()
        session.save()
    except:
        scr.stop()
        traceback.print_exc(file=open('spelltinkle.traceback', 'w'))
        for doc in session.docs:
            del doc.views[:]
            if doc.filename:
                doc.filename += '.crashed'
                doc.write()
        print(session.docs)
