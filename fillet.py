#!/usr/bin/python3

from sys import exit
import os
from filletFun.filletClass import *
from filletFun.filletFun1 import fil_connector

import time
import argparse

# All arg parameters are passed to class object, to be used by fil_connector()
parser = argparse.ArgumentParser(description="Parse a list of URLs for Index directories")
parser.add_argument('-f', '--file', help="Pass a file containing URLs")
parser.add_argument('-t', '--timeout', help="Url request timeout interval: default is 3 seconds. Lowering the may speed up search at the possible cost of accuracy.")
parser.add_argument('-E', '--exclusions', help="Pass a text file containing domains to exclude. Must be delimited by newline.")
parser.add_argument('-g','--geoip', action='store_true', help="Retrieve IP and geo-location details on domains.")
parser.add_argument('-u','--randomagent', action='store_true', help="Use a random user-agent with each url request. Default UA is phish-fillet.")
#parser.add_argument('-n', '--nodir', nargs='+', help="Pass directories you want to avoid searching") # deadcode - testing
parser.add_argument('-d', '--download', nargs='+', help="Specify extention types you wish to download.")
parser.add_argument('-dd', '--ddir', help="Select a download directory any downloads will be saved.")
parser.add_argument('-v', '--verbose', action='store_true', help="Print out additional information to the console.")
parser.add_argument('-q', '--quiet', action='store_true', help="Minimal screen with progress bar. No output.")
parser.add_argument("-o", "--output", type=str, help="Save output to a file delimited by newlines")
parser.add_argument("-r", "--recursive", action='store_true', help="If a index folder is found check it. Output is marked with a [r]")
args = parser.parse_args()

filConfig = filletConfig()

if not args.file:
    print("[!] Error: You must specify a text file containg a url list.")
    exit(0)
if args.exclusions:
    filConfig.exclusions = args.exclusions
    fil_newUrlList(args.file,fil_createPattern(filConfig.exclusions))
if args.randomagent:
    filConfig.randomUserAgent = True
if args.geoip:
    filConfig.geoIpEnabled = True
if args.download:
    filConfig.download = args.download
if args.timeout:
    filConfig.timeout = args.timeout
if args.verbose:
    filConfig.verbose = True
if args.quiet:
    filConfig.quiet = True
    from progress.bar import FillingSquaresBar # IMPORT
if args.output:
    filConfig.output = args.output
if args.recursive:
    filConfig.recursive = args.recursive
if args.ddir:
    filConfig.ddir = args.ddir 

# Ensure there are no conflicting arguments

def main():
    textfile = args.file

    if filConfig.exclusions:
        textfile = 'urls-with-exclusions.txt'
    if filConfig.download:
        target.download = filConfig.download

    # Retrieve number of url lines
    content = []
    with open(textfile, 'r') as f:
        content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
        # Return lines to config object
        filConfig.numOfUrls = len(content)

    # Open textfile again to actually run.


    if filConfig.quiet:
        print("\n[ Searching {} urls ]".format(filConfig.numOfUrls))
        bar = FillingSquaresBar('Filleting Phish', max = filConfig.numOfUrls)
        print("\n")
    
    if filConfig.verbose:
        filConfig.show()

    for line in content:
        

        try:
            if filConfig.quiet:
                bar.next()
            # Pass URL to target class object
                
            # Class object passed to urlConstruct to create attributes 

            # Launch GeoIP Function
            if filConfig.geoIpEnabled:
                fil_getGeoIP(target, filConfig) # Can this be placed inside connector?
            
            # If output selected collect return and place in output function
            if filConfig.output:
                index = fil_connector(target, filConfig)
                fil_output(index, filConfig.output)
            else:
                fil_connector(filConfig, content)
                exit()
            
        except (KeyboardInterrupt, SystemExit):

                print("\n\n\
Goodbye!       ,-,\n\
             ,/.(     __\n\
          ,-'    `!._/ /\n\
         > X )<|    _ <\n\
          `-....,,;' \_\n")
                exit()



if __name__ == '__main__':
    main()
