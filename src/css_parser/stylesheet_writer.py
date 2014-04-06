class StyleSheetWriter:

	@classmethod
	def write_string(cls, stylesheet):
		return str(stylesheet)

	@classmethod
	def write_filepath(cls, stylesheet, filepath):
		f = open(filepath, 'w')
		f.write(str(stylesheet))
		f.close()

