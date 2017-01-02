import os
import difflib
import filecmp
import datetime

def initialise_file(out, content_dictionary):
    if ( os.path.isfile(out) ):
        os.remove(out)
    write_file( file(out, 'w'), content_dictionary )

def write_file( out, content ):
    file_content = content['domain'] + "\n"
    file_content += content['url'] + "\n"
    file_content += str( content['http'] ) + "\n"

    for category in content['categories']:
        file_content += category.encode('utf-8') + "\n"

    for datetime_object in content['datetime_list']:
        file_content += str( datetime_object ) + "\n"

    file_content += content['author'].encode('utf-8') + "\n"
    file_content += content['title'].encode('utf-8') + "\n"
    file_content += content['ingress'].encode('utf-8') + "\n"
    file_content += content['text'].encode('utf-8') + "\n"

    for img in content['images']:
        file_content += img.encode('utf-8') + "\n"
    for caption in content['captions']:
        file_content += caption.encode('utf-8') + "\n"

    out.write( file_content.strip() )

def write_difference_log(domain, out, test_content_path):
    filename = 'test/difference_logs/' + domain + '_diff.txt'
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, "w") as diff_log:
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

def file_exists(out):
    assert os.path.isfile(out)

def file_not_empty(out):
    assert os.path.getsize(out) > 0

def file_contents_match(domain, out):
    test_content_path = 'test/test_contents/' + domain + '.txt'
    write_difference_log( domain, out, test_content_path )
    assert filecmp.cmp( test_content_path, out )

def dictionary_created(d):
    assert bool( d )

def dictionary_contains_right_keys(d):
    keys = ['domain', 'url', 'http', 'categories', 'datetime_list', 'author', 'title', 'ingress', 'text', 'images', 'captions']
    for key in keys:
        assert key in d

def dictionary_values_correct_type(d):
    assert type( d['domain'] ) is str
    assert type( d['url'] ) is str
    assert type( d['http'] ) is int

    assert type( d['categories'] ) is list
    for category in d['categories']:
        type( category ) is unicode

    assert type( d['datetime_list'] ) is list
    assert len( d['datetime_list'] ) > 0
    for datetime_object in d['datetime_list']:
        assert type( datetime_object ) is datetime.datetime or datetime.date

    assert type( d['author'] ) is unicode
    assert type( d['title'] ) is unicode
    assert type( d['ingress'] ) is unicode
    assert type( d['text'] ) is unicode

    assert type( d['images'] ) is list
    for img in d['images']:
        assert type( img ) is unicode

    assert type( d['captions'] ) is list
    for caption in d['captions']:
        assert type( caption ) is unicode
