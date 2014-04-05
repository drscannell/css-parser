import os
import re
from css_parser.tokenizer import Tokenizer
from css_parser.stylesheet import StyleSheet
from css_parser.stylesheet_reader import StyleSheetReader
from css_parser.rulefactory import RuleFactory

class TestCases:

	def test_get_rules(self):
		tests = [
				{'descrip': 'one rule',
				 'txt': 'body{margin:0;}',
				 'query': 'body',
				 'expected': 1
				 },
				{'descrip': 'two rules, query by class',
				 'txt': 'body {' \
						 '	margin:0;' \
						 '}' \
						 '.indent {' \
						 '	margin:0;' \
						 '}',
				 'query': '.indent',
				 'expected': 1
				 },
				{'descrip': 'four rules, two matches',
				 'txt': 'body { margin:0;}' \
						 '	.indent {margin:0;}' \
						 '	p.indent {margin:0;}' \
						 '	.indent {text-indent:5px;}',
				 'query': '.indent',
				 'expected': 2
				 },
				{'descrip': 'multiple selectors on rule',
				 'txt': 'body,p,div,span { margin:0;}' \
						 '	p.indent {text-indent:5px;}',
				 'query': 'p',
				 'expected': 1
				 },
				{'descrip': 'multiple selectors on rule, search by tag#id',
				 'txt': 'body,p,div,span { margin:0;}' \
						 'h1.heading,' \
						 'h2.heading,' \
						 'div#app,' \
						 'p#content {' \
						 '	margin:20px 0 20px 0;' \
						 '}' \
						 '	div#app {font-weight:bold;}',
				 'query': 'div#app',
				 'expected': 2
				 },
				{'descrip': 'child selector',
				 'txt': 'body,p,div,span { margin:0;}' \
						 'h1.heading > strong {font-family: StrongCoffeeBold;}', 
				 'query': 'h1.heading > strong',
				 'expected': 1
				 },
				{'descrip': 'child selector, extra space in stylesheet',
				 'txt': 'body,p,div,span { margin:0;}' \
						 'h1.heading >   strong {font-family: StrongCoffeeBold;}', 
				 'query': 'h1.heading > strong',
				 'expected': 1
				 },
				{'descrip': 'child selector, extra space in query',
				 'txt': 'body,p,div,span { margin:0;}' \
						 'h1.heading > strong {font-family: StrongCoffeeBold;}', 
				 'query': 'h1.heading   >       strong',
				 'expected': 1
				 }
				]

		for test in tests:
			yield self.check_get_rules, test
	
	def check_get_rules(self, test):
		stylesheet = StyleSheetReader.read_string(test['txt'])
		results = stylesheet.get_rules(test['query'])
		observed = len(results)
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed: %s' % (observed)
		assert observed == test['expected']

	# ----------------------------------------



