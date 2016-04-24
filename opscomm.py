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
  -s SERVER --server=SERVER              Set Server Address
  -p PORT --port=PORT                    Set Port [default: 8080]
  -F --FULL                              Use Full detail listing
  -c COLUMN --columns=COLUMNS            Set Columns [default: 25]
  -L LEVEL --logging=level               Set Debug Level critical, error, warning, info, debug  [default: error]

Examples:
  opscomm search n3b01

Help:
  Yeah we all need some help.

"""

#[default: opscomm-server-core-mluich.c9users.io]
import os
from inspect import getmembers, isclass, ismodule
from docopt import docopt
import logging
import pkg_resources  # part of setuptools
import ConfigParser



#version = pkg_resources.require("opscomm")[0].version
version = "0.0.20160228"
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    """Main opscomm entrypoint."""
    import datastores
    options={}
    # set an initial logging level
    logger.setLevel(logging.DEBUG)
    
    
    #Since command line options overide config file options 
    #Grab the config files first!
    Config = ConfigParser.ConfigParser()
    try:
     Config.readfp(open('/etc/opscomm/opscomm-cli.conf'))
    except:
      logging.warning("/etc/opscomm/opscomm-cli.conf NOT FOUND")
      
    Config.read(['site.cfg', os.path.expanduser('~/.opscomm/opscomm-cli.conf')])
    
    
    for section_name in Config.sections():
      if section_name != 'server': continue
      logging.debug('Section: %s' % section_name)
      logging.debug('  Options: %s'% Config.options(section_name))
      for name, value in Config.items(section_name):
        logging.debug( '  %s = %s' % (name, value))
        options[name]=value

    logging.debug("Getting docopt")
    #And Commandline options overwrite
    docOptions = docopt(__doc__, version=version)
    for key in docOptions.keys():
        #print key, options[key]
        cleanKey=key.strip('-')
        if cleanKey in options: continue
        options[cleanKey] = docOptions[key]

    logging.debug("Set Logging level")
    #Set logging level:
    if 'logging' in options:
      logging.debug("options exists: %s" % options['logging'])
      
    if options['logging'] == "critical": logger.setLevel(logging.CRITICAL)
    elif options['logging'] == "error": logger.setLevel(logging.ERROR)
    elif options['logging'] == "warning": logger.setLevel(logging.WARNING)
    elif options['logging'] == "info:": logger.setLevel(logging.INFO)
    elif options['logging'] == "debug": logger.setLevel(logging.DEBUG)
    else: logger.setLevel(logging.INFO)

    logging.debug("options: ")
    logging.debug(options)
    logging.debug(options['logging'])

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
