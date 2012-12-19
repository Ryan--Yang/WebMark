import logging
import os
import sys
from webmark_runner import WebMarkRunner

def usage():
    print "usage: webmark.py [config]"

if __name__== "__main__":
    conf_file = 'config.json'
    if len(sys.argv) > 1:
        conf_file = sys.argv[1]
    if not os.path.isfile(conf_file):
        print conf_file, "is not a file."
        usage()
        sys.exit(1)

    #logging.basicConfig(level=logging.DEBUG)
    WebMarkRunner(conf_file).run()
