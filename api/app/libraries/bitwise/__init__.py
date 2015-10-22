__author__ = 'gia'


class Bitwise:
    __bit = 0

    def __init__(self, bit=0):
        self.__bit = bit

    def has(self, bit):
        return self.__bit & bit > 0

    def set(self, bit):
        self.__bit = bit
        return self

    def add(self, bit):
        self.__bit = self.__bit | bit
        return self

    def remove(self, bit):
        self.__bit = (self.__bit | bit) ^ bit

    @property
    def int(self):
        return self.__bit

    @property
    def array(self):
        results = []

        for i in range(1, self.__bit):
            if self.has(i):
                results.append(i)
            i *= 2

        return results
