
LONG_TERM = 60
MEDIUM_TERM = 30
SHORT_TERM = 15

class MovingAvg:
	def __init__(self):
		self._value = None
		self._gap = None
		self._rel = None
		self._len = None
		self._archives = []
		self._speed = None
		self._speed_rel = None

	@property
	def value(self): return self._value
	@property
	def gap(self): return self._gap
	@property
	def rel(self): return self._rel
	@property
	def len(self): return self._len
	@property
	def archives(self): return sefl._archives
	@property
	def archive(self, n): return self._archive[n]
	@property
	def speed(self): return self._speed
	@property
	def speed_rel(self): return self._speed_rel

	def __calcTriangularNbr(n):
		return (n * (n + 1)) / 2

	def update(self, values):
		if len(values) > 0:
			self._value = \
				sum([(i + 1) * xi for i, xi in enumerate(values)]) / \
				MovingAvg.__calcTriangularNbr(len(values))
			self._gap = values[-1] - self._value
			self._rel = abs(self._gap) / values[-1]
			self._len = len(values)
			self._archives.append(self._value)
			if len(self._archives) >= 2:
				self._speed = self._archives[-1] - self._archives[-2]
				self._speed_rel = abs(self._speed) / self._value


class Stats:
	def __init__(self):
		self._values = []
		self._last = None
		self._mavg_total = MovingAvg()
		self._mavg_long = MovingAvg()
		self._mavg_medium = MovingAvg()
		self._mavg_short = MovingAvg()
		self._speed = None

	def __str__(self):
		return "Stats(nvalues:{0}, mavg_tot:{1}, mavg_long:{2}, mavg_medium:{3}, mavg_short:{4})"\
			.format(len(self._values), self._mavg_total, self._mavg_long, self._mavg_medium, self._mavg_short)

	@property
	def mavg_total(self): return self._mavg_total
	@property
	def mavg_long(self): return self._mavg_long
	@property
	def mavg_medium(self): return self._mavg_medium
	@property
	def mavg_short(self): return self._mavg_short
	@property
	def speed(self): return self._speed
	@property
	def tendance(self): return self._tendance

	def feed(self, value):
		self._values.append(value)
		self._last = value
		self.__calcMovingAvgTotal()
		self.__calcMovingAvgLong()
		self.__calcMovingAvgMedium()
		self.__calcMovingAvgShort()
		if len(self._values) >= 2:
			self._speed = self._values[-1] - self._values[-2]

	def __calcMovingAvg(self, mavg, term):
		start = max(0, len(self._values) - term)
		mavg.update(self._values[start:])

	def __calcMovingAvgTotal(self):
		self._mavg_total.update(self._values)

	def __calcMovingAvgLong(self):
		self.__calcMovingAvg(self._mavg_long, LONG_TERM)

	def __calcMovingAvgMedium(self):
		self.__calcMovingAvg(self._mavg_medium, MEDIUM_TERM)

	def __calcMovingAvgShort(self):
		self.__calcMovingAvg(self._mavg_short, SHORT_TERM)
