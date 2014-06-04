
class Stats:
	def __init__(self):
		self._values = []
		self._last = None
		self._moving_avg = None

	def __str__(self):
		return "Stats(nvalues:{0}, moving_avg:{1})"\
			.format(len(self._values), self._moving_avg)

	@property
	def moving_avg(self):
		return self._moving_avg

	def feed(self, value):
		self._values.append(value)
		self._last = value

	def __calcTriangularNbr(n):
		return (n * (n + 1)) / 2

	def calcMovingAvg(self):
		if len(self._values) > 0:
			 self._moving_avg = \
			 	sum([(i + 1) * xi for i, xi in enumerate(self._values)]) / \
			 	Stats.__calcTriangularNbr(len(self._values))
