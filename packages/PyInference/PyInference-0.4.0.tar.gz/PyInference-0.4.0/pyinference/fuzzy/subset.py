﻿# -*- coding: UTF-8 -*-

"""Модуль реализует набор базовых типов, представляющих разные виды нечетких подмножеств.
"""

import pyinference.fuzzy.domain
from pyinference.fuzzy.tnorm import MinMax

import pylab as p
import math


class Subset(object):
    """ Нечеткое подмножество.

    Реализует функциональность нечеткого подмножества общего вида.
    Имеет атрибуты, указывающие начало и конец интервала определения подмножества (для подмножеств, определенных на R).

    Syntax:
        >>> A = Subset()
        >>> A.domain.begin
        0.0
        >>> A.domain.end
        1.0

    Attributes:
        values (dict):

        points (dict):

        domain (pyinference.fuzzy.domain.Domain):

    Kwargs:
        begin (float):

        end (float):

        begin (pyinference.fuzzy.domain.Domain):
    """

    def __init__(self, begin=0.0,
                 end=1.0,
                 domain=None):

        self.domain = domain or pyinference.fuzzy.domain.RationalRange(begin, end)
        self.values = {}
        self.points = {}

        self.values[self.domain.begin] = 0.0
        self.values[self.domain.end] = 0.0
        self.points[self.domain.begin] = 0.0
        self.points[self.domain.end] = 0.0

        self._algebra = SubsetAlgebra()

    def value(self, key):
        """
        Возвращает уровень принадлежности точки нечеткому подмножеству.
        Данный метод непосредственно и является программной имплементацией
        функции принадлежности.
        >>> A = Gaussian(1.0, 1.0)
        >>> A.value(0.5)
        0.8825
        >>> A.value(1.5)
        0.8825
        >>> A.value(1.0)
        1.0
        >>> A.value(0.0)
        0.60653
        """
        if isinstance(key, Subset):
            return self.__cmp__(key)

        if not key in self.domain:
            return 0.0
        try:
            return self.values[key]
        except KeyError:
            sort = sorted(self.values.keys())
            sort1 = sorted(self.values.keys())
            sort1.pop(0)
            for (i, j) in zip(sort, sort1):
                if i < key < j:
                    return (key - i) * (self[j] - self[i]) / (j - i) + self[i]

    def char(self):
        """
        Выводит на экран список элементов носителя и соответствующих им значений
        нечеткого множества. Шаг перебора непрерывного носителя совпадает с
        частотой дискретизации при численных вычислениях
        Синтаксис:
            >>> A = Triangle(1.0, 2.0, 4.0)
            >>> A.domain.acc=5
            >>> A.char()
            1.0 0.0
            1.6 0.6
            2.2 0.9
            2.8 0.6
            3.4 0.3
            4.0 0.0

        """
        for i in self.domain:
            print i, self.value(i)

    def normalize(self):
        """
        Возвращает нормированное по высоте нечеткое множество.
        Синтаксис:
            >>> A = Triangle(1.0, 2.0, 4.0)
            >>> A.domain.acc=5
            >>> B = A*0.5
            >>> '%0.3f' % B.card()
            '0.720'
            >>> '%0.3f' % A.card()
            '1.500'
            >>> C = B.normalize()
            >>> '%0.3f' % C.card()
            '1.600'
            >>> '%0.3f' % B.value(B.mode())
            '0.450'
            >>> '%0.3f' % C.value(C.mode())
            '1.000'

        """
        sup = self.sup()
        if sup == 0.0:
            return self
        res = Subset(self.domain.begin, self.domain.end)
        for i in self.domain:
            res[i] = self.value(i) / sup
        return res

    def sup(self):
        sup = 0.0
        for i in self.domain:
            if self.value(i) > sup:
                sup = self.value(i)
        return sup

    def plot(self, verbose=True, subplot=p):
        """
        Отображает нечеткое множество графически. Только для нечетких множеств,
        определенных на носителе типа RationalRange. Параметр verbose
        определяет отображение на графике дополнительной информации.
        Синтаксис:
            >>> A=Triangle(2.5, 3.8, 10.2)
            >>> A.plot()
            >>> A.plot()
            >>> A.plot(verbose=False)

        """
        xxx = []
        yyy = []
        for i in self.domain:
            xxx.append(i)
            yyy.append(self.value(i))
        subplot.plot(xxx, yyy)
        if isinstance(self.domain, pyinference.fuzzy.domain.IntegerRange):
            # TODO построение графиков НПМ на целочисленных интервалах.
            pass
        subplot.plot(self.domain.begin, 1.2)
        subplot.plot(self.domain.end + (self.domain.end - self.domain.begin) / 3, -0.1)
        if verbose:
            subplot.text(self.domain.begin, 0.0, str(self.domain.begin))
            subplot.text(self.domain.end, 0.0, str(self.domain.end))
            for i in self.points.iterkeys():
                subplot.text(i, self.points[i], str(i))

    def level(self, lvl):
        begin = self.domain.begin
        end = self.domain.end
        for i in self.domain:
            if self.value(i) >= float(lvl):
                begin = i
                break
        for i in self.domain:
            if (self.value(i) <= lvl) and (i > begin):
                end = i
                break
        res = Interval(begin, end)
        return res

    def __getitem__(self, key):
        return self.value(key)

    def __setitem__(self, key, value):
        if not key in self.domain:
            raise KeyError
        self.values[key] = value

    def centr(self):
        """
        Вычисляет центроид (центр масс) нечеткого подмножества.
        Зависит от конфигурации ФП. Работает как на непрерывных
        ФП заданного вида, так и на ФП произвольного вида.
        >>> A=Triangle(0.2, 0.3, 0.4)
        >>> print round(A.centr(), 3)
        0.3
        >>> A=Trapezoidal((1.0, 2.0, 5.0, 6.0))
        >>> "%0.2f" % A.centr()
        '3.50'
        """
        sum_ = 0.0
        j = 0.0
        for i in self.domain:
            sum_ += self[i] * i
            j += self[i]
        if j != 0:
            return sum_ / j
        else:
            return (self.domain.end - self.domain.begin) / 2

    def card(self):
        """
        Возвращает мощность нечеткого подмножества
        Синтаксис:
            >>> T=Triangle(-1.4, 0.0, 2.6)
            >>> print round(T.card(), 2) # doctest: +SKIP
            4.0
        """
        sum_ = 0.0
        for i in self.domain:
            sum_ += self.value(i)
        return sum_ * (self.domain.end - self.domain.begin) / self.domain.acc

    def mode(self):
        """ Возвращает моду (точку максимума) нечеткого подмножества.

        Синтаксис:
            >>> A = Triangle(10, 20, 40)
            >>> A.mode()
            20.0
            >>> B = Triangle(20, 40, 50)
            >>> B.mode()
            40.0
            >>> C = A + B
            >>> '%0.3f' % C.mode()
            '20.040'
        """
        res = self.domain.begin
        for i in self.domain:
            if self.value(i) > self.value(res):
                res = i
        return res

    def euclid_distance(self, other):
        begin = min(self.domain.begin, other.domain.begin)
        end = max(self.domain.end, other.domain.end)
        acc = max(self.domain.acc, other.domain.acc)

        domain = pyinference.fuzzy.domain.RationalRange(begin, end, acc=acc)

        summ = 0.0
        for i in domain:
            summ += (self.value(i) - other.value(i)) ** 2

        return math.sqrt(summ / acc)

    def hamming_distance(self, other):
        begin = min(self.domain.begin, other.domain.begin)
        end = max(self.domain.end, other.domain.end)
        acc = max(self.domain.acc, other.domain.acc)

        domain = pyinference.fuzzy.domain.RationalRange(begin, end, acc=acc)

        summ = 0.0
        for i in domain:
            summ += abs(self.value(i) - other.value(i))

        return summ / acc

    def __add__(self, other):
        return self._algebra.__add__(self, other)

    def __sub__(self, other):
        return self._algebra.__sub__(self, other)

    def __mul__(self, other):
        return self._algebra.__mul__(self, other)

    def __div__(self, other):
        return self._algebra.__div__(self, other)

    def __pow__(self, other):
        return self._algebra.__pow__(self, other)

    def __invert__(self):
        return self.__neg__()

    def __not__(self):
        return self.__neg__()

    def __neg__(self):
        res = Subset(domain=self.domain)
        for i in res.domain:
            res[i] = 1 - self.value(i)
        return res

    def __and__(self, other):
        return self._algebra.__and__(self, other)

    def __or__(self, other):
        return self._algebra.__or__(self, other)

    def __abs__(self):
        return self.card()

    def __str__(self):
        return str(self.centr())

    # TODO протестировать следующие три функции
    def __cmp__(self, other):
        return self._algebra.__eq__(self, other)

    def __eq__(self, other):
        if other in self.domain:
            return self.value(other)
        elif isinstance(other, Subset):
            return self._algebra.__eq__(self, other)
        else:
            raise NotImplementedError

    def __ne__(self, other):
        return 1 - (self == other)


