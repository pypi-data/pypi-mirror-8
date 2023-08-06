import math


class RunningStats(object):
    # implementation of http://www.johndcook.com/standard_deviation.html

    def __init__(self):
        self.runs = 0
        self.total = 0
        self.min = float('inf')
        self.max = 0
        self.__old_mean = self.__new_mean = self.__old_exp = self.__new_exp = None

    def update(self, duration):
        self.total += duration
        self.min = min(duration, self.min)
        self.max = max(duration, self.max)
        self.runs += 1
        if self.runs == 1:
            self.__old_mean = self.__new_mean = duration
            self.__old_exp = 0.0
        else:
            delta = duration - self.__old_mean
            self.__new_mean = self.__old_mean + delta / self.runs
            self.__new_exp = self.__old_exp + delta * (duration - self.__new_mean)

            self.__old_mean = self.__new_mean
            self.__old_exp = self.__new_exp

    @property
    def avg(self):
        return self.total / self.runs if self.runs else 0.0

    @property
    def mean(self):
        return self.__new_mean if self.runs else 0.0

    @property
    def variance(self):
        return self.__new_exp / (self.runs - 1) if self.runs > 1 else 0.0

    @property
    def stddev(self):
        return math.sqrt(self.variance)

    def __str__(self):
        return "Stats[%s runs in %.4fsec, min=%.4fsec, max=%.4fsec, avg=%.4fsec, mean=%.4fsec, stddev=%.4fsec]" % (
            self.runs, self.total, self.min, self.max, self.avg, self.mean, self.stddev
        )
