import os
import difflib

def initialise_file(out, content_dictionary):
    if ( os.path.isfile(out) ):
        os.remove(out)
    write_file( file(out, 'w'), content_dictionary )

def write_file( out, content ):
    file_content = content['url'] + "\n"
    file_content += content['http'] + "\n"

    for category in content['categories']:
        file_content += category + "\n"

    for datetime_object in content['datetime_list']:
        file_content += str( datetime_object ) + "\n"

    file_content += content['author'] + "\n"
    file_content += content['title'] + "\n"
    file_content += content['ingress'] + "\n"
    file_content += content['text'] + "\n"

    for img in content['images']:
        file_content += img + "\n"
    for caption in content['captions']:
        file_content += caption + "\n"

    out.write( file_content.strip() )

def write_difference_log(domain, out, test_content_path):
    diff_log = file('test/difference_logs/' + domain + '_diff.txt', 'w')

    test_content = open(test_content_path, 'r')
    content = open(out, 'r')

    test_content_text = test_content.read().replace(' ', ' \n')
    content_text = content.read().replace(' ', ' \n')

    test_content_lines = test_content_text.splitlines()
    content_lines = content_text.splitlines()

    d = difflib.Differ()
    diff = d.compare(test_content_lines, content_lines)
    diff_log.write( '\n'.join(diff) )

    test_content.close()
    content.close()
