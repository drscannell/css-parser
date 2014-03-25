import os
import tempfile
from css_parser.stylesheet_reader import StyleSheetReader

class TestCases:

	def test_read_string(self):
		expected = 'body {' \
				'	margin:0;' \
				'}' \
				'' \
				'p.indent {text-indent:1em;}'\
				'/* terminal comment */'

		stylesheet = StyleSheetReader.read_string(expected)
		assert expected == str(stylesheet)


	def test_read_filepath(self):
		expected = 'body {' \
				'	margin:0;' \
				'}' \
				'' \
				'p.indent {text-indent:1em;}'\
				'/* terminal comment */'
		handle, tmp_path = tempfile.mkstemp()
		f = open(tmp_path, 'w')
		f.write(expected)
		f.close()

		stylesheet = StyleSheetReader.read_filepath(tmp_path)
		assert expected == str(stylesheet)
		os.remove(tmp_path)
