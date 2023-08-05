import sys
import re


print '''
Wrapped C Types and Functions
==========================

.. warning::

    This is far from a comprehensive list, but we hope to improve it as we go.

'''

for path, fh in [(path, open(path)) for path in sys.argv[1:]] or [('<stdin>', sys.stdin)]:

    is_sphinx = False
    did_header = False

    for line in fh:

        line = line.lstrip()
        if re.match(r'^#\s+\.\.', line):
            is_sphinx = True

        if is_sphinx and not line.startswith('#'):
            print
            is_sphinx = False

        if is_sphinx:
            if not did_header:
                print path.replace('../include/', '')
                print '-' * len(path)
                print
                did_header = True

            sys.stdout.write(re.sub(r'^# ?', '', line))
