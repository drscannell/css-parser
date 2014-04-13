from css_parser.rule import Rule
from css_parser.declaration import Declaration

class TestCases:

	# ----------------------------------------

	def test_prepend_declaration(self):
		tests = [
				# two declarations, add one
				{'input': 'body{' \
						'	margin:0;' \
						'	padding:0;' \
						'}',
				 'to_add': 'color:blue;',
				 'existing_index': None,
				 'expected': 'body{color:blue;' \
						'	margin:0;' \
						'	padding:0;' \
						'}'
					},
				{'input': 'body{' \
						'	margin:0;' \
						'	padding:0;' \
						'}',
				 'to_add': 'color:blue;',
				 'existing_index': 0,
				 'expected': 'body{' \
						'	color:blue;margin:0;' \
						'	padding:0;' \
						'}'
					}
				]

		for test in tests:
			yield self.check_prepend_declaration, test
	
	def check_prepend_declaration(self, test):
		rule = Rule.from_string(test['input'])
		decl = Declaration.from_string(test['to_add'])
		existing_rule = None
		if test['existing_index'] != None:
			existing_rule = rule.declarations[test['existing_index']]
		rule.prepend_declaration(decl, existing_rule)
		observed = rule.to_string()
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed: %s' % (observed)
		assert observed == test['expected']

	# ----------------------------------------





