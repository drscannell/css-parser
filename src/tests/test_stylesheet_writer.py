import os
import tempfile
from css_parser.stylesheet import StyleSheet

class TestCases:

	def test_write_string(self):
		expected = 'body {' \
				'	margin:0;' \
				'}' \
				'' \
				'p.indent {text-indent:1em;}'\
				'/* terminal comment */'

		stylesheet = StyleSheet.from_string(expected)
		observed = stylesheet.to_string()
		assert expected == observed


	def test_write_filepath(self):
		expected = 'body {' \
				'	margin:0;' \
				'}' \
				'' \
				'p.indent {text-indent:1em;}'\
				'/* terminal comment */'
		stylesheet = StyleSheet.from_string(expected)
		handle, tmp_path = tempfile.mkstemp()
		stylesheet.to_file(tmp_path)

		f = open(tmp_path, 'r')
		observed = f.read()
		f.close()

		assert expected == observed
		os.remove(tmp_path)