class Trapezoidal(Subset):
    """
    Нечеткое множество с трапециевидной функцией принадлежности.
    Синтаксис:
        >>> A = Trapezoidal((0.0, 1.5, 2.8, 6.6))

    Параметры:
        begin
            задает нижнюю границу левого ската трапеции. Значение
            принадлежности в этой точке равно 0.
        begin_tol
            задает нижнюю границу интервала толернтности. Значение
            принадлежности равно 1.
        end_tol
            верхняя граница интервала толерантности. Значение - 1.
        end
            верхняя граница правого ската трапеции. Значение - 0.
        domain
            Этим параметром можно задать границы области определения нечеткого
            множества. Подробнее см. RationalRange и IntegerRange.

        Attributes:
            begin_tol
            end_tol
    """

    def __init__(self, points):
        (begin, begin_tol, end_tol, end) = points

        super(Trapezoidal, self).__init__(begin, end)

        self.domain.begin = float(begin)
        self.begin_tol = float(begin_tol)
        self.end_tol = float(end_tol)
        self.domain.end = float(end)

        self[begin] = 0.0
        self[end] = 0.0
        self[begin_tol] = 1.0
        self[end_tol] = 1.0

    def card(self):
        return (self.begin_tol - self.domain.begin) / 2 + \
            self.end_tol - self.begin_tol + \
            (self.domain.end - self.end_tol) / 2

    def mom(self):
        return (self.end_tol + self.begin_tol) / 2

    def mode(self):
        return self.begin_tol

    def median(self):
        return (self.domain.begin + self.begin_tol + self.domain.end + self.end_tol) / 4

    def __eq__(self, other):
        # #        if isinstance(other, Trapezoidal):
        # #            if self.domain.begin == other.domain.begin and \
        # #                self.begin_tol == other.begin_tol and \
        # #                self.end_tol == other.end_tol and \
        ##                self.domain.end == other.domain.end:
        ##                return True
        ##            else:
        ##                return False
        ##        else:
        return Subset.__eq__(self, other)


