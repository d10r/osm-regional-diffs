#!/usr/bin/python

import argparse, urllib2, re

parser = argparse.ArgumentParser(\
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description='Print all way ids of latest \
planet.openstreetmap.org - replication diff file',
                epilog='''
''')

# TODO: figure out what happens when 000 changes. Currently (2014-06-09)
# state.txt does not show 000 in it.
replication_url = 'http://planet.openstreetmap.org/replication/'
minutely_url = replication_url + "minute/"
state_url = minutely_url + "state.txt"

parser.add_argument("--verbose", action="store_true", help="increase verbosity")
args = parser.parse_args()

# Verbose print function taken from: http://stackoverflow.com/a/5980173
if args.verbose:
    def verboseprint(*args):
            # Print each argument separately so caller doesn't need to
            # stuff everything to be printed into a single string
            for arg in args:
               print arg,
            print
else:   
    verboseprint = lambda *a: None      # do-nothing function

# download stats.txt and extract current sequence number
def getCurrentSequenceNumber():
    response = urllib2.urlopen(state_url)
    html = response.read()
    verboseprint("VERBOSE: Content of state.txt:\n", html)
    sequenceNumber = re.findall('.*sequenceNumber=\d*', html)[0]
    return re.split('=', sequenceNumber)[1]

def splitSequenceNumber(currentSequenceNumber):
    m = re.search('(...)(...)', currentSequenceNumber)
    if not m:
        raise Exception("Current Sequence Number can not be extracted! Please check state.txt file manually.")
    return m

if __name__ == '__main__':
    currentSequenceNumber = getCurrentSequenceNumber()
    print "Split sequence number: " + splitSequenceNumber(currentSequenceNumber).group(1) + ":" + splitSequenceNumber(currentSequenceNumber).group(2)

