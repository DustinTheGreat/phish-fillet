import re 
import time
from progress.bar import FillingSquaresBar
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from ip2geotools.databases.noncommercial import DbIpCity
from sys import exit
from random import choice
from os import path as osPath
from .filletAsync import fil_async
from .filletClass import filletTarget


def argCheck(config):
    '''
    This function checks all of the arguments passed to the config object
    to ensure there are no conflicting arguments. Such as verbose and quiet.
    Obviously both of these arguments can not be set.
    If a particular condition matches, we perform an action such as exit.
    '''
    
    if config.verbose and config.quiet:
        print("[-] You cannot enable both verbose and quiet. Please double check your flags.\n")
        exit()
    

    if config.ddir:
        if not osPath.isdir(config.ddir):
            print("\n[-] The download output path does not exist.")
            exit()
        if not config.download:
            print("\n[-] You specified a download path, but no download")
    
        

def fil_createPattern(exclusions):

    ''' 
    This functions returns a RE pattern string based off of the list passed
    to the exclusions parameter. The user will have to pass a text file path.
    
    Example: 
    
    x = fil_createPattern('excluded_domains.txt')
   
    x will contain "(google.com)|(aol.com)|(yahoo.com)"
    '''

    p = '|'
    pattern = []

    with open(exclusions,'r') as f:
        for each in f:
            each = each.rstrip('\n')
            each = each.replace(each, '('+each+')')
            pattern.append(each)
            #TODO: Add debug logging functionality
        

        # Join each item with pipe and place in string var
        p = p.join(pattern)

    return(p)



def fil_newUrlList(urlFile, excludeString):

    ''' 
    This function will pass the incoming url file to the urlFile argument.
    The exclusions will be performed, and a new url list will be returned.
    
    Example:
    fil_newUrlList('urls.txt',fil_createPattern('excluded-domains.txt')) 
    '''
    
    # Contains string created by fil_createPattern function
    regex = re.compile(excludeString)

    # Used to delete the exclusions so appended objects don't build
    with open('urls-with-exclusions.txt','w') as clearme:
        pass

    with open(urlFile, 'r') as f:

        for l in f:

            x = regex.search(l)

            if x:
                print("\n[+] Omitting matched exclusion: {}".format(x.group()))

            else: 
            #TODO: Make new URL file a variable
                # If no match, write URL to new text file
                with open('urls-with-exclusions.txt','a') as new:

                    new.write(l.rstrip(''))
            
def printLine(i=60,char="="):
    '''
    Quick function used to create distinguishable lines
    '''
    print(char*i)



def fil_urlConstruct(target, config):
    
    ''' 
    This function will take the a single URL and break up each
    component and stick it into the filletTarget class object's attribute.
    Each URL will be broken down and stuck into a class object for easy access.
    '''
    urls = []
    
    try:
        target.domain = urlparse(target.url).hostname.strip('\n')
        target.protocol = urlparse(target.url).scheme.strip('\n')
        target.parentString = urlparse(target.url).path.strip('\n')
        domain = target.protocol+"://"+target.domain
    except Exception as e:
        print("[-] Potential error with url. Please check url file for errors: {}".format(e))
        print("[-] Current target information:\n")
        print(target.show())
        print("here")
        exit()


    
    # Split directories up for target.parentDirs
    dirs = target.parentString.split("/")
    dirs = dirs[1:]

    # Remove empty strings
    for i in dirs:
        if i == '':
            dirs.remove(i)

    count = str(len(dirs))
    dirs.reverse() # Required to start from parent dirs.
    urls.append(domain)

    # Remove file extension from url path
    for each in dirs:
        if "." in each:
            dirs.remove(each)

    if dirs:
        try:
            domain = domain+'/'+dirs.pop()
            urls.append(domain)
        except Exception as e:
            print("[-] Error appending[fil_UrlConstruct]: Issue has occured.")
            print(e)
            exit()

    target.parentDirs = urls


# Currently not in use
#def fil_noDir(nodirs, parentDirs):
#    
#    # TODO this needs to be thought out. Remove dirs from searching, or remove URLs that have the dir?
#    ''' 
#    This function is used to avoid searching directories specified by the user. 
#    fil_noDir will return a new list of directories to be searched after excluding
#    any identified matches.. 
#
#    All non-matches are added to a new list which can then be returned to the target's 
#    parentDirs attribute.
#    
#    Example: target.parentDirs = fil_noDir(args.nodirs, target.ParentDirs)
#    '''
#
#    newDirs = [] 
#
#    for each in parentDirs:
#        if each in nodirs:
#            i = parentDirs.index(each)
#            del(parentDirs[i:])
#
#    return(newDirs)



def fil_getGeoIP(target, config):

    ''' 
    This function will take the target.domain attribute and retrieve
    ip and country / region information which will be injected back into
    the class object. 
    '''
    from ip2geotools.databases.noncommercial import DbIpCity # IMPORT

    try:
        target.ip = gethostbyname(target.domain)
        response = DbIpCity.get(target.ip, api_key='free')
        target.country = response.country
        target.region = response.region
        target.city = response.city

    except(KeyboardInterrupt, SystemExit):
        exit()

    except:
        if not config.quiet: 
            print("[-] Can not reach domain.")
            target.clearLocation()

        target.clearLocation()    



def fil_randomAgent():
    
    ''' 
    This function will select a random agent and inject it into a header.
    The header is then returned. Consider running this inside the header.
    '''
    from random import choice # IMPORT

    agents =['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.158 Safari/537.36)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 YaBrowser/20.3.1.195 Yowser/2.5 Yptp/1.23 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97 (Edition Yx 03)',
            'Safari/13604.1.38.1.6 CFNetwork/887 Darwin/17.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 6.0.1; SM-G930V Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.117 Mobile Safari/537.36',]

    return {'User-Agent': choice(agents),'Accept':'text/html,*/*;'}   


def printTitle():
    '''Prints ascii title'''
    print("\
 __  _  _ _ ____ _  _    ____ _ _    _    ____ ___\n\
|__] |__| | [__  |__| __ |___ | |    |    |___  | \n\
|    |  | | ___] |  |    |    | |___ |___ |___  | \n\
--------------------------------------------------\n\
              ,/.(     __                         \n\
           ,-'    `!._/ /\n\
          > X )<|    _ <\n\
           `-....,,;' \_\n\
")


    
def fil_download(target, config):
        
    '''
    This is the function that downloads things. :)
    '''

    fPath = str(target.dfilename)

    if config.ddir:
        fPath = str(config.ddir)+'/'+str(target.dfilename)
    try:
        with open(fPath, 'wb') as f:
            r = requests.get(target.durl, stream=True)
            s = int(r.headers['content-length']) / 1000000
            if not config.quiet:
                print("[+] Downloading file: {} Size: {:.2f}MB".format(target.dfilename, s))
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print("[-] Downloading error occured: {}".format(e))
       


def fil_output(index, config):

    '''
    This function takes the index files returned from fil_connect and
    writes them out.
    Example:
    index = fil_connector(target, filConfig)
    fil_output(index, filConfig.output) 
    '''

    with open(config, 'a') as f:
        try:
            for i in index:
                f.write(i+"\n")
        except:
            pass



def fil_connector(config, content):
    '''
    This function is the main function of the program. It is responsible for executing various
    functions that are used to retrieve data. Some examples of this are downloading files, 
    retrieiving geoIP locations and other functions.
    '''
    urls = content
    indexFiles = []
    userAgent = {'User-Agent':'PhishFillet/v1.0'}
    printTitle()
    try:
        fil_async(urls, config)
    except:
        print("no")    
    return indexFiles

  