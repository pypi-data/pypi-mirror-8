# -*- coding: UTF-8 -*-
"""Модуль, описывающий различные типы носителей нечетких множеств, а также
реализующий функциональность нечетких правил логического вывода.
"""

import pyinference.fuzzy


class Domain(object):
    """Абстрактный класс, реализующий интерфейс носителя нечеткого множества.

    Смысловую нагрузку несут подклассы этого класса,
    представляющие различные виды носителей. Преимуществом такого подхода
    является его универсальность: в качестве носителя при определении
    нечеткого множества можно задавать действительный интервал,
    целочисленный интервал, в принципе, любую итерируемую структуру.
    """
    def __init__(self):
        pass

    def __iter__(self):
        pass

    def char(self):
        for i in self:
            print i

    def card(self):
        """Cardinality of the domain
        """
        pass


class RationalRange(Domain):
    """Данный класс реализует носитель нечеткого подмножества в виде отрезка действительной оси.

    В качестве параметров конструктор класса
    принимает значения начала и конца интервала, а также параметр "точность" -
    целое число, определяющее количество проходов при расчете нечетких
    функционалов численным методом. Это число является компромиссом между
    точностью и скоростью подсчета, поэтому там, где это возможно,
    численный расчет нечетких функционалов заменен аналитическими выражениями.

    Синтаксис:

        >>> B = RationalRange(end=3.0, acc=3)
        >>> for i in B: print i
        0.0
        1.0
        2.0
        3.0

        >>> B = RationalRange(end=3.0, acc=8)
        >>> for i in B: print i
        0.0
        0.375
        0.75
        1.125
        1.5
        1.875
        2.25
        2.625
        3.0

    Attributes:
        begin:
        end:
        acc:
    """

    def __init__(self, begin=0.0, end=1.0, acc=pyinference.fuzzy.ACCURACY):
        super(RationalRange, self).__init__()
        self.begin = float(begin)
        self.end = float(end)
        self.acc = acc

    def __iter__(self):
        if self.begin == self.end:
            for i in range(self.acc):
                yield self.begin
        else:
            delta = (self.end - self.begin) / self.acc
            i = self.begin
            while i <= self.end:
                yield i
                i += delta

    def card(self):
        return len(self)

    def __len__(self):
        return self.end - self.begin

    def __contains__(self, item):
        if self.begin <= item <= self.end:
            return True
        return False

    def __abs__(self):
        return self.card()


class IntegerRange(RationalRange):
    """Класс, моделирующий носитель нечеткого множества в виде целочисленного интервала.

    По сути, является частным случаем предыдущего класса
    (см. :class:`RationalRange`), когда точность равна разнице границ интервала.

   Синтаксис:

        >>> B=IntegerRange(begin=0.0, end=3.0)
        >>> for i in B: print i
        0
        1
        2
        3

    Attributes:
        begin
        end

    """

    def __init__(self, begin=1, end=100):
        begin = int(begin)
        end = int(end)
        acc = end - begin or 1
        super(IntegerRange, self).__init__(begin, end, acc)
        self.begin = begin
        self.end = end

    def __contains__(self, item):
        if int(item) == item and self.begin <= item <= self.end:
            return True
        return False
