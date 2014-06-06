
import sys

class Input:

	def __init__(self, inp=sys.stdin):
		self._inp = inp
		self._ndays = None
		self._startK = None
		self._curday = 0
		self._curprice = None
		self.__readFirst()

	def __str__(self):
		return "Input(day:{0}/{1}, startK:{2}, curprice:{3})"\
			.format(self._curday, self._ndays, self._startK, self._curprice)

	@property
	def ndays(self):
		return self._ndays

	@property
	def startK(self):
		return self._startK

	@property
	def curday(self):
		return self._curday

	@property
	def curprice(self):
		return self._curprice

	def __readLine(self):
		sys.stdin.flush()
		line = self._inp.readline()
		# for debug:
		#sys.stderr.write("readline="+line)
		#sys.stderr.flush()
		return line

	def __readInt(self):
		return int(self.__readLine())

	def __readFloat(self):
		return float(self.__readLine())

	def __readFirst(self):
		self._startK = self.__readFloat()
		self._ndays = self.__readInt()

	def nextDay(self):
		self._curday += 1
		if self._curday > self._ndays:
			return None
		else:
			self._curprice = self.__readFloat()
			return self._curprice

	def isLastDay(self):
		return self._curday == self._ndays