#!/usr/bin/env python
"""
opscomm cli client

Usage:
  opscomm [options] ACTION ITEM [<keyvalues>...]

  opscomm -h|--help
  opscomm --version

Options:
  -h --help                              Show this screen.
  --version                              Show version.
  -s SERVER --server=SERVER              Set Server [default: 192.168.224.76]
  -p PORT --port=PORT                    Set Port [default: 8000]
  -F --FULL                              Use Full detail listing
  -c COLUMN --columns=COLUMNS            Set Columns [default: 25]
  -L LEVEL --logging=level               Set Debug Level critical, error, warning, info, debug  [default: error]

Examples:
  opscomm devices n3b01

Help:
  Yeah we all need some help.

"""
from inspect import getmembers, isclass, ismodule
from docopt import docopt
import logging
import pkg_resources  # part of setuptools
version = pkg_resources.require("opscomm")[0].version

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    """Main opscomm entrypoint."""
    import datastores



    options = docopt(__doc__, version=version)
    for key in options.keys():
        #print key, options[key]
        options[key.strip('-')] = options[key]

    #Set logging level:
    if options['logging'] == "critical": logger.setLevel(logging.CRITICAL)
    elif options['logging'] == "error": logger.setLevel(logging.ERROR)
    elif options['logging'] == "warning": logger.setLevel(logging.WARNING)
    elif options['logging'] == "info:": logger.setLevel(logging.INFO)
    elif options['logging'] == "debug": logger.setLevel(logging.DEBUG)
    else: logger.setLevel(logging.INFO)

    logging.debug("options: ")
    logging.debug(options)
    #print (options['logging'])

    for name, data in getmembers(datastores, isclass):
      if name == '__builtins__': continue
      if name =='Base': continue

      for name2, data2 in getmembers(data):

          if name2 == options['ACTION']:
              #Ok so we have the function!
              instance=data(options)
              try:
                func = getattr(instance, options['ACTION'] )
              except AttributeError:
                print 'function not found "%s"  ' % (name2,)
              else:
                func()


if __name__ == "__main__":
    main()
