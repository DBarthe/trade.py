
import sys

class Executor:

	_out = sys.stdout
	_log = None

	def logOn(out=sys.stderr):
		Executor._log = out

	def logOff():
		Executor._log = None

	def setOut(out=sys.stdout):
		Executor._out = out

	def __write(s, out):
		out.write(s)
		out.flush()

	def log(s):
		if Executor._log:
			Executor.__write(s, Executor._log)

	def __send(s):
		Executor.__write(s, Executor._out)
		Executor.log(s)

	def buy(nshares):
		assert(nshares >= 0)
		Executor.__send("buy {0}\n".format(nshares))
		
	def sell(nshares):
		assert(nshares >= 0)
		Executor.__send("sell {0}\n".format(nshares))

	def wait():
		Executor.__send("wait\n")

