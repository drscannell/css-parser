import os
import re
from css_parser.tokenizer import Tokenizer
from css_parser.parser import Parser
from css_parser.rulefactory import RuleFactory

class TestCases:

	def test_num_rules(self):
		tests = [
				('/* comment */', 0),
				('body{margin:0;}', 1),
				('''/*body {
						margin:0;
					}*/
					div {
						padding:0;
					}''', 1),
				('body{margin:0;}\ndiv{padding:0;}', 2),
				('''body {
						margin:0;
					}
				/* comment */
				div{padding:0;}''', 2),
				('''@media screen and (min-width:300px) {
						.page {
							width: 100%;
						}
					}''', 1)

				]

		for test in tests:
			yield self.check_num_rules, test
	
	def check_num_rules(self, test):
		txt, expected = test
		stylesheet = Parser.parse_string(txt)
		rules = stylesheet.get_rules()
		observed = len(rules)
		print 'input: %s' % (txt)
		print 'expected: %i rules' % (expected)
		print 'observed: %i rules' % (observed)
		assert expected == observed


