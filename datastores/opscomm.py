#This provides some basic features:
import common

#from common import getPage, putPage

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
        
class opscomm():
    """Do Some stuff with opscomm"""
    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.col = col = int(options['columns'])
        
    def info(self):
        print "Enter opscomm info"

        #print 'You supplied the following options:', dumps(self.options, indent=2, sort_keys=True)
        url = "http://%s:%s/opscomm/?info=%s" % (self.options['server'],self.options['port'],self.options['ITEM'])

        #print ("Fetching: %s" %url)

        logging.debug(url)
        try:
            r = getPage(url)
        except:
            logging.error("Unable to retrieve data from: %s" %(url))
            return

        DATA=json.loads(r.text)