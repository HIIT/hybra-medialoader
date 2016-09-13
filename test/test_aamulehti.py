import sys
import unittest

sys.path.append("/Users/paakkoj6/Documents/python/mediacollection")

from sites import aamulehti

url = "http://www.aamulehti.fi/kotimaa/hulppea-yli-34-miljoonan-euron-huoneisto-tampereen-huipulla-on-nyt-varattu/"

class AamulehtiTest(unittest.TestCase):

    def setUp(self):
        
