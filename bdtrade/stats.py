
class EMA:
	def __init__(self):
		self._value = None
		self._archives = []

	def __str__(self):
		return str(self._value)

	@property
	def value(self): return self._value
	@property
	def archives(self): return self._archives

	def __calc(values, t, a):
		assert(t >= 0)
		if t == 0:
			return values[0]
		else:
			return a * values[t] + (1 - a) * EMA.__calc(values, t - 1, a)

	def update(self, values):
		a = 2 / (len(values) + 1)
		self._value = EMA.__calc(values, len(values) - 1, a)
		self._archives.append(self._value)


class MACD:
	def __init__(self):
		self._delta = None
		self._signal = EMA()
		self._archives = []

	@property
	def delta(self): return self._delta

	def __signOf(n):
		return 1 if n >= 0 else -1

	def isCrossOver(self):
		if len(self._archives) < 2:
			return 0
		else:
			prev_sign = MACD.__signOf(self._archives[-2] - self._signal.archives[-2])
			cur_sign = MACD.__signOf(self._delta - self._signal.value)
			if prev_sign == cur_sign:
				return 0
			elif cur_sign == 1:
				return 1
			else:
				return -1

	def update(self, ema12, ema26):
		self._delta = ema12.value - ema26.value
		self._archives.append(self._delta)
		start = max(0, len(self._archives) - 9)
		self._signal.update(self._archives[start:])


class Stats:
	EVAL_BUY = 1
	EVAL_SELL = 2
	EVAL_WAIT = 0

	def __init__(self):
		self._values = []
		self._last = None
		self._ema12 = EMA()
		self._ema26 = EMA()
		self._macd = MACD()

	def __str__(self):
		return "Stats(nvalues:{0}, ema12:{1}, ema26:{2}, macd:{3})"\
			.format(len(self._values), self._ema12, self._ema26, self._macd.isCrossOver())

	def feed(self, value):
		self._values.append(value)
		self._last = value
		self.__calcEMA(self._ema12, 12)
		self.__calcEMA(self._ema26, 26)
		self._macd.update(self._ema12, self._ema26)

	def __calcEMA(self, ema, period):
		start = max(0, len(self._values) - period)
		ema.update(self._values[start:])

	def eval(self):
		macd_res = self._macd.isCrossOver()
		if macd_res == 0:
			return Stats.EVAL_WAIT
		elif macd_res == 1:
			return Stats.EVAL_BUY
		else:
			return Stats.EVAL_SELL


