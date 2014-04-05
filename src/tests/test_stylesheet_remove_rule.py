import os
import re
from css_parser.tokenizer import Tokenizer
from css_parser.stylesheet import StyleSheet
from css_parser.stylesheet_reader import StyleSheetReader
from css_parser.rulefactory import RuleFactory

class TestCases:

	def test_remove_rule(self):
		tests = [
				{'descrip': 'one rule',
				 'txt': 'body{margin:0;}',
				 'indextoremove': 0,
				 'expected_num_rules': 0,
				 'expected_txt':''
				 },
				{'descrip': 'two rules, remove one',
				 'txt': 'body{margin:0;}' \
						 '/* comment */' \
						 'p.indent {padding:0;}',
				 'indextoremove': 1,
				 'expected_num_rules': 1,
				 'expected_txt':'body{margin:0;}' \
						 '/* comment */' \
						 ''
				 },
				{'descrip': 'two rules in mediaqueyr, remove one',
				 'txt': '@media all {' \
						 '	body{margin:0;}' \
						 '	p.indent {padding:0;}' \
						 '}',
				 'indextoremove': 1,
				 'expected_num_rules': 1,
				 'expected_txt':'@media all {' \
						 '	body{margin:0;}' \
						 '	' \
						 '}'
				 }

				]

		for test in tests:
			yield self.check_remove_rule, test
	
	def check_remove_rule(self, test):
		stylesheet = StyleSheetReader.read_string(test['txt'])
		ruletoremove = stylesheet.get_rules()[test['indextoremove']]
		stylesheet.remove_rule(ruletoremove)
		observed_num_rules = len(stylesheet.get_rules())
		observed_txt = str(stylesheet)
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed num rules: %s' % (observed_num_rules)
		print 'observed txt: %s' % (observed_txt)
		assert observed_num_rules == test['expected_num_rules']
		assert observed_txt == test['expected_txt']

	# ----------------------------------------