class Triangle(Trapezoidal):
    """
    Нечеткое множество с функцией принадлежности в виде треугольника.
    Фактически, представляет собой частный случай трапециевидного нечеткого
    множества с вырожденным в точку интервалом толерантности. Этот класс
    создан для быстрого создания нечетких множеств наиболее распространенной
    (треугольной) формы.
    Синтаксис:
        >>> A=Triangle(1.0, 2.3, 5.6)

    Параметры:
        Принимает три параметра, по порядку: нижняя раница ската, точка моды,
        верхняя граница ската. Числа должны быть упорядочены по возрастанию.

    Attributes:
        a
        b
        c

    """

    def __init__(self, a, b, c):
        super(Triangle, self).__init__((a, b, b, c))

    def mode(self):
        return self.begin_tol

    def card(self):
        return (self.domain.end - self.domain.begin) / 2


class Interval(Trapezoidal):
    """
    Определяет четкий интервал как частный вид нечеткого множества. Конструктор
    принимает два параметра - границы интервала.
    Синтаксис:
        >>> A=Interval(0.5, 6.4)

    """

    def __init__(self, a, b, x=1.0):
        super(Interval, self).__init__((a, a, b, b))
        self.level = x

    def card(self):
        return self.end_tol - self.begin_tol

    def value(self, value):
        if value in self.domain:
            return self.level
        else:
            return 0.0


