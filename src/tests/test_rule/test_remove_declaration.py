from css_parser.rule import Rule

class TestCases:

	# ----------------------------------------

	def test_remove_declaration(self):
		tests = [
				# two declarations, remove one
				{'input': 'body{' \
						'	margin:0;' \
						'	padding:0;' \
						'}',
				 'query': 'margin',
				 'expected': 'body{' \
						'	' \
						'	padding:0;' \
						'}'
					},
				# three declarations, remove two
				{'input': 'body{' \
						'	color:blue;' \
						'	padding:0;' \
						'	color:red;' \
						'}',
				 'query': 'color',
				 'expected': 'body{' \
						'	' \
						'	padding:0;' \
						'	' \
						'}'
					}

				]

		for test in tests:
			yield self.check_remove_declaration, test
	
	def check_remove_declaration(self, test):
		rule = Rule.from_string(test['input'])
		for toremove in rule.get_declarations(test['query']):
			rule.remove_declaration(toremove)
		observed = rule.to_string()
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed: %s' % (observed)
		assert observed == test['expected']

	# ----------------------------------------


