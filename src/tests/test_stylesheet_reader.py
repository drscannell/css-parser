import os
import tempfile
from css_parser.stylesheet import StyleSheet

class TestCases:

	def test_read_string(self):
		expected = 'body {' \
				'	margin:0;' \
				'}' \
				'' \
				'p.indent {text-indent:1em;}'\
				'/* terminal comment */'

		stylesheet = StyleSheet.from_string(expected)
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

		stylesheet = StyleSheet.from_file(tmp_path)
		assert expected == str(stylesheet)
		os.remove(tmp_path)
