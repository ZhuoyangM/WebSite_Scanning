from backupscan import createSearchList, searchBackUp
from fake_headers import Headers
import requests

url = 'https://www.geeksforgeeks.org/geeksforgeeks.zip'
url2 = 'https://www.w3schools.com/1.bak'
url3 = 'https://www.geeksforgeeks.org'

target = 'https://www.baidu.com/baidu.zip'

header = Headers(headers=False)
r = requests.get(url=url3, headers=header.generate(), 
                     allow_redirects=False, stream=True, verify=False)

print(r.headers.get('Content-Length'))

#searchBackUp(url3, res_file='result.txt')
