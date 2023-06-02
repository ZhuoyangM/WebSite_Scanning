'''Test for backupscan'''
import unittest
from backupscan import parseURL, parseURLFile

class testBackUpScan(unittest.TestCase):
    
    def test_parseURL(self):
        s1 = 'http://baidu.com'
        s2 = 'https://qq.com'
        s3 = '    https://mysite.com  '
        s4 = ' example.com'
        s5 = 'HtTps://blabla.com'
        
        self.assertEquals(parseURL(s1), 'http://baidu.com')
        self.assertEquals(parseURL(s2), 'https://qq.com')
        self.assertEquals(parseURL(s3), 'https://mysite.com')
        self.assertEquals(parseURL(s4), 'http://example.com')
        self.assertEquals(parseURL(s5), 'https://blabla.com')


    def test_parseURLFile(self):
        pass


