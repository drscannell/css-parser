from mediaquery import MediaQuery

class MediaQueryFactory:

	@classmethod
	def construct(cls, starttokens, endtokens):
		query = MediaQuery(starttokens, endtokens)
		return query
