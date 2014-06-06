
import sys

from bdtrade.input import Input
from bdtrade.box import Box
from bdtrade.executor import Executor
from bdtrade.stats import Stats

class Trader:
    INDICE = 0.25
    WAIT_DAYS = 0

    def __init__(self, verbose=False):
        self._inp = Input()
        self._box = Box(self._inp.startK)
        self._stats = Stats()
        self._verbose = verbose
        if self._verbose:
            Executor.logOn()

    def run(self):
        while self._inp.nextDay() is not None:
            self._stats.feed(self._inp.curprice)

            if self._verbose:
                Executor.log("***********\n"+str(self._inp)+"\n"+str(self._stats)+\
                    "\n"+str(self._box)+"\n")

            if self._inp.isLastDay():
                self.__destock()
            else:
                self.__decide()

    def __decide(self):
        if self._inp.curday < Trader.WAIT_DAYS:
            self.__wait()
        else:
            eva = self._stats.eval()
            if eva == Stats.EVAL_WAIT:
                self.__wait()
            elif eva == Stats.EVAL_BUY:
                self.__trybuy(int(self.__howManySharesCouldIBuy() * Trader.INDICE))
            else:
                self.__trysell(int(self._box.nshares * Trader.INDICE))

    def __howManySharesCouldIBuy(self):
        return int((self._box.capital - Box.calcCommission(self._box.capital))\
                 / self._inp.curprice)

    def __trybuy(self, nshares):
        if self._inp.curprice > 0:
            nshares = min(nshares, self.__howManySharesCouldIBuy())
        if nshares == 0:
            self.__wait()
        else:
            if self._box.purchase(nshares * self._inp.curprice, nshares):
                Executor.buy(nshares)
            else:
                self.__wait()

    def __trysell(self, nshares):
        if nshares == 0:
            self.__wait()
        else:
            nshares = min(nshares, self._box.nshares)
            if self._box.sale(nshares * self._inp.curprice, nshares):
                Executor.sell(nshares)
            else:
                self.__wait()

    def __wait(self):
        Executor.wait()

    def __destock(self):
        self.__trysell(self._box.nshares)
