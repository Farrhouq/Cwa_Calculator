class SpecialStr:

    def __init__(self, ss):
        self.ss = ss
        self.part1 = 'Course[' + str(ss[0]) + ']'
        self.part2 = 'Score: ' + str(ss[1])
        self.part3 = 'Credit(s): ' + str(ss[2])


class New:

    def __init__(self, tup):
        self.tup = tup
        self.p0 = tup[0]
        self.p1 = tup[1]
        self.p2 = tup[2]