
import sys

class Executor:
 	def buy(nshares):
 		assert(nshares >= 0)
 		sys.stdout.write("buy {0}\n".format(nshares))
 		sys.stdout.flush()

 	def sell(nshares):
 		assert(nshares >= 0)
 		sys.stdout.write("sell {0}\n".format(nshares))
 		sys.stdout.flush()

 	def wait():
 		sys.stdout.write("wait\n")
 		sys.stdout.flush()
