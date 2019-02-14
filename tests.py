import unittest
from get_data import get_id, save_image
import requests
import re
import os
import imghdr

class TestMarkdownPy(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_get_id(self):
        '''
        Test example from https://research.google.com/youtube8m/video_id_conversion.html
        '''
        self.assertEqual(get_id('nXSc'), '0sf943sWZls')

            
    def test_save_image(self):
        filename_path = save_image('.', '0sf943sWZls')
        ext = imghdr.what(filename_path)
        assert ext in ['jpg', 'jpeg', 'tiff', 'png']
        
 
if __name__ == '__main__':
    unittest.main()
    os.remove('0sf943sWZls.jpg')
    