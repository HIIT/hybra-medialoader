import sys
import os
import importlib
import pytest

path = os.path.abspath('..')
sys.path.append(path)

out = 'test_file.txt'
url_list = 'urls.txt'

def run_parser_tests():
    urls = open(url_list, 'r')

    i = 1
    for line in urls:
        domain,url = line.split(",")
        module = importlib.import_module('sites.' + domain)
        initialise_file(module, url.strip())
        print create_log(domain, url.strip(), i)
        pytest.main(['-q', '--domain=' + domain])
        i += 1
    urls.close()
    print_not_tested()

def initialise_file(module, url):
    if ( os.path.isfile(out) ):
        os.remove(out)
    module.parse(url, file(out, 'w'))

def create_log(domain, url, test_no):
    log_content = "\n**************"
    log_content += "\nTest run no. " + str(test_no)
    log_content += "\n**************\n"
    log_content += "\nParser: " + domain
    log_content += "\nURL: " + url
    log_content += "\nTest content file path: test_contents/" + domain + ".txt"
    log_content += "\nParser output file path: test_file.txt" + "\n"
    return log_content

def print_not_tested():
    not_tested = open('not_tested.txt', 'r')
    print "\nParsers that were not tested:"
    for parser in not_tested:
        print parser.strip()
    print "\n"

if __name__ == '__main__':
    run_parser_tests()
