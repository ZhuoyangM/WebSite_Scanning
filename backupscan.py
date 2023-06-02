import requests
from urllib.parse import urlparse
from argparse import ArgumentParser
from fake_headers import Headers
from hurry.filesize import size
from concurrent.futures import ThreadPoolExecutor


# Create a searchList
def createSearchList(url):
    backUpDic = []
    # Common backup file names
    backUpName = ['1', '127.0.0.1', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
                    '2020', '2021', '2022', '2023', 'admin', 'archive', 'asp', 'aspx', 'auth', 'back',
                    'backup', 'backups', 'bak', 'bbs', 'bin', 'clients', 'code', 'com', 'customers', 'dat', 'data',
                    'database', 'db', 'dump', 'engine', 'error_log', 'faisunzip', 'files', 'forum', 'home', 'html',
                    'index', 'joomla', 'js', 'jsp', 'local', 'localhost', 'master', 'media', 'members', 'my', 'mysql',
                    'new', 'old', 'orders', 'php', 'sales', 'site', 'sql', 'store', 'tar', 'test', 'user', 'users',
                    'vb', 'web', 'website', 'wordpress', 'wp', 'www', 'wwwroot', 'root', 'log']
    
    resTuple = urlparse(url)
    host = resTuple.hostname
    
    domainList = [host, host.replace('.', ''), host.replace('.', '_')]
    if 'www' in host:
        domainList.append(host.replace('www.',''))
        domainList.append(host.split('.')[1])
        domainList.append(host.split('.',1)[1].replace('.', ''))
    else:
        domainList.append(host.split('.')[0])
    
    backUpName.extend(domainList)
    # Common backup file suffix
    backUpSuffix = ['.zip', '.rar', '.tar.gz', 
                    '.tgz', '.tar.bz2', '.tar', 
                    '.jar', '.war', '.7z', 
                    '.bak', '.sql', '.gz', 
                    '.sql.gz', '.tar.tgz', '.backup']
    
    # Compose backup file dictionary
    for name in backUpName:
        for suffix in backUpSuffix:
            backUpDic.append(name+suffix)
    
    # Create a search list
    searchList = []
    for fName in backUpDic:
        searchList.append(url+'/'+fName) 
    return searchList


# Parse a single input url
def parseURL(url):
    res = ''
    tmp = url.strip().lower()
    if tmp.startswith('http://') or tmp.startswith('https://'):
        res = tmp
    else:
        res = 'http://' + tmp
    
    return res

# Parse a url file
def parseURLFile(fName):
    urlList = []
    try:
        f = open(fName, 'r')
        lines = f.readlines()
        for line in lines:
            url = parseURL(line)
            urlList.append(url)
        f.close()
        return urlList
    except FileNotFoundError:
        print('The file {} does not exist.'.format(fName))
    

# Search for backup files for a given website
def searchBackUp(url):
    r = requests.get(url=url, headers=Headers.generate(), 
                     allow_redirects=False, stream=True, verify=False)
    if r.status_code == 200:
        sizeInBytes = int(r.headers.get('Content-Length'))
        fileSize = str(size(sizeInBytes))
        if int(fileSize[0:-1]) > 0: # Potential backup file found
            with open(res_file, 'a') as f:
                f.write(str(url) + '  ' + 'size:' + str(fileSize) + '\n')
            print('[SUCCESS] {}'.format(url))
        else: # Empty file can't be a backup file
            print('[EMPTY] {}'.format(url))

    else:
        print('[NOT FOUND] {}'.format(url))


# Scan the website using multithreads
def scan(url):
    p = ThreadPoolExecutor(max_workers=20)
    for target in searchList:
        p.submit(searchBackUp, target)
    p.shutdown()


if __name__ == 'main':
    usageEx = 'python3 backupscan.py -u https://www.example.com -o result.txt'
    parser = ArgumentParser(add_help=True, usage=usageEx, description='A website backup file leak scan tool.')
    parser.add_argument('-o', dest='res_file', type=str, help='An output file to store the searching result',required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', dest='url', action='store_true', type=str, help='A single website to be searched')
    group.add_argument('-f', dest='url_file', action='store_true', type=str, help='A file of websites to be searched')
    args = parser.parse_args()
    
    global res_file
    res_file = args.res_file

    try:
        if args.url:
            url = parseURL(args.url)
            searchList = createSearchList(url)
            scan(url)
        elif args.url_file:
            url_file = args.url_file
            urlList = parseURLFile(url_file)
            for url in urlList:
                searchList = createSearchList(url)
                scan(url)
    except Exception as e:
        print(e)




