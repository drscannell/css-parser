import os
import re
from css_parser.tokenizer import Tokenizer
from css_parser.parser import Parser
from css_parser.rulefactory import RuleFactory

class TestCases:

	def test_num_rules(self):
		tests = [

				# basic comment
				('/* comment */', 0),

				# one simple rule
				('body{margin:0;}', 1),

				# one rule, one commented rule
				('''/*body {
						margin:0;
					}*/
					div {
						padding:0;
					}''', 1),

				# two rules
				('body { ' \
				 '	margin:0;' \
				 '}' \
				 'div{padding:0;}', 2),

				# two rules w/ comment between
				('''body {
						margin:0;
					}
				/* comment */
				div{padding:0;}''', 2),

				# media query
				('\n@media screen and (min-width:300px) {\n' \
				 '	.page {\n' \
				 '		width: 100%;\n' \
				 '	}\n\n\n\n\n' \
				 '}', 1),

				# media query with two rules
				('@media screen and (min-width:300px) {' \
				 '	.page{width: 100%;}' \
				 '	div{width: 100%;}' \
				 '}', 2),

				# media query with two rules, spaced
				('@media screen and (min-width:300px) {' \
				 '	p { ' \
				 '		width: 100%;' \
				 '	}' \
				 '	div { ' \
				 '		width: 100%;' \
				 '	}' \
				 '}', 2),

				# media query w/ commented rule
				('@media screen and (min-width:300px) {' \
				 '	.page {' \
				 '		width: 100%;' \
				 '	}' \
				 '	/*p {' \
				 '		text-indent: 1em;' \
				 '	}*/' \
				 '}', 1),

				# media query w/ commented rule start
				('@media screen and (min-width:300px) {' \
				 '	.page {' \
				 '		width: 100%;' \
				 '	}' \
				 '	/*p { */' \
				 '}', 1),

				# media query w/ commented rule end
				('@media screen and (min-width:300px) {' \
				 '	.page {' \
				 '		width: 100%;' \
				 '	}' \
				 '	/* } */' \
				 '}', 1),

				# rule with a bunch of linebreaks after
				('body {margin:0;}\n\n\n\n', 1),

				# media query with a bunch of linebreaks after
				('@media amzn-mobi {.mobi-hide {display:none;}}\n\n\n\n', 1),

				# media query with a bunch of linebreaks then another rule
				('@media amzn-mobi {.mobi-hide {display:none;}}\n\n\n\n' \
						'p.indent {margin:0;}', 2)


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


