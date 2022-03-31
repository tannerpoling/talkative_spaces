# DIFFERS FROM SYNTH OF SELF'S SYNTHITER!
# MODIFIED 03/23/2022

from collections import deque

class SynthIter:
    # an interator that continually returns a 'base' value, until given a sequence of values

    def __init__(self, initValue = 1.0):
        self.initValue = initValue
        self.q = deque()
        self.q.append(initValue)

    def __iter__(self):
        return self

    def __next__(self):
        # if there is more than one value in queue, use popleft() to remove from queue
        if len(self.q) == 1:
            num = self.q[0]
        else:
            num = self.q.popleft()
        return num

    def append(self, values):
        for val in values:
            self.q.append(val)

    def changeBase(self, value):
        # self.q.append(value)
        self.q[0] = value
        # self.q.popleft()

    def getBase(self):
        return self.q[0]

    def getValues(self):
        return str(self.q)

    def hasValues(self):
        return (len(self.q == 1));

    def remove(self, numValues):
        if numValues > len(self.q):
            numValues = len(self.q) - 1     # always at least 1 value in self.q
        for i in range(numValues):
            self.q.popleft()
