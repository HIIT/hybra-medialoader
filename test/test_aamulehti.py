import sys
import os

path = os.path.abspath('..')
sys.path.append(path)

from sites import aamulehti

url = "http://www.aamulehti.fi/kotimaa/vanhemmat-uhmaavat-tamperelaisen-koulun-ohjetta-odotetaan-sita-paivaa-etta-joku-jaa-auton-alle/"

def test_file_exists():
    aamulehti.parse(url,file('test.txt', 'w'))
    assert os.path.isfile("test.txt") == True

def test_contents_match():
    
