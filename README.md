# Tools for collecting media data

## Contributors
* Matti Nelimarkka, HIIT
* Eemeli Kjeldsen, TET student working in HIIT
* Juho Pääkkönen, research assistant at HIIT

## Testing

[Pytest](http://doc.pytest.org/en/latest/) is used for testing the parsers. To run the tests from command line run pytest in
the home directory.

Parsers are tested against test content files, which are located in [/test/test_contents](https://github.com/HIIT/mediacollection/tree/master/test/test_contents).
The output of the latest parser is saved in /test/parser_out.txt.
Difference log files for parser output files and test content files are saved in /test/difference_logs/.
Difference logs are created using python [difflib](https://docs.python.org/2/library/difflib.html).
