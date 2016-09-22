# Tools for collecting media data

## Contributors
* Matti Nelimarkka, HIIT
* Eemeli Kjeldsen, TET student working in HIIT
* Juho Pääkkönen, research assistant at HIIT

## Testing

[Pytest](http://doc.pytest.org/en/latest/) is used for testing the parsers. To run the tests from command line, go to /test
and run "python run_tests.py".

Parsers are tested against test content files, which are located in /test/test_contents. The output of the latest parser
is saved in /test/parser_out.txt. Difference log files for parser output files and test content files are saved in
/test/difference_logs/. Difference logs are created using python [difflib](https://docs.python.org/2/library/difflib.html).

The tests run through a list of urls stored in /test/urls.txt, which correspond to the test content files. To test just some
particular parsers, edit urls.txt accordingly (command line options for testing single parsers to be provided).
