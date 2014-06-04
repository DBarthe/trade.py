
import sys

from bdtrade.input import Input
from bdtrade.box import Box
from bdtrade.executor import Executor
from bdtrade.stats import Stats

class Trader:
    def __init__(self):
        self._inp = Input()
        self._box = Box(self._inp.startK)
        self._stats = Stats()

    def run(self):
        while self._inp.nextDay() is not None:
            self._stats.feed(self._inp.curprice)
            if self._inp.isLastDay():
                self.__destock()
            else:
                self.__decide()
            # for debug :
            sys.stderr.write(str(self._inp)+", "+str(self._stats)+", "+str(self._box)+"\n")
            sys.stderr.flush()

    def __decide(self):
        self._stats.calcMovingAvg()
        gap = self._stats.moving_avg - self._inp.curprice
        relation = gap / self._inp.curprice
        sign = 0 if gap == 0 else (1 if gap > 0 else -1)
        if sign == 1:
            self.__trysell(int(0.2 * self._box.nshares))
        elif sign == -1:
            self.__trybuy(int(0.2 * self.__howManySharesCouldIBuy()))
        else:
            self.__wait()

    def __howManySharesCouldIBuy(self):
        return self._box.capital / self._inp.curprice

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
