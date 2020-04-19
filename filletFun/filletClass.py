#!/usr/bin/python3 

class filletTarget():
    '''
    For each line in a url text file, the url is passed to the filletTarget object. 
    The url is analyzed, parsed, and sent to the class object's specified attributes.

    This is done through various functions throughout the program, such as fil_urlConstruct
    and fil_getGeoIp
    
    Then the url has all information loaded into the target object which can be passed to 
    other functions or modules if needed.
    '''
    
    def __init__(self, parentDirs=[], parentString='', domain='',
    region='', country='', hosting='', ip='', url='', geoipEnabled=False, 
    city='',protocol='', dfilename='', durl='', found= '', downloads=''):

        self.parentDirs = parentDirs
        self.parentString = parentString
        self.domain = domain
        self.country = country
        self.region = region
        self.city = city
        self.hosting = hosting
        self.ip = ip
        self.url = url
        self.protocol = protocol
        self.dfilename = dfilename
        self.durl = durl
        self.found = []
        self.downloads = []



    def show(self):
        '''Print target will print out attribute values to console'''

        print("\n")
        print("="*25)
        print(" \
Url: {}\n \
Protocol: {}\n \
Domain: {}\n \
Parent String: {}\n \
Parent Directories: {}\n \
Country: {}\n \
Region: {}\n \
City: {}\n \
Hosting: {}\n \
IP: {}\n \
Found: {}\n \
Downloads: {}".format(self.url, self.protocol, self.domain, self.parentString, 
        self.parentDirs, self.country, self.region, self.city, self.hosting, self.ip, self.found, self.downloads))
        print("="*25+"\n")



    def clearLocation(self):

        self.country = ''
        self.region = ''
        self.city = ''



class filletConfig:

    '''
    This class is used to create the main config object for the program. Once
    arguments have been passed, they are saved in the config object.

    This is useful when a function needs to see what values have been passed
    by the user. 
    '''

    def __init__(self,geoIpEnabled=False,randomUserAgent=False, download=[],
            exclusions='',timeout=3,verbose=False, numOfUrls=0,logBuffer=[],
            quiet=False, output='', recursive=False, ddir=''):
        
        self.geoIpEnabled = geoIpEnabled
        self.randomUserAgent = randomUserAgent
        self.download = download
        self.exclusions = exclusions
        self.timeout = timeout
        self.verbose = verbose
        self.numOfUrls = numOfUrls
        self.logBuffer = logBuffer #TODO this might be deadcode
        self.quiet = quiet
        self.output = output
        self.recursive = recursive
        self.ddir = ddir

                
    def show(self):

        print("\n")
        print("="*25)
        print(" \
Number of Urls: {}\n \
Geo IP Lookup: {}\n \
Random User-Agent: {}\n \
Downloading: {}\n \
Download Directory: {}\n \
Exclusion File: {}\n \
Request Timeout: {}\n \
Verbose: {}\n \
Quiet: {}".format(self.numOfUrls,self.geoIpEnabled,self.randomUserAgent,
                self.download,self.ddir, self.exclusions,self.timeout,
                self.verbose,self.quiet))
        print("="*25+"\n")


# Dead code, not in use.

#    def checkBuffer(self, lines):
#
#        """ 
#        This method allows you to check the logBuffer against the amount of 
#        entered lines. If the logBuffer surpasses the max lines. Clear buffer.
#        """
#
#        if len(self.logBuffer) >= lines:
#            self.logBuffer = []