class Point(Trapezoidal):
    """
    Реализует нечеткое множество состоящее из одной точки.
    Синтаксис:
        >>> A=Point(2.0)

    """

    def __init__(self, a):
        super(Point, self).__init__((a, a, a, a))

    def value(self, x):
        if x != self.domain.begin:
            return 0.0
        elif self.domain.begin == x:
            return 1.0
        else:
            return -1

    def plot(self, verbose=True, subplot=p):
        subplot.scatter([self.domain.begin], [1.0])
        subplot.plot(self.domain.begin, 1.0)

    def card(self):
        return 0.0


class Gaussian(Subset):
    """
    Определяет нечеткое множество с функцией принадлежности в виде гауссианы.
    Синтаксис:
        >>> A=Gaussian(0.0, 1.0)    # Стандартное распределение

    Первый параметр - мода гауссианы, второй - стандартное отклонение (омега)
    Attributes:
        mu
        omega
    """

    def __init__(self, mu, omega):
        super(Gaussian, self).__init__(mu - 5 * omega, mu + 5 * omega)

        self.median = float(mu)
        self.omega = float(omega)

    def value(self, x):
        return round(math.exp(-((x - self.median) ** 2) / (2 * self.omega ** 2)), 5)

    def plot(self, verbose=True, subplot=p):
        xxx = []
        yyy = []
        for i in self.domain:
            xxx.append(i)
            yyy.append(self.value(i))
        subplot.plot(xxx, yyy)
        subplot.plot(self.domain.end + (self.domain.end - self.domain.begin) / 3, -0.1)
        subplot.text(self.median, 1.00, str(self.median))

    def centr(self):
        return self.median

    def mode(self):
        return self.median

    def card(self):
        return round(math.sqrt(2 * math.pi) * self.omega, 5)


class Algebra():
    def __init__(self):
        pass


class SubsetAlgebra(Algebra):
    def __init__(self, tnorm=None):
        Algebra.__init__(self)
        self.tnorm = tnorm or MinMax()

    def _fuzzy_algebra(self, one, other, operation):
        if isinstance(self, Point) or isinstance(other, Point):
            raise NotImplementedError
        if isinstance(other, float) or isinstance(other, int):
            res = Subset(domain=one.domain)
            for i in res.domain:
                res[i] = max(
                    min(
                        operation(one[i], other),
                        1.0),
                    0.0)
            return res

        if isinstance(one, Interval) and isinstance(other, float):
            l = max(
                min(
                    operation(one.level, other),
                    1.0),
                0.0)
            return Interval(one.domain.begin, one.domain.end, l)

        begin = min(one.domain.begin, other.domain.begin)
        end = max(one.domain.end, other.domain.end)
        acc = max(one.domain.acc, other.domain.acc)

        domain = pyinference.fuzzy.domain.RationalRange(begin, end, acc=acc)
        res = Subset(domain=domain)
        for i in res.domain:
            res[i] = max(
                min(
                    operation(one[i], other[i]),
                    1.0),
                0.0)
        return res

    def __add__(self, one, other):
        return self._fuzzy_algebra(one, other, lambda x, y: x + y)

    def __sub__(self, one, other):
        return self._fuzzy_algebra(one, other, lambda x, y: x - y)

    def __mul__(self, one, other):
        return self._fuzzy_algebra(one, other, lambda x, y: x * y)

    def __and__(self, one, other):
        return self._fuzzy_algebra(one, other, lambda x, y: self.tnorm.norm(x, y))

    def __or__(self, one, other):
        return self._fuzzy_algebra(one, other, lambda x, y: self.tnorm.conorm(x, y))

    def __div__(self, one, other):
        raise NotImplementedError

    def __pow__(self, one, other):
        if not (isinstance(other, float) or isinstance(other, int)):
            raise NotImplementedError
        begin = one.domain.begin
        end = one.domain.end
        res = Subset(begin, end)
        for i in res.domain:
            res[i] = min(one.value(i) ** other, 1)
        return res

    # #    def __cmp__(self, one, other):
    # #        raise NotImplementedError

    def __eq__(self, one, other):
        return max(
            min(
                abs(one & other) / abs(one),
                1.0),
            0.0)

    def __ne__(self, other):
        return 1 - (self == other)


class NumbersAlgebra(Algebra):
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
