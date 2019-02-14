import unittest
from get_data import get_id
import requests
import re

class TestMarkdownPy(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_get_id(self):
        '''
        Test example from https://research.google.com/youtube8m/video_id_conversion.html
        ** Also make sure that if you give wrong id that the script
        doesn't break. Add error checking to get_id!
        '''
        self.assertEqual(get_id('nXSc'), '0sf943sWZls')
        #self.assertFalse(...)
 
if __name__ == '__main__':
    unittest.main()