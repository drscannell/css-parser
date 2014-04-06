from css_parser.declaration import Declaration

class TestCases:

	# ----------------------------------------

	def test_from_string(self):
		tests = [
				{'input': 'margin:0;',
				 'prop': 'margin',
				 'val': '0'					
				 },
				{'input': 'margin:0;',
				 'prop': 'margin',
				 'val': '0'					
				 }

				]

		for test in tests:
			yield self.check_from_string, test
	
	def check_from_string(self, test):
		decl = Declaration.from_string(test['input'])
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed prop: %s' % (decl.get_property())
		print 'observed val: %s' % (decl.get_value())
		assert test['prop'] == decl.get_property()
		assert test['val'] == decl.get_value()

	# ----------------------------------------



