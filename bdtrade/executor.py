
import sys

class Executor:

	def __write(s, out=sys.stdout):
		out.write(s)
		out.flush()

	def buy(nshares):
		assert(nshares >= 0)
		Executor.__write("buy {0}\n".format(nshares))
		Executor.__write("buy {0}\n".format(nshares), sys.stderr)
		
	def sell(nshares):
		assert(nshares >= 0)
		Executor.__write("sell {0}\n".format(nshares))
		Executor.__write("sell {0}\n".format(nshares), sys.stderr)

	def wait():
		Executor.__write("wait\n")
		Executor.__write("wait\n", sys.stderr)

