import sys
import os
import importlib
import pytest

path = os.path.abspath( '..' )
sys.path.append(path)

out = 'parser_out.txt'
url_list = 'urls.txt'
#url_list = 'single_url.txt'

def run_parser_tests():
    urls = open( url_list, 'r' )

    i = 1
    for line in urls:
        domain,url = line.split( "," )
        module = importlib.import_module( 'sites.' + domain ) # Would be good to move
        content_dictionary = module.parse( url.strip() )      # these lines to a test setup method.
        initialise_file( module, content_dictionary )         # First, however find out how to parameterize setup methods
        print create_log( domain, url.strip(), i )
        pytest.main( ['-q', '--domain=' + domain, '--url=' + url.strip()] )
        i += 1

    urls.close()

def initialise_file(module, content_dictionary):
    if ( os.path.isfile(out) ):
        os.remove(out)
    write_file( file(out, 'w'), content_dictionary )

def write_file( out, content ):
    file_content = content['url'] + "\n"
    file_content += content['http'] + "\n"
    file_content += content['category'] + "\n"

    for date in content['date']:
        file_content += date + "\n"
    for time in content['time']:
        file_content += time + "\n"

    file_content += content['author'] + "\n"
    file_content += content['title'] + "\n"
    file_content += content['ingress'] + "\n"
    file_content += content['text'] + "\n"

    for img in content['images']:
        file_content += img + "\n"
    for caption in content['captions']:
        file_content += caption + "\n"

    out.write( file_content.strip() )


def create_log(domain, url, test_no):
    log_content = "\n**************"
    log_content += "\nTest run no. " + str(test_no)
    log_content += "\n**************\n"
    log_content += "\nParser: " + domain
    log_content += "\nURL: " + url
    log_content += "\nTest content file path: test_contents/" + domain + ".txt"
    log_content += "\nParser output file path: parser_out.txt"
    log_content += "\nDifference log file path: difference_logs/" + domain + "_diff.txt" + "\n"
    return log_content

def print_not_tested():
    not_tested = open(  'not_tested.txt', 'r')
    print "\nParsers that were not tested:"
    for parser in not_tested:
        print parser.strip()
    print "\n"

if __name__ == '__main__':
    run_parser_tests()
