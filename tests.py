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
        fName = 'testURLFile.txt'
        expected = ['http://baidu.com', 'https://qq.com', 'https://mysite.com', 'http://example.com', 'https://blabla.com']
        actual = parseURLFile(fName)
        fName2 = 'notExist.txt'
        self.assertEquals(actual, expected)
        self.assertEquals(parseURLFile(fName2), None)
        


if __name__ =='__main__':
    unittest.main()