import os
import re
from css_parser.tokenizer import Tokenizer
from css_parser.stylesheet import StyleSheet

class TestCases:

	def test_str_no_modifications(self):
		'''
		If we don't manipulate the stylesheet, is
		the original text being faithfully preserved?
		'''

		inputs = [
				'body {margin:0;}',
				'''body {
					margin:0;
					background:blue;
				}''',
				'''body {
					margin:0;
					background:blue;
				}
				
				@media amzn-kf8 {
					.mobi-hide {
						display:none;
					}
				}'''
				]

		for inp in inputs:
			yield self.check_str, inp
	
	def check_str(self, txt_in):
		tokens = Tokenizer.tokenize_string(txt_in)
		stylesheet = StyleSheet()
		stylesheet.set_tokens(tokens)
		txt_out = str(stylesheet)
		print 'expected:\n%s' % (txt_in)
		print '\nobserved:\n%s' % (txt_out)
		assert txt_in == txt_out

