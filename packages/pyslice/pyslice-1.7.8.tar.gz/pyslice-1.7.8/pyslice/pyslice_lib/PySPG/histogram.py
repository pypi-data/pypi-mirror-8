#! /usr/bin/python

from __future__ import print_function

import math

class SPGHistogram:
    __boxsize = 1
    __dict = {}
    __elements = 0

    def __init__(self, boxsize=1):
        self.__boxsize = boxsize
        self.__elements = 0.
#    import sys
#    sys.stderr.write("histogram box size = %lf\n"%self.__boxsize)

    def __getitem__(self, value):

        nearest = self.__get_nearest(value)

        if self.__dict.has_key(nearest):
            return self.__dict[nearest] / self.__elements
        else:
            return 0.

    def add_value(self, value):
        nearest = self.__get_nearest(value)
        if self.__dict.has_key(nearest):
            self.__dict[nearest] += 1.
        else:
            self.__dict[nearest] = 1.
        self.__elements += 1.

    def __str__(self):
        if self.__elements == 0:
            return " "
        keys = self.__dict.keys()
        keys.sort()
        return "\n".join([
                         "%f\t%f" % (k, (self.__dict[k] / self.__elements))
                         for k in keys
                         ])

    def __get_nearest(self, value):
        return self.__boxsize * math.floor(value / self.__boxsize)

    def get_dataset(self):
        if self.__elements == 0:
            return [[0, 0]]
        keys = self.__dict.keys()
        keys.sort()
        return [
            [k, (self.__dict[k] / self.__elements)]
            for k in keys
        ]


if __name__ == "__main__":
    a = SPGHistogram(.1)
    import random
    import sys
    import time

    time1 = time.time()
    for i in range(100000):
        a.add_value(random.gauss(0.1, 0.5))
    time2 = time.time()

    print(a)
    sys.stderr.write("ellapsed time: %lf\n" % (time2 - time1))
