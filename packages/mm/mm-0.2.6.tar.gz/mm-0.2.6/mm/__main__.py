import sys

if __package__ == '':
    import os
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

import mm

if __name__ == '__main__':
    sys.exit(mm.main())