import os
import tempfile
from css_parser.stylesheet_reader import StyleSheetReader
from css_parser.stylesheet_writer import StyleSheetWriter

class TestCases:

	def test_write_string(self):
		expected = 'body {' \
				'	margin:0;' \
				'}' \
				'' \
				'p.indent {text-indent:1em;}'\
				'/* terminal comment */'

		stylesheet = StyleSheetReader.read_string(expected)
		observed = StyleSheetWriter.write_string(stylesheet)
		assert expected == observed


	def test_write_filepath(self):
		expected = 'body {' \
				'	margin:0;' \
				'}' \
				'' \
				'p.indent {text-indent:1em;}'\
				'/* terminal comment */'
		stylesheet = StyleSheetReader.read_string(expected)
		handle, tmp_path = tempfile.mkstemp()
		StyleSheetWriter.write_filepath(stylesheet, tmp_path)

		f = open(tmp_path, 'r')
		observed = f.read()
		f.close()

		assert expected == observed
		os.remove(tmp_path)
