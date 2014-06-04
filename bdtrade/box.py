
class Box:
	def __init__(self, capital, nshares=0):
		self._capital = capital
		self._nshares = nshares

	def __str__(self):
		return "Box(capital:{0}, nshares:{1})"\
			.format(self._capital, self._nshares)

	@property
	def capital(self):
		return self._capital

	@property
	def nshares(self):
		return self._nshares

	def purchase(self, cost, nshares):
		assert(cost >= 0)
		assert(nshares >= 0)
		if cost <= self._capital:
			self._capital -= cost
			self._nshares += nshares
			return True
		else:
			return False
		
	def sale(self, income, nshares):
		assert(income >= 0)
		assert(nshares >= 0)
		if nshares <= self._nshares:
			self._capital += income
			self._nshares -= nshares
			return True
		else:
			return False
